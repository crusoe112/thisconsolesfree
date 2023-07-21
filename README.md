# This Console's Free

A simple utility for testing Target Communication Framework (TCF) debugging agents

## Description

Provides utilities for reading files, writing files, and executing commands on a remote target via the TCF protocol.

## Getting Started

### Dependencies

* Python3

### Installing

* git clone https://github.com/crusoe112/thisconsolesfree.git

### Executing program

#### Reading a file
* `python3 thisconsolesfree.py read [-h] [--rport RPORT] lfile rfile rhost`
* E.g. `python3  thisconsolesfree.py read remote_shadow '/etc/shadow' 127.0.0.1`

#### Writing a file
* `python3 thisconsolesfree.py write [-h] [--rport RPORT] lfile rfile rhost`
* E.g. `python3 thisconsolesfree.py write modified_shadow '/etc/shadow' 127.0.0.1`

#### Executing a command
* `python3 thisconsolesfree.py run [-h] [--pwd PWD] [--rport RPORT] cmd rhost`
* E.g. `python3 thisconsolesfree.py run 'cat /etc/shadow' 127.0.0.1`

#### Getting help
* `python3 thisconsolesfree.py help cmd`
* E.g. `python3 thisconsolesfree.py help read`

## Authors

Contributors names and contact info

Marc Bohler
[crusoe112](https://github.com/crusoe112)

## License

This project is licensed under the The MIT License (MIT) - see the LICENSE file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [Eclipse TCF Plugin](https://git.eclipse.org/c/tcf/org.eclipse.tcf.git)
