#!/usr/bin/env python3
#
# bfpython v1.0.0
# Copyright 2021 Rog3rSm1th
#
# Usage: bfpython.py [-h] [-a] -f FILE
# You can also use it as a library : import bfpython
# bfpython.evaluate(<your code>, show_array=<Boolean>)
#
import sys
import re
import argparse

ARRAY_LENGTH = 30000
# Each cell is a n-bits integer
# In this implementation we choose to use values from 0 to 255
BITS = 8

class ArrayController:
    
    def __init__(self):
        self.array = [0] * ARRAY_LENGTH
        self.current_cell = 0
    
    def increment(self):
        self.array[self.current_cell] = (self.array[self.current_cell] + 1) % (2 ** BITS)

    def decrement(self):
        self.array[self.current_cell] = (self.array[self.current_cell] - 1) % (2 ** BITS)

    # Dangling pointers protection
    # Going left from cell 0 will wrap around to the last cell
    def right(self):
        self.current_cell = (self.current_cell + 1) % (ARRAY_LENGTH)

    # Going right from the last cell will wrap around to the first cell
    def left(self):
        self.current_cell = (self.current_cell - 1) % (ARRAY_LENGTH)

    # Displays the value of the table's cells after the execution 
    def show_array(self):
        if all(cell == 0 for cell in self.array):
            return 
        while self.array[-1] == 0:
            self.array.pop()
        print(self.array)

class BrainfuckInterpreter:

    def __init__(self, sourcecode, array_controller, show_array):
        self.array_controller = array_controller
        self.array = array_controller.array
        self.position = 0
        self.length = len(sourcecode)
        self.sourcecode = list(sourcecode)
        self.show_array = show_array

    def execute_instruction(self, instruction):
        # Increments the value at the current cell by one
        if instruction == "+":   self.array_controller.increment()
        # Decrements the value at the current cell by one
        elif instruction == '-': self.array_controller.decrement()
        # Moves the data pointer to the next cell (cell on the right)
        elif instruction == ">": self.array_controller.right()
        # Moves the data pointer to the previous cell (cell on the left)
        elif instruction == "<": self.array_controller.left()
        # Prints the ASCII value at the current cell 
        elif instruction == ".": print(chr(self.array[self.array_controller.current_cell]), end='')
        # If the value at the current cell is zero, skips to the corresponding ]. Otherwise, move to the next instruction
        elif instruction == "[":
            if self.array[self.array_controller.current_cell] == 0:
                corresponding_bracket = self.sourcecode[0:self.position+1].count("[")
                self.position = [m.start() for m in re.finditer(']', ''.join(self.sourcecode))][-corresponding_bracket]
                return 
        # If the value at the current cell is zero, move to the next instruction. Otherwise, move backwards in the instructions to the corresponding [
        elif instruction == "]":
            if self.array[self.array_controller.current_cell] != 0:
                while self.sourcecode[self.position] != "[":
                    self.position -= 1
        # Reads a single input character into the current cell
        elif instruction == ",":
            char = sys.stdin.read(1)
            self.array[self.array_controller.current_cell] = ord(char) if char else 0  

        self.position += 1

    def run(self):
        while self.position < self.length:
            self.execute_instruction(self.sourcecode[self.position])
        if self.show_array:
            self.array_controller.show_array()

# Run the BrainFuck program
def evaluate(brainfuck_code, show_array=False):
    array_controller = ArrayController()        
    BrainfuckInterpreter(brainfuck_code, array_controller, show_array=show_array).run()

def main():
    # Usage: bfpython.py [-h] [-a] -f FILE
    parser = argparse.ArgumentParser(description='A BrainFuck interpreter written in python')
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--array', action='store_true', 
        help="Show the array after the execution")

    parser.add_argument('-f', '--file', required=True, help="Path to the brainfuck program")
    args = parser.parse_args()

    program_file = args.file
    try:
        with open(program_file, 'r') as f:
            sourcecode = ''.join(instruction for instruction in f.read() if instruction in '+-<>.,[]')
            evaluate(sourcecode, show_array=args.array)
    except:
        print("Error : Impossible to open your BrainFuck program")
    sys.exit()

if __name__ == "__main__":
    main()