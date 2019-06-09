# Rational Quantum Secret Sharing in PyQuil
[Stanford CS269Q](https://cs269q.stanford.edu/) (Spring 2019) Final Project [[Project Report](https://github.com/zjiang23/CS269Q-QSS/blob/master/cs269q_rqss_project_report.pdf)]
by Manan Rai, Andrew Tierno, and Jerry Zhilin Jiang

PyQuil implementation of Rational Quantum Secret Sharing (RQSS), based on the [Qin et al. (2018)](https://www.nature.com/articles/s41598-018-29051-z) paper.

## Requirements
It is recommended to create and activate an [Anaconda](https://www.anaconda.com/distribution/) virtual environment from the `environment.yml` configuration to handle all Python dependencies.

[Forest SDK](https://www.rigetti.com/forest) is also required.


## How to run
Before executing any RQSS code, start a QVM instance (`qvm -S`) and a Rigetti Quil Compiler instance (`quilc -S`) in the background.

A customizable test program is available in `tests.py`.

Running instructions are presented below:

```
usage: tests.py [-h] [-N N] [-a] [-n n] [-cheat]
                [-c [CONSISTENT_PROG_CHEATERS [CONSISTENT_PROG_CHEATERS ...]]]
                [-r [RANDOM_PROG_CHEATERS [RANDOM_PROG_CHEATERS ...]]] [-v]
                [-S] [-s] [-p ALICE_PROB_REAL]

Rational Quantum Secret Sharing Scheme

optional arguments:
  -h, --help            show this help message and exit
  -N N, --num_runs N    number of times to run same test [default: 1]
  -a, --run_all         flag to run all tests
  -n n, --num_bobs n    number of Bobs (receiving agents) [default: 3]
  -cheat, --test_cheating
                        flag to test cheating [default: False]
  -c [CONSISTENT_PROG_CHEATERS [CONSISTENT_PROG_CHEATERS ...]], --consistent_prog_cheaters [CONSISTENT_PROG_CHEATERS [CONSISTENT_PROG_CHEATERS ...]]
                        indices of Bobs who cheat with consistent program
                        [default: []]
  -r [RANDOM_PROG_CHEATERS [RANDOM_PROG_CHEATERS ...]], --random_prog_cheaters [RANDOM_PROG_CHEATERS [RANDOM_PROG_CHEATERS ...]]
                        indices of Bobs who cheat with random program
                        [default: []]
  -v, --verbose         print all progress [default: False]
  -S, --silent          silence all output [default: False]
  -s, --only_summarize  silence all output except final output [default:
                        False]
  -p ALICE_PROB_REAL, --alice_prob_real ALICE_PROB_REAL
                        probability that Alice generates the true secret
```

These instructions can be printed using `python tests.py --help` (or `-h`) for detailed instructions.
