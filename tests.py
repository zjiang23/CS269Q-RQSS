from typing import Dict, List, Callable, Union, Tuple
from pyquil import Program
from pyquil.quilatom import QubitPlaceholder
from pyquil.api import get_qc
from pyquil.quil import address_qubits
from pyquil.gates import I, X, Y, Z, H, RX, RY, RZ, MEASURE

from qft import qft, iqft
from entangle import init_p, entangle, disentangle
from agents import Alice, Bob

import numpy as np

Q = Union[int, QubitPlaceholder]

def run(secret_ansatz: Callable[[Q], Program],
		alice_prob_real: float = 0.4,
		num_bobs: int = 2,
		num_trials: int = 1,
		verification_program: Callable[[np.array], bool] = lambda x: False):
	alice = Alice(secret_ansatz, prob_real=alice_prob_real)
	while not alice.secret_revealed:
		protocol = Program()
		bob_memories = protocol.declare('ro', 'BIT', num_bobs ** 2)
		phi_dash_copies = alice.deal_shares(num_bobs)
		bobs = [Bob(shares=phi_dash_copies[curr_id],
					memory=[bob_memories[curr_id * num_bobs + i] for i in range(num_bobs)],
					self_id=curr_id)
				for curr_id in range(num_bobs)]
		
		for bob in bobs:
			bob.set_bob_map(bobs)
			bob.distribute_all_shares()
		
		for bob in bobs:
			bob.retrieve(num_bobs)

		protocol += alice.protocol
		for bob in bobs:
			protocol += bob.protocol

		qc = get_qc("{}q-qvm".format(num_bobs ** 2))
		protocol = protocol.wrap_in_numshots_loop(num_trials)
		addresses = {qubit[0]: i * num_bobs + j
						for i, qbyte in enumerate(alice.q_mat)
							for j, qubit in enumerate(qbyte)}
		# print(addresses)
		protocol = address_qubits(protocol, addresses)
		# print(protocol)
		ep = qc.compile(protocol)
		result = qc.run(ep)

		alice.reset()

		result = np.reshape(result, (num_bobs, num_bobs))
		print(result)
		# break
		# Write verification code
		results = result[:, 1:]
		verified = (results == results[0]).all()
		if verified: #verification_program(result):
			if alice.secret_revealed:
				print("SECRET REVEALED")
			else:
				print("RETRYING...")
		else:
			print("CHEATING DETECTED")
			break

		#if verified
		#alice reveals if secret revealed
		#else terminate program 

	return result

def tests():
	secret_ansatz = lambda q: Program() + H(q)
	for num_bobs in range(2, 4):
		def verification_program(results):
			results = results[:, 1:]
			return (results == results[0]).all()

		result = np.array(run(secret_ansatz, num_bobs=num_bobs, verification_program=verification_program))
		# result = result.flatten()
		# result[result == 0] = -1
		# _sum = abs(np.sum(result[i] for i in range(num_bobs ** 2) if (i % 2 == 1)))
		# passed = (_sum == num_bobs)

		# result = np.reshape(result, (num_bobs, num_bobs))

		# if passed:
		# 	print("{} bobs: Passed".format(num_bobs))
		# else:
		# 	result[result == -1] = 0
		# 	print("{} bobs: Failed with {} and sum {}".format(num_bobs, result, _sum))

if __name__ == "__main__":
	tests()
