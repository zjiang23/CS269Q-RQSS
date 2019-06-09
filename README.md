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

#### Note: It is suggested that you run as ```python -W ignore tests.py [...]```, with the warnings ignore flag turned on for cleaner console interaction.

Some example instructions are presented below:
- Run test with no cheating:
```console
foo@bar:~$ python -W ignore tests.py -a
Running test with 1 Alice and 3 Bobs, and no cheating Bobs
FAKE SECRET REVEALED, RETRYING...
FAKE SECRET REVEALED, RETRYING...
SECRET REVEALED [(0.7071067812+0j)|0> + (-0.7071067812+0j)|1>]
```
- Run test with no cheating and control Alice's probability of revealing real secret:
```console
foo@bar:~$ python -W ignore tests.py -a -p 1
Running test with 1 Alice and 3 Bobs, and no cheating Bobs
SECRET REVEALED [(0.7071067812+0j)|0> + (-0.7071067812+0j)|1>]
```
- Run test with 2 Bobs and no cheating
```console
foo@bar:~$ python -W ignore tests.py -a -n 2
Running test with 1 Alice and 2 Bobs, and no cheating Bobs
...
```
- Run test with Bobs 0 and 1 cheating with consistent program
```console
foo@bar:~$ python -W ignore tests.py -a -cheat --consistent_prog_cheaters 0 1
Running test with 1 Alice and 3 Bobs,
such that Bobs Bobs 0 and 1 cheat cheat with a consistent program
and No Bobs cheat with a random program:
CHEATING DETECTED
...
```
- Run test with verbose output
```console
foo@bar:~$ python -W ignore tests.py -v
Running test with 1 Alice and 3 Bobs, and no cheating Bobs
If no Bobs are cheating, all single particles should be 1.
Bob 1 received single particles: 1, 1
Bob 2 received single particles: 1, 1
Bob 3 received single particles: 1, 1
SECRET REVEALED [(0.7071067812+0j)|0> + (-0.7071067812+0j)|1>]
```
- Run all tests 2 times with only summary printed and all other console output suppressed
```console
foo@bar:~$ python -W ignore tests.py -a -N 2 -s
True Positives: 4
False Positives: 6
True Negatives: 14
False Negatives: 0
```
- Run all tests 2 times with completely silenced output
```console
foo@bar:~$ python -W ignore tests.py -a -N 2 -S
```

## Citation
For code:
```
@misc{PRQSS2019git,
  author = {Manan Rai and Andrew Tierno and Jerry Zhilin Jiang},
  title = {Rational Quantum Secret Sharing in PyQuil},
  year = {2019},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/zjiang23/CS269Q-RQSS}}
}
```

For paper:
```
@unpublished{PRQSS2019,
  author = {Manan Rai and Andrew Tierno and Jerry Zhilin Jiang},
  title = {Rational Quantum Secret Sharing in PyQuil},
  year = {2019},
  url = {unpublished}
}
```
