import re

from source.Parser.Lexer import *
from source.Parser.CoreFunctions import *
from source.Parser.Baseclasses import *


def NOT(operand):
    return UnaryOperations(operand, "~", operand.size)


def RAND(operand):
    return UnaryOperations(operand, "&", operand.size)


def RNAND(operand):
    return UnaryOperations(operand, "~&", operand.size)


def RXOR(operand):
    return UnaryOperations(operand, "^", operand.size)


def RXNR(operand):
    return UnaryOperations(operand, "~^", operand.size)


def ROR(operand):
    return UnaryOperations(operand, "|", operand.size)


def RNOR(operand):
    return UnaryOperations(operand, "~|", operand.size)


def MUL(left, right):
    return BaseOperations("*", left, right, max(left.size, right.size))


def DIV(left, right):
    return BaseOperations("/", left, right, max(left.size, right.size))


def ADD(left, right):
    return BaseOperations("+", left, right, max(left.size, right.size))


def SUB(left, right):
    return BaseOperations("-", left, right, max(left.size, right.size))


def ShiftLeft(left, right):
    return BaseOperations("<<", left, right, left.size + right.size)


def ShiftRight(left, right):
    return BaseOperations(">>", left, right, min(left.size - right.size, 1))


def AND(left, right):
    return BaseOperations("&", left, right, max(left.size, right.size))


def XOR(left, right):
    return BaseOperations("^", left, right, max(left.size, right.size))


def XNR(left, right):
    return BaseOperations("~^", left, right, max(left.size, right.size))


def BOR(left, right):
    return BaseOperations("|", left, right, max(left.size, right.size))


class VerilogParser:
    def __init__(self, file):
        self.Token = Tokens()
        self.constants = []
        self.const_id = 0
        self.exceptions = []
        input_signals, inputs_types, input_size, output_signals, output_types, output_size = get_in_out_signal_names(
            file)
        self.observer = ContinuousObserver()
        self.Module_Node = VerilogModule(get_Module_Name(file))
        for inp, inp_type, inp_size in zip(input_signals, inputs_types, input_size):
            self.Module_Node.add_input(SignalNode(inp, inp_type, inp_size, self.observer))
        for out, out_type, out_size in zip(output_signals, output_types, output_size):
            self.Module_Node.add_output(SignalNode(out, out, out_size, self.observer))

    def prep_blocking(self, NewToken):
        WriteTo = NewToken[0]
        del NewToken[0]
        del NewToken[0]
        del NewToken[-1]
        NewToken = NewToken[0]
        for key_out in self.Module_Node.outputs:
            if key_out == WriteTo:
                WriteTo = self.Module_Node.outputs[key_out]
        for key_in in self.Module_Node.inputs:
            found = re.search(key_in, NewToken)
            if found:
                NewToken = re.sub(key_in, "self.Module_Node.inputs[\"" + key_in + "\"]", NewToken)
        matches = re.finditer("[1-9]*'(b|d|h)[0-9]*", NewToken)
        for match in matches:
            constant_str = match.group()
            cons_type = re.search(r"'(d|b|h)", constant_str).group()
            constant = re.sub(r"[1-9]*'(b|d|h)", "", constant_str)
            if cons_type == "'b":
                constant = int(constant, 2)
            elif cons_type == "'h":
                constant = int(constant, 16)
            else:
                constant = int(constant, 10)
            binary = bin(constant)
            binary = re.sub("0b", "", binary)
            self.constants.append(Constant(constant, len(binary)))
            NewToken = re.sub(constant_str, "self.constants[" + str(self.const_id) + "]", NewToken)
            self.const_id += 1
        matches = re.finditer("(\(|,)[0-9]+", NewToken)
        for match in matches:
            constant_str = match.group()
            constant_prev = re.search("(\(|,)", constant_str).group()
            if constant_prev == "(":
                constant_prev = "\\" + constant_prev
            constant_str = re.sub(r"(\(|,)", "", constant_str)
            if constant_str != "":
                constant = int(constant_str, 10)
                binary = bin(constant)
                binary = re.sub("0b", "", binary)
                self.constants.append(Constant(constant, len(binary)))
                NewToken = re.sub(constant_prev + constant_str,
                                  constant_prev + "self.constants[" + str(self.const_id) + "]", NewToken)
                NewToken = re.sub(r"\\", "", NewToken)
                self.const_id += 1
        print(NewToken)
        return WriteTo, NewToken

    def Parse(self):
        NewToken, TokenType, TokenLine = self.Token.get_token()
        is_assign = re.search("assign", TokenType)
        # print(NewToken)
        if is_assign:
            WriteTo, NewToken = self.prep_blocking(NewToken)
            self.Module_Node.add_assign(ContinuousAssignment(WriteTo, eval(NewToken), TokenLine))
        for cont in self.Module_Node.continuous_assignment:
            self.observer.Register(cont)
        return self.Module_Node


l = Lexer("adder.v")
l.doLexing()
v = VerilogParser("adder.v")
main_node = v.Parse()
main_node.inputs["in1"].value = 2
main_node.inputs["in2"].value = 3
print(main_node.outputs["out"].value)

