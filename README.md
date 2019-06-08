# Rational Quantum Secret Sharing in PyQuil
[Stanford CS269Q](https://cs269q.stanford.edu/) (Spring 2019) Final Project [[Project Report](https://github.com/zjiang23/CS269Q-QSS/blob/master/cs269q_rqss_project_report.pdf)]

PyQuil implementation of Rational Quantum Secret Sharing (RQSS), based on the [Qin et al. (2018)](https://www.nature.com/articles/s41598-018-29051-z) paper.

## Authors
Andrew Tierno, Jerry Zhilin Jiang, Manan Rai

## Requirements
It is recommended to create and activate an [Anaconda](https://www.anaconda.com/distribution/) virtual environment from the `environment.yml` configuration to handle all Python dependencies.

[Forest SDK](https://www.rigetti.com/forest) is also required.


## How to run
Before executing any RQSS code, start a QVM instance (`qvm -S`) and a Rigetti Quil Compiler instance (`quilc -S`) in the background.

A customizable test program is available in `tests.py`.

Run `python tests.py --help` (or `-h`) for detailed instructions.
