from typing import List
import numpy as np

import random

from pyquil import Program
from pyquil.gates import X, H, CNOT
from pyquil.quil import address_qubits
from pyquil.quilatom import QubitPlaceholder
from pyquil.api import QVMConnection
from pyquil.api import WavefunctionSimulator


""" Initialize list of qubits to pure |1> state.

    @param  p (List[QubitPlaceholder]): list of qubits in pure |0> state.
    @return pq (Program): corresponding PyQuil Program.
"""
def init_p(p: List[QubitPlaceholder], noise=None) -> Program:
    pq = Program()
    for i in range(len(p)):
        pq += X(p[i])
    return pq


""" Entangles phi with a series of signal particles.

    @param  phi (QubitPlaceholder): qubit containing transformed version
                                    of the original secret.
    @param  p (List[QubitPlaceholder]): single particle pure |1> qubits.
    @return pq (Program): corresponding PyQuil Program.
"""
def entangle(phi: QubitPlaceholder, p: List[QubitPlaceholder],
             noise=None) -> Program:
    pq = Program()
    pq += H(phi)
    for i in range(len(p)):
        pq += CNOT(phi, p[i])
    return pq


""" Disentangles the entangled state consisting of phi and a list of particles.

    @param  phi (QubitPlaceholder): entangled secret qubit.
    @param  p (List[QubitPlaceholder]): entangled single particle qubits.
    @return pq (Program): corresponding PyQuil Program.
"""
def disentangle(phi: QubitPlaceholder, p: List[QubitPlaceholder],
                noise=None) -> Program:
    pq = Program()
    for i in range(len(p)):
        pq += CNOT(phi, p[i])
    pq += H(phi)
    return pq


""" Simple tests demonstrating qubit entanglement/disentanglement workloads.

    @param  n (int): number of single particle qubits (p_0,...,p_{n-1}).
"""
def entangle_test(n=5):
    phi = QubitPlaceholder()
    p = [QubitPlaceholder() for i in range(n)]

    test_pqs = [
        init_p(p) + entangle(phi, p),
        init_p(p) + entangle(phi, p) + disentangle(phi, p),
        init_p(p) + H(phi) + entangle(phi, p),
        init_p(p) + H(phi) + entangle(phi, p) + disentangle(phi, p),
    ]

    wf_sim = WavefunctionSimulator()
    for pq in test_pqs:
        print(wf_sim.wavefunction(address_qubits(pq)))


def main():
    entangle_test()


if __name__ == '__main__':
    main()

