from typing import List, Callable, Union, Tuple
from pyquil.quilatom import QubitPlaceholder
from pyquil import Program
from pyquil.gates import RX, RY, RZ, X, Y, Z, H, CNOT
from random import random
from qft import qft, iqft
import math
import numpy as np

Q = Union[int, QubitPlaceholder]
QubitMap = List[List[Q]]
QubitSourceMap = List[List[Tuple[Q, int]]]

class Alice:
    def __init__(self, secret_ansatz: Callable[[List[Q]], Program], d_secret: int = 2, prob_real: float = 0.4):
        self.prob_real = prob_real
        self.d_secret = d_secret
        self.num_qubits = int(math.ceil(math.log2(self.d_secret)))
        self.protocol = Program()
        self.secret_ansatz = secret_ansatz
        assert d_secret == 2, "Error: Can only currently process two dimensional secrets."

    def generate_qubit_map(self, num_bobs: int) -> QubitMap:
        #num_qubits to represent the state, num_bobs - 1 for single particles
        return [[QubitPlaceholder() for _ in range(num_qubits + num_bobs - 1)] for _ in range(num_bobs)]

    def generate_n_test_secrets(self, n: int, qubits: QubitMap, len_ansatz: int = 50) -> Program:
        angles = np.arange(0, np.pi, np.pi / 16)
        rotation_gates = [RX, RY, RZ]
        flip_gates = [X, Y, Z, H]
        pq = Program()
        for _ in range(len_ansatz):
            qubit = np.random.choice(self.num_qubits)
            action = random()
            if action < 0.4: 
                gate = np.random.choice(rotation_gates)
                angle = np.random.choice(angles)
                for i in range(n):
                    pq += gate(angle, qubits[i][qubit])
            elif action < 1:
                gate = np.random.choice(flip_gates)
                for i in range(n):
                    pq += gate(qubits[i][qubit])
        return pq

    def deal_states(self, num_bobs: int) -> QubitSourceMap:
        should_reveal_secret = random()< self.prob_real
        qubits = generate_qubit_map(num_bobs)
        pq = Program()
        if should_reveal_secret:
            for i in range(num_bobs):
                pq += self.secret_ansatz(qubits[i])
        else:
            pq += self.generate_n_test_secrets(num_bobs, qubits)
        for qubits_b in qubits:
            secret = qubits_b[:self.num_qubits]
            single_particles = qubits_b[self.num_qubits:]
            pq += iqft(*secret, self.num_qubits)
            for single_particle in single_particles:
                pq += CNOT(*secret, single_particle)
                pq += qft(single_particle, 1)
            pq += qft(*secret, self.num_qubits)
        
        output = [[] for _ in range(num_bobs)]
        for i in range(len(qubits[0])):
            for j in range(num_bobs):
                source_idx = (j + i) % num_bobs
                output[j].append((qubits[source_idx][i], source_idx))
        return output