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

########################################
# For Reference
########################################

def classical_qft(j, d):
	k_vec = lambda k : np.array([0 for i in range(d) if i != k else 1])
	omega = 2.0 * np.pi * 1j / d
	return (1.0 / np.sqrt(d)) * np.sum([omega ** (k * j) * k_vec(k) for k in range(d)])

def classical_iqft(j, d):
	k_vec = lambda k : np.array([0 for i in range(d) if i != k else 1])
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

# Reference: http://www-bcf.usc.edu/~tbrun/Course/lecture13.pdf (Page 10)
def QFT_mat(n):
	omega = np.exp(2.0 * np.pi * 1j / n)
	mat = np.ones((n, n))
	for i in range(1, n):
		for j in range(i, n):
			mat[i][j] *= omega
	return mat / math.sqrt(float(n))

def QFT_gate(n):
	# Get the Quil definition for the new gate
	QFT_definition = DefGate("QFT", QFT_mat(k))
	# Get the gate constructor
	QFT = QFT_definition.get_constructor()
	return QFT, QFT_definition

########################################
# Quantum Implemenations
########################################

# Fourier Transform
def qft(phi, n):
	pq = Program()
	QFT, QFT_definition = QFT_gate(n)
	pq += QFT_definition
	pq += QFT(phi)
	return pq

# Inverse Fourier Transform
def iqft(j, d):
	pass

