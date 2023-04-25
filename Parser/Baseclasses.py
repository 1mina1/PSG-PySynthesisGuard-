from source.Parser.CoreFunctions import *
import threading

"""
this file contains the base class for all the required nodes by the
parser
"""


class ContinuousAssignment:
    def __init__(self, left, right, lineNum):
        self.left = left
        self.right = right
        self.line = lineNum
        self.left_nBits = (1 << self.left.size) - 1

    def run_assignment(self):
        if self.right.value != "x":
            self.left.value = self.right.value & self.left_nBits
        else:
            self.left.value = "x"


class ContinuousObserver:
    def __init__(self):
        self.subscribers = set()

    def Register(self, block):
        self.subscribers.add(block)

    def update(self):
        for subscriber in self.subscribers:
            subscriber.run_assignment()


class Constant:
    def __init__(self, value, size):
        self.value = value
        self.size = size


class SignalNode:
    def __init__(self, name, type, size, observer):
        self._value = "x"
        self.size = size
        self.name = name
        self.type = type
        self.observer = observer

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, valuechng):
        if valuechng != self._value:
            self._value = valuechng
            self.observer.update()


class VerilogModule:
    def __init__(self, name):
        self.module_name = name
        self.inputs = {}
        self.outputs = {}
        self.internal = []
        self.continuous_assignment = []
        self.procedual_assignment = []

    def add_input(self, inputAdd: SignalNode):
        self.inputs[inputAdd.name] = inputAdd

    def add_output(self, outputAdd: SignalNode):
        self.outputs[outputAdd.name] = outputAdd

    def add_internal(self, internalAdd: SignalNode):
        self.internal.append(internalAdd)

    def add_always(self, alwaysAdd: object):
        self.procedual_assignment.append(alwaysAdd)

    def add_assign(self, assignAdd: ContinuousAssignment):
        self.continuous_assignment.append(assignAdd)


class BaseOperations:
    def __init__(self, type: str, left, right, size):
        self.type = type
        self.left = left
        self.right = right
        self.size = size

    @property
    def value(self):
        # print("type is " + self.type + " and left value is " + str(self.left.value) + " and right is "+str(self.right.value))
        if not (self.left.value == "x" or self.right.value == "x"):
            if self.type == "&":
                return self.left.value & self.right.value
            elif self.type == "|":
                return self.left.value | self.right.value
            elif self.type == "^":
                return self.left.value ^ self.right.value
            elif self.type == "+":
                return self.left.value + self.right.value
            elif self.type == "*":
                return self.left.value * self.right.value
            elif self.type == "/":
                return self.left.value / self.right.value
            elif self.type == "~^" or self.type == "^~":
                return xnor(self.left.value, self.right.value)
            elif self.type == "<<":
                return self.left.value << self.right.value
            elif self.type == ">>":
                return self.left.value >> self.right.value
            else:
                return "x"
        else:
            return "x"


class UnaryOperations:
    def __init__(self, operand, type: str, size):
        self.operand = operand
        self.type = type
        if self.type == "~":
            self.size = size
        else:
            self.size = 1

    @property
    def value(self):
        # print("type is "+ str(self.type)+ " and operand is "+str(self.operand.value))
        if not self.operand.value == "x":
            if self.type == "~":
                return not_gate(self.operand.value, self.size)
            elif self.type == "&":
                return ReductionAnd(self.operand.value)
            elif self.type == "|":
                return ReductionOr(self.operand.value)
            elif self.type == "~&":
                return not_gate(ReductionAnd(self.operand.value), self.size)
            elif self.type == "~|":
                return not_gate(ReductionOr(self.operand.value), self.size)
            elif self.type == "^":
                return ReductionXor(self.operand.value)
            elif self.type == "~^" or self.type == "^~":
                return not_gate(ReductionXor(self.operand.value), self.size)
            else:
                return "x"
        else:
            return "x"

