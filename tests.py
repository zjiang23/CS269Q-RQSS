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
import argparse

Q = Union[int, QubitPlaceholder]

def run(secret_ansatz: Callable[[Q], Program],
		alice_prob_real: float = 0.4,
		num_bobs: int = 2,
		num_trials: int = 1,
		verification_program: Callable[[np.array], bool] = lambda x: False,
		consistent_cheating_bobs: list = [],
		random_cheating_bobs: list = []):
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
					is_consistent_cheater=(curr_id in consistent_cheating_bobs),
					is_random_cheater=(curr_id in random_cheating_bobs))
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
		if args.verbose:
			print(result)
		if verification_program(result):
			if alice.secret_revealed:
				print("SECRET REVEALED [{}]".format(wf_sim.wavefunction
														(address_qubits
															(secret_ansatz(alice.q_mat[0][0][0])))))
			else:
				print("RETRYING...")
		else:
			print("CHEATING DETECTED")
			break

	return result


def tests():
	secret_ansatzs = [
		#lambda q: Program() + X(q),
		lambda q: Program() + X(q) + H(q)
	]
	
	for secret_ansatz in secret_ansatzs:
		if args.run_all:
			num_bobs_range = range(2, 4)
		else:
			num_bobs_range = [args.num_bobs]
		for num_bobs in num_bobs_range:
			def verification_program(results):
				results = results[:, 1:]
				return (results == results[0]).all()

			def single_run(message, **kwargs):
				print("=" * 90)
				print("Running test with 1 Alice and {} Bobs, {}".format(num_bobs, message))
				print("-" * 90)
				run(**kwargs)
				print("=" * 90)
				print()

			def combination_run(**kwargs):
				print("=" * 70)
				print("Running test with 1 Alice and {} Bobs,\n".format(num_bobs) +
						"such that Bobs {} cheat with a consistent program\n".format(list_to_string(args.consistent_prog_cheaters)) +
						"and {} with a random program:".format(list_to_string(args.random_prog_cheaters)))
				print("-" * 70)
				run(**kwargs)
				print("=" * 70)
				print()

			if args.run_all:
				single_run("and no cheating Bobs", secret_ansatz=secret_ansatz,
							num_bobs=num_bobs, verification_program=verification_program)
				for i in range(num_bobs):
					single_run("such that Bob {} cheats with a consistent program:".format(num_bobs, i),
								secret_ansatz=secret_ansatz, num_bobs=num_bobs,
								verification_program=verification_program, consistent_cheating_bobs=[i])
					single_run("such that Bob {} cheats with a random program:".format(num_bobs, i),
								secret_ansatz=secret_ansatz, num_bobs=num_bobs,
								verification_program=verification_program, random_cheating_bobs=[i])

			elif args.test_cheating:
				def list_to_string(l):
					if len(l) < 0:
						return "No Bobs cheat"
					elif len(l) == 1:
						return "Bob " + str(l[0]) + " cheats"
					elif len(l) == 2:
						return "Bobs " + str(l[0]) + " and " + str(l[1]) + " cheat"
					else:
						s = "Bobs "
						for e in l[:-1]:
							s += str(e) + ", "
						s += "and " + str(l[-1])
						return s + " cheat"

				combination_run(secret_ansatz=secret_ansatz, num_bobs=num_bobs, verification_program=verification_program,
								consistent_cheating_bobs=args.consistent_prog_cheaters, random_cheating_bobs=args.random_prog_cheaters)

			else:
				print("=" * 70)
				print("Running test with 1 Alice and {} Bobs, and no cheating Bobs:".format(num_bobs))
				print("-" * 70)
				run(secret_ansatz, num_bobs=num_bobs, verification_program=verification_program)
				print("=" * 70)
				print()
			
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Rational Quantum Secret Sharing Scheme')
	parser.add_argument('-a', '--run_all', action='store_true', help='flag to run all tests')
	parser.add_argument('-n', '--num_bobs', metavar='n', type=int, default=3, help='number of Bobs (receiving agents) [default: 3]')
	parser.add_argument('-cheat', '--test_cheating', action='store_true', help='flag to test cheating [default: False]')
	parser.add_argument('-c', '--consistent_prog_cheaters', nargs='*', type=int, help='indices of Bobs who cheat with consistent program [default: []]')
	parser.add_argument('-r', '--random_prog_cheaters', nargs='*', type=int, help='indices of Bobs who cheat with random program [default: []]')
	parser.add_argument('-v', '--verbose', action='store_true', help='print progress [default: False]')

	args = parser.parse_args()
	tests()
