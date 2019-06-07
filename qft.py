'''
    Quantum Implementations of:
        1. Fourier Transform
        2. Inverse Fourier Transform
'''

import numpy as np
import math
from typing import Tuple, List
from pyquil import Program
from pyquil.gates import *
from pyquil.quilatom import QubitPlaceholder
from pyquil.api import WavefunctionSimulator
from pyquil.quil import address_qubits, DefGate

########################################
# For Reference
########################################

def classical_qft(j, d):
    k_vec = lambda k : np.array([0 if i != k else 1 for i in range(d)])
    omega = 2.0 * np.pi * 1j / d
    return (1.0 / np.sqrt(d)) * np.sum([omega ** (k * j) * k_vec(k) for k in range(d)])

def classical_iqft(j, d):
    k_vec = lambda k : np.array([0 if i != k else 1 for i in range(d)])
    omega = 2.0 * np.pi * 1j / d
    return (1.0 / np.sqrt(d)) * np.sum([omega ** (-k * j) * k_vec(k) for k in range(d)])

########################################
# Helper PyQuil Wrappers
########################################

# Reference: http://www-bcf.usc.edu/~tbrun/Course/lecture13.pdf (Page 10)
def Rk_mat(k):
    return np.array([[1, 0], [0, (2*np.pi*1j) / (2**k)]]) 

def RK_gate(k):
    # Get the Quil definition for the new gate
    Rk_definition = DefGate("Rk", Rk_mat(k))
    # Get the gate constructor
    RK = Rk_definition.get_constructor()
    return RK, Rk_definition

# Reference: https://courses.edx.org/c4x/BerkeleyX/CS191x/asset/chap5.pdf (Page 2)
def QFT_mat(n):
    omega = np.exp(2.0 * np.pi * 1j / n)
    mat = np.ones((n, n), dtype=complex)
    
    for i in range(1, n):
        for j in range(1, n):
            mat[i, j] = omega ** (i * j)

    mat /= math.sqrt(float(n))
    return mat

def QFT_gate(n):
    # Get the Quil definition for the new gate
    QFT_definition = DefGate("QFT{}".format(n), QFT_mat(2 ** n))
    # Get the gate constructor
    QFT = QFT_definition.get_constructor()
    return QFT, QFT_definition

def IQFT_mat(n):
    omega = np.exp(2.0 * np.pi * 1j / n)
    mat = np.ones((n, n), dtype=complex)
    
    for i in range(1, n):
        for j in range(1, n):
            mat[i, j] = omega ** (-i * j)

    mat /= math.sqrt(float(n))
    #print(mat.shape)
    return mat

def IQFT_gate(n):
    # Get the Quil definition for the new gate
    IQFT_definition = DefGate("IQFT{}".format(n), IQFT_mat(2 ** n))
    # Get the gate constructor
    IQFT = IQFT_definition.get_constructor()
    return IQFT, IQFT_definition

########################################
# Quantum Implemenations
########################################

# Fourier Transform
def qft(phi, n):
    pq = Program()
    QFT, QFT_definition = QFT_gate(n)
    pq += QFT_definition
    if isinstance(phi, List):
        pq += QFT(*phi) #Program("QFT({}) {}".format(n, *phi)) #QFT(*phi)
    else:
        pq += QFT(phi) #Program("QFT({}) {}".format(n, phi)) #QFT(phi)
    return pq

# Inverse Fourier Transform
def iqft(phi, n):
    pq = Program()
    IQFT, IQFT_definition = IQFT_gate(n)
    pq += IQFT_definition
    if isinstance(phi, List):
        pq += IQFT(*phi) #Program("IQFT({}) {}".format(n, *phi)) #IQFT(*phi)
    else:
        pq += IQFT(phi) #Program("IQFT({}) {}".format(n, phi)) #IQFT(phi)
    return pq

########################################
# Tests
########################################

def init_pure(p: List[QubitPlaceholder]) -> Program:
    pq = Program()
    for i in range(len(p)):
        pq += X(p[i])
    return pq

def qft_tests(n=4):
    phi = [QubitPlaceholder() for i in range(n)]
    tests = [
        init_pure(phi) + H(phi[0]) + qft(phi, n) + iqft(phi, n), # Should be H(0)
        init_pure(phi) + iqft(phi, n) + qft(phi, n), # Should be pure |1>'s
    ]
    wf_sim = WavefunctionSimulator()
    for test in tests:
        print(wf_sim.wavefunction(address_qubits(test)))

if __name__ == "__main__":
    qft_tests()
