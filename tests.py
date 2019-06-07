from typing import Dict, List, Callable, Union, Tuple
from pyquil import Program
from pyquil.quilatom import QubitPlaceholder
from pyquil.api import get_qc
from pyquil.quil import address_qubits
from pyquil.gates import I, X, Y, Z, H, RX, RY, RZ, MEASURE

from qft import qft, iqft
from entangle import init_p, entangle, disentangle
from agents import Alice, Bob

Q = Union[int, QubitPlaceholder]

def run(secret_ansatz: Callable[[Q], Program], alice_prob_real: float = 0.4, num_bobs: int = 2, num_trials: int = 1):
	protocol = Program()
	alice = Alice(secret_ansatz, prob_real=alice_prob_real)
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
	protocol = address_qubits(protocol)
	# print(protocol)
	ep = qc.compile(protocol)
	result = qc.run(ep)
	return result

def tests():
	secret_ansatzs = [
		lambda q: Program() + X(q)# + H(q)
	]

	for secret_ansatz in secret_ansatzs:
		print(run(secret_ansatz))

if __name__ == "__main__":
	tests()
