import re
import itertools
from source.Parser.Lexer import *
from source.Parser.CoreFunctions import *
from source.Parser.Baseclasses import *
from itertools import chain


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


def LOGNEG(operand):
    return UnaryOperations(operand, "!", 1)


def RNOR(operand):
    return UnaryOperations(operand, "~|", operand.size)


def MUL(left, right):
    return BaseOperations("*", left, right, left.size + right.size)


def DIV(left, right):
    return BaseOperations("/", left, right, max(left.size, right.size))


def ADD(left, right):
    return BaseOperations("+", left, right, max(left.size, right.size) + 1)


def SUB(left, right):
    return BaseOperations("-", left, right, max(left.size, right.size))


def ShiftLeft(left, right):
    if isinstance(right, Constant):
        return BaseOperations("<<", left, right, left.size + right.value)
    else:
        return BaseOperations("<<", left, right, left.size + right.size)


def ShiftRight(left, right):
    if isinstance(right, Constant):
        return BaseOperations(">>", left, right, max(left.size - right.value, 1))
    else:
        return BaseOperations(">>", left, right, max(left.size - right.size, 1))


def AND(left, right):
    return BaseOperations("&", left, right, max(left.size, right.size))


def LAND(left, right):
    return BaseOperations("&&", left, right, 1)


def XOR(left, right):
    return BaseOperations("^", left, right, max(left.size, right.size))


def XNR(left, right):
    return BaseOperations("~^", left, right, max(left.size, right.size))


def BOR(left, right):
    return BaseOperations("|", left, right, max(left.size, right.size))


def LessThan(left, right):
    return BaseOperations("<", left, right, 1)


def LessThanEqual(left, right):
    return BaseOperations("<=", left, right, 1)


def GreaterThan(left, right):
    return BaseOperations(">", left, right, 1)


def GreaterThanEqual(left, right):
    return BaseOperations(">=", left, right, 1)


def Equal(left, right):
    return BaseOperations("==", left, right, 1)


def NotEqual(left, right):
    return BaseOperations("!=", left, right, 1)


def Always(sensitivity_list, blocks, lines):
    return ProcedualAssignment(sensitivity_list, blocks, lines)


def Blocking(left, right, line):
    return ContinuousAssignment(left, right, line, "Blocking")


def NonBlocking(left, right, line):
    return ContinuousAssignment(left, right, line, "NonBlocking")


def IF(Cond, blocks_true, Blocks_false, lines):
    return IfCondition(Cond, blocks_true, Blocks_false, lines)


def CASE(statement, Items, Items_lines, line_list, Non_parallel_case):
    return CaseStatement(statement, Items, Items_lines, line_list, Non_parallel_case)


class VerilogParser:
    def __init__(self, file):
        self.Token = Tokens()
        self.constants = []
        self.const_id = 0
        self.exceptions = []
        input_signals, inputs_types, input_size, input_lines, output_signals, output_types, output_size, output_lines, internal_signals, internal_types, internal_size, internal_lines = get_in_out_signal_names(
            file)
        self.observer = ContinuousObserver()
        self.Module_Node = VerilogModule(get_Module_Name(file))
        for inp, inp_type, inp_size, inp_line in zip(input_signals, inputs_types, input_size, input_lines):
            self.Module_Node.add_input(SignalNode(inp, inp_type, inp_size, self.observer, inp_line, "input"))
        for out, out_type, out_size, out_line in zip(output_signals, output_types, output_size, output_lines):
            self.Module_Node.add_output(SignalNode(out, out_type, out_size, self.observer, out_line, "output"))
        for internal, internal_type, intern_size, intern_line in zip(internal_signals, internal_types, internal_size,
                                                                     internal_lines):
            self.Module_Node.add_internal(
                SignalNode(internal, internal_type, intern_size, self.observer, intern_line, "internal"))

    def prep_blocking(self, NewToken):
        WriteTo = NewToken[0]
        del NewToken[0]
        del NewToken[0]
        del NewToken[-1]
        NewToken = NewToken[0]
        found = 0
        for key_out in self.Module_Node.outputs:
            if key_out == WriteTo:
                WriteTo = self.Module_Node.outputs[key_out]
                found = 1
                break
        if not found:
            for key_int in self.Module_Node.internal:
                if key_int == WriteTo:
                    WriteTo = self.Module_Node.internal[key_int]
        NewToken = self.Token_obj_Replace(NewToken)
        return WriteTo, NewToken

    def Token_obj_Replace(self, NewToken):
        for key_in in self.Module_Node.inputs:
            NewToken = re.sub(r"(?<!([a-z]|[A-Z]|_))" + key_in + r"(?!([0-9]|_|[a-z]|[A-Z]))",
                              "self.Module_Node.inputs[\"" + key_in + "\"]", NewToken)
        for key_int in self.Module_Node.internal:
            NewToken = re.sub(r"(?<!([a-z]|[A-Z]|_))" + key_int + r"(?!([0-9]|_|[a-z]|[A-Z]))",
                              "self.Module_Node.internal[\"" + key_int + "\"]", NewToken)
        for key_out in self.Module_Node.outputs:
            NewToken = re.sub(r"(?<!([a-z]|[A-Z]|_))" + key_out + r"(?!([0-9]|_|[a-z]|[A-Z]))",
                              "self.Module_Node.outputs[\"" + key_out + "\"]", NewToken)
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
            NewToken = re.sub(r"(?<!([1-9]))" + constant_str + r"(?!([0-9]|_))",
                              "self.constants[" + str(self.const_id) + "]", NewToken)
            self.const_id += 1
        return NewToken

    def Parse(self):
        NewToken, TokenType, TokenLine = self.Token.get_token()
        while NewToken:
            is_assign = re.search("assign", TokenType)
            always = re.search("always", TokenType)
            # print(NewToken)
            if is_assign:
                WriteTo, NewToken = self.prep_blocking(NewToken)
                self.Module_Node.add_assign(ContinuousAssignment(WriteTo, eval(NewToken), TokenLine, "Blocking"))
            elif always:
                NewToken = self.Token_obj_Replace(NewToken)
                self.Module_Node.add_always(eval(NewToken))
                print(NewToken)
            # for cont in self.Module_Node.continuous_assignment:
            #     self.observer.Register(cont)
            NewToken, TokenType, TokenLine = self.Token.get_token()
        return self.Module_Node


