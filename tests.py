from typing import Dict, List, Callable, Union, Tuple
from pyquil import Program
from pyquil.quilatom import QubitPlaceholder
from pyquil.api import get_qc, WavefunctionSimulator
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
		verification_program: Callable[[np.array], bool] = lambda x: False,
		consistent_cheating_bob: int = -1,
		random_cheating_bob: int = -1):
	alice = Alice(secret_ansatz, prob_real=alice_prob_real)
	wf_sim = WavefunctionSimulator()
	while not alice.secret_revealed:
		protocol = Program()
		bob_memories = protocol.declare('ro', 'BIT', num_bobs ** 2)
		phi_dash_copies = alice.deal_shares(num_bobs)
		# print("Original secret:", wf_sim.wavefunction(address_qubits(secret_ansatz(alice.q_mat[0][0][0]))))

		bobs = [Bob(shares=phi_dash_copies[curr_id],
					memory=[bob_memories[curr_id * num_bobs + i] for i in range(num_bobs)],
					self_id=curr_id,
					is_consistent_cheater=(curr_id == consistent_cheating_bob),
					is_random_cheater=(curr_id == random_cheating_bob))
				for curr_id in range(num_bobs)]
		
		for idx, bob in enumerate(bobs):
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
		
		protocol = address_qubits(protocol, addresses)
		ep = qc.compile(protocol)
		result = qc.run(ep)

		alice.reset()
		for bob in bobs:
			bob.reset()

		result = np.reshape(result, (num_bobs, num_bobs))
		print(result)
		if verification_program(result):
			if alice.secret_revealed:
				print("SECRET REVEALED [{}]\n".format(wf_sim.wavefunction
														(address_qubits
															(secret_ansatz(alice.q_mat[0][0][0])))))
			else:
				print("RETRYING...")
		else:
			print("CHEATING DETECTED\n")
			break

	return result

def tests():
	secret_ansatzs = [
		#lambda q: Program() + X(q),
		lambda q: Program() + X(q) + H(q)
	]
	
	for secret_ansatz in secret_ansatzs:
		for num_bobs in range(2, 4):
			def verification_program(results):
				results = results[:, 1:]
				return (results == results[0]).all()

			print("Running test with 1 Alice and {} Bobs, and no cheating Bobs:".format(num_bobs))
			result1 = np.array(run(secret_ansatz, num_bobs=num_bobs, verification_program=verification_program))
			for i in range(num_bobs):
				print("Running test with 1 Alice and {} Bobs, such that Bob{} cheats with consistent program:".format(num_bobs, i))
				result2 = np.array(run(secret_ansatz, num_bobs=num_bobs, verification_program=verification_program, consistent_cheating_bob=i))
			for i in range(num_bobs):
				print("Running test with 1 Alice and {} Bobs, such that Bob{} cheats with random program:".format(num_bobs, i))
				result2 = np.array(run(secret_ansatz, num_bobs=num_bobs, verification_program=verification_program, random_cheating_bob=i))
			
if __name__ == "__main__":
	tests()
