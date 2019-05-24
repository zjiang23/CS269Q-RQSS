'''
	Quantum Implementations of:
		1. Fourier Transform
		2. Inverse Fourier Transform
'''

import numpy as np

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
# Quantum Implemenations
########################################

def qft(j, d):
	pass

def iqft(j, d):
	pass