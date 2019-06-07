from typing import Dict, List, Callable, Union, Tuple
from pyquil.quilatom import QubitPlaceholder
from pyquil import Program
from pyquil.gates import RX, RY, RZ, X, Y, Z, H, MEASURE
from pyquil.quilatom import MemoryReference
from random import random
from qft import qft, iqft
from entangle import init_p, entangle, disentangle
import numpy as np

Q = Union[int, QubitPlaceholder]
QubitShare = Tuple[Q, int] # (Qubit, Entangling set the qubit is from)
QubitShareList = List[QubitShare]
QubitShareMatrix = List[QubitShareList]


class Alice:
    def __init__(self, secret_ansatz: Callable[[Q], Program], prob_real: float = 0.4):
        self.secret_ansatz = secret_ansatz
        self.prob_real = prob_real
        self.protocol = Program()
        self.secret_revealed = False

    def roll_matrix(self, matrix):
        arr = np.array(matrix, dtype=np.object)
        new_arr = np.zeros_like(arr)
        for qubit in range(arr.shape[1]):
            new_arr[:, qubit, :] = np.roll(arr[:, qubit, :], shift=qubit, axis=0)
        return new_arr.tolist()

    def tester_ansatz(self, qubit: Q, len_ansatz: int = 50) -> Program:
        angles = np.arange(0, np.pi, np.pi / 16)
        rotation_gates = [RX, RY, RZ]
        flip_gates = [X, Y, Z, H]
        pq = Program()
        for _ in range(len_ansatz):
            action = random()
            if action < 0.4:
                gate = np.random.choice(rotation_gates)
                angle = np.random.choice(angles)
                pq += gate(angle, qubit)
            elif action < 1:
                gate = np.random.choice(flip_gates)
                pq += gate(qubit)
        return pq

    def generate_qubit_matrix(self, num_bobs: int) -> List[QubitShareList]:
        return [[(QubitPlaceholder(), bob) for qubit in range(num_bobs)] for bob in range(num_bobs)]

    def deal_shares(self, num_bobs: int) -> QubitShareMatrix:
        q_mat = self.generate_qubit_matrix(num_bobs)
        if random() < self.prob_real:
            self.secret_revealed = True
        for bob in range(num_bobs):
            qubit_list = [q[0] for q in q_mat[bob]]
            self.protocol += init_p(qubit_list[1:])
            if self.secret_revealed:
                self.protocol += self.secret_ansatz(qubit_list[0])
            else:
                self.protocol += self.tester_ansatz(qubit_list[0])
            self.protocol += iqft(qubit_list[0], 1)
            self.protocol += entangle(qubit_list[0], qubit_list[1:])
            self.protocol += qft(qubit_list, num_bobs)
        return self.roll_matrix(q_mat)


class Bob:
    def __init__(self, shares: QubitShareList, memory: List[MemoryReference], self_id: int):
        self.shares = shares
        self.bob_map = None
        self.id = self_id
        self.protocol = Program()
        self.received_shares = [None for _ in range(len(shares))]
        self.received_shares[0] = self.shares[0][0]
        self.memory = memory

    def set_bob_map(self, bob_map: Dict):
        self.bob_map = bob_map

    def receive_share(self, share: QubitShare, qubit_idx: int):
        self.received_shares[qubit_idx] = share[0]

    def distribute_all_shares(self):
        assert self.bob_map is not None, "You must set bob map before distributing shares."
        for share_idx, share in enumerate(self.shares):
            self.bob_map[share[1]].receive_share(share, share_idx)

    def retrieve(self, num_bobs: int) -> Program:
        # Assert: Has received all components for the target entanglement set
        assert None not in self.received_shares, \
            "Bob #" + str(self.id) + ": retrieve() attempted without receiving all shares"

        self.protocol += iqft(self.received_shares, num_bobs)
        self.protocol += disentangle(self.received_shares[0], self.received_shares[1:])
        self.protocol += qft(self.received_shares[0], 1)
        for i, share in enumerate(self.received_shares):
            self.protocol += MEASURE(share, self.memory[i])