# l = Lexer("E:/EECE_2023_4thyear_1stterm/Siemens_Graduation_Project/COCOSCOPE/Example/SHIFT_UNIT.v")
# l.doLexing()
# v = VerilogParser("E:/EECE_2023_4thyear_1stterm/Siemens_Graduation_Project/COCOSCOPE/Example/SHIFT_UNIT.v")
# main_node = v.Parse()
# for cont in main_node.internal["current_state_2"].contributors:
#     print(cont.name)
# Generate all possible combinations of values for the inputs
# value_combinations = [range(2 ** input_obj.size) for input_obj in main_node.inputs.values()]
# combinations = list(itertools.product(*value_combinations))
#
# # Check that all combinations occur in the dictionary
# for combination in combinations:
#     for input_name, input_obj in main_node.inputs.items():
#         # Get the value for this input from the current combination
#         input_value = combination[list(main_node.inputs.keys()).index(input_name)]
#
#         # Check that the input value is valid
#         if not 0 <= input_value < 2 ** input_obj.size:
#             print(f"Invalid value {input_value} for input {input_name}")
#             break
#         # Set the input value in the dictionary
#         input_obj.value = input_value
#         # Check that the input value matches the value in the dictionary
#         if input_obj.value != input_value:
#             print(f"Value mismatch for {input_name} ({input_obj.value} != {input_value})")
#             break
#         else:
#             for inp in main_node.inputs:
#                 print(str(main_node.inputs[inp].name) + " with value " + str(main_node.inputs[inp].value))
# print(main_node.ALLFF)
# print(main_node.procedual_assignment[0].LHS)
# print(main_node.procedual_assignment[0].LHS_LINES)
# print(main_node.procedual_assignment[1].LHS)
# print(main_node.procedual_assignment[1].LHS_LINES)
# main_node.inputs["in1"].value = 1
# main_node.inputs["in2"].value = 5
# main_node.procedual_assignment[0].Allblocks[2].run_assignment()
# print(isinstance(main_node.procedual_assignment[0].Allblocks[3], ContinuousAssignment))
# for cont in main_node.procedual_assignment[0].Allblocks[2].contributors:
#     if isinstance(cont, SignalNode):
#         print(cont.name)
# print(main_node.outputs["out3"].value)
# print(main_node.internal["internOut"].size)
# print(main_node.internal["internOut"].value)
# main_node.continuous_assignment[0].run_assignment()
# for op in main_node.continuous_assignment[0].operations:
#     print(op)
# for cont in main_node.continuous_assignment[0].contributors:
#     if isinstance(cont, SignalNode):
#         print(cont.name)
#         print(cont.size)
# print(main_node.continuous_assignment[0].left.size)
# print(main_node.continuous_assignment[0].right.size)
