from typing import List, Callable, Union, Tuple
from pyquil.quilatom import QubitPlaceholder
from pyquil import Program
from pyquil.gates import RX, RY, RZ, X, Y, Z, H, CNOT
from random import random
from qft import qft, iqft
from entangle import init_p, entangle, disentangle
import numpy as np

Q = Union[int, QubitPlaceholder]
QubitShare = Tuple[Q, int]
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
            self.protocol += iqft(qubit_list[0])
            self.protocol += entangle(qubit_list[0], qubit_list[1:])
        return self.roll_matrix(q_mat)

# class Alice:
#     def __init__(self, secret_ansatz: Callable[[List[Q]], Program], prob_real: float = 0.4):
#         self.prob_real = prob_real
#         self.protocol = Program()
#         self.secret_ansatz = secret_ansatz
#
#     def generate_qubit_map(self, num_bobs: int) -> QubitMap:
#         #1 to represent the state, num_bobs - 1 for single particles
#         return [[QubitPlaceholder() for _ in range(num_bobs)] for _ in range(num_bobs)]
#
#     def generate_n_test_secrets(self, n: int, qubits: QubitMap, len_ansatz: int = 50) -> Program:
#         angles = np.arange(0, np.pi, np.pi / 16)
#         rotation_gates = [RX, RY, RZ]
#         flip_gates = [X, Y, Z, H]
#         pq = Program()
#         for _ in range(len_ansatz):
#             qubit = 0
#             action = random()
#             if action < 0.4:
#                 gate = np.random.choice(rotation_gates)
#                 angle = np.random.choice(angles)
#                 for i in range(n):
#                     pq += gate(angle, qubits[i][qubit])
#             elif action < 1:
#                 gate = np.random.choice(flip_gates)
#                 for i in range(n):
#                     pq += gate(qubits[i][qubit])
#         return pq
#
#     def deal_states(self, num_bobs: int) -> QubitSourceMap:
#         should_reveal_secret = random()< self.prob_real
#         qubits = generate_qubit_map(num_bobs)
#         pq = Program()
#         if should_reveal_secret:
#             for i in range(num_bobs):
#                 pq += self.secret_ansatz(qubits[i])
#         else:
#             pq += self.generate_n_test_secrets(num_bobs, qubits)
#         for qubits_b in qubits:
#             secret = qubits_b[:self.num_qubits]
#             single_particles = qubits_b[self.num_qubits:]
#             pq += iqft(*secret, self.num_qubits)
#             for single_particle in single_particles:
#                 pq += CNOT(*secret, single_particle)
#                 pq += qft(single_particle, 1)
#             pq += qft(*secret, self.num_qubits)
#
#         output = [[] for _ in range(num_bobs)]
#         for i in range(len(qubits[0])):
#             for j in range(num_bobs):
#                 source_idx = (j + i) % num_bobs
#                 output[j].append((qubits[source_idx][i], source_idx))
#         return output