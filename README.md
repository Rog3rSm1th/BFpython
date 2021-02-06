# BFpython

BFpython is an interpreter for the BrainFuck language written in Python.

### What is BrainFuck

Brainfuck is an esoteric, Turing-Complete programming language created in 1993 by Urban Müller, notable for its extreme minimalism (only 8 commands !).

It uses an array of 30,000 8-bit integers, and a pointer which can move from cell to cell one at a time. The value of each cell can be incremented or decremented one at a time.

Each Brainfuck programme consists only of the following 8 instructions :

Command | Action
-------:|---
``+``   | increment the value of the current cell by 1
``-``   | decrement the value of the current cell by 1
``>``   | move to next cell
``<``   | move to previous cell
``.``   | print the ascii character of the current cell to stdout
``,``   | get a character from stdin and store it in the current cell
``[``   | if the current cell is 0, jump to the matching ``]``
``]``   | if the current cell is **not** 0, jump to the matching ``[``

### How to use BFpython

```console
$ git clone https://github.com/Rog3rSm1th/BFpython.git
$ cd BFpython
$ ./bfpython.py -f <path to the brainfuck program>
```

### Flags

Flag                | Action
-------------------:|---
``-a``/``--array`` | Show the array after the execution.

### Use it as a library

```py
>>> import bfpython
>>> program = '-[------->+<]>-.-[->+++++<]>++.+++++++..+++.[--->+<]>----.'
>>> bfpython.evaluate(program)
Hello!
```