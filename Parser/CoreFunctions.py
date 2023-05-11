import re
import string
from functools import reduce
from typing import Tuple, List, Any


def get_in_out_signal_names(file: str) -> tuple[
    list[str], list[str], list[int | Any], list[int], list[str], list[str], list[int | Any], list[int], list[str], list[
        str], list[int | Any], list[int]]:
    input_signals = []
    inputs_types = []
    input_size = []
    input_lines = []
    output_signals = []
    output_types = []
    output_size = []
    output_lines = []
    internal_signals = []
    internal_types = []
    internal_size = []
    internal_lines = []
    Parameters_dic = getParameters(file)
    current_line_num = 0
    with open(file, 'r') as f:
        for line in f:
            current_line_num += 1
            line = re.sub(r'//.*', '', line)
            line = re.sub(r'\n', '', line)
            line = re.sub(r"\t", " ", line)
            matches_input = re.search("input\s+", line)
            matches_output = re.search("output\s+", line)
            matches_internal = re.search(r"(?<!([a-z]|[A-Z]|_))" + "(wire|logic|reg)\s+" + r"(?!([0-9]|_))", line)
            if matches_input or matches_output or matches_internal:
                names = re.sub(r"(?<!([a-z]|[A-Z]|_))" + "(wire|logic|reg)\s+" + r"(?!([0-9]|_))", "", line)
                names = re.sub(" ", "", names)
                names = re.sub(";", "", names)
                names = re.sub("[\(\[].*?[\)\]]", "", names)
                names = re.sub(r"(?<!([a-z]|[A-Z]|_))" + "(wire|logic|reg|input|output)" + r"(?!([0-9]|_))", "", names)
                names = names.split(",")
                names = [x for x in names if x != ',']
                names = [x for x in names if x != '']
                Sig_type = re.search("(wire|logic|reg|bit)", line)
                if Sig_type is None:
                    Sig_type = "wire"
                else:
                    Sig_type = Sig_type.group()
                Sig_size = re.search("\[.+\]", line)
                if Sig_size is None:
                    Sig_size = 1
                else:
                    Sig_size = Sig_size.group()
                    Sig_size = re.sub("(\[|\]|\s)", "", Sig_size)
                    for key in Parameters_dic:
                        key_found = re.search(key, Sig_size)
                        if key_found:
                            Sig_size = re.sub(key, str(Parameters_dic[key]), Sig_size)
                    Sig_size = Sig_size.split(":")
                    Sig_size = eval(Sig_size[0]) - eval(Sig_size[1]) + 1
            if matches_internal and not (matches_input or matches_output):
                for element in names:
                    internal_signals.append(element)
                    internal_types.append(Sig_type)
                    internal_size.append(Sig_size)
                    internal_lines.append(current_line_num)
            elif matches_input:
                for element in names:
                    input_signals.append(element)
                    inputs_types.append(Sig_type)
                    input_size.append(Sig_size)
                    input_lines.append(current_line_num)
            elif matches_output:
                for element in names:
                    output_signals.append(element)
                    output_types.append(Sig_type)
                    output_size.append(Sig_size)
                    output_lines.append(current_line_num)
    return input_signals, inputs_types, input_size, input_lines, output_signals, output_types, output_size, output_lines, internal_signals, internal_types, internal_size, internal_lines


def getParameters(file: str) -> dict:
    Parameters_dic = {}
    notdone = 0
    with open(file, 'r') as f:
        for line in f:
            line = re.sub(r'//.*', '', line)
            line = re.sub(r'\n', '', line)
            line = re.sub(r"\t", " ", line)
            parametersfound = re.search("(parameter|localparam)\s+", line)
            line = re.sub("(\s|\t)", "", line)
            if parametersfound or notdone:
                semicolon = re.search(";", line)
                hash = re.search("(#|module)", line)
                coma = re.search(",", line)
                if not semicolon and not hash and coma:
                    notdone = 1
                else:
                    notdone = 0
                    line = re.sub(";", "", line)
                parameters = re.sub(r"(module|\(|#)", "", line)
                parameters = re.sub(r"(\(|\)|\[.*\])", "", parameters)
                parameters = re.sub(r"(parameter|localparam)", "", parameters)
                parameters = parameters.split(",")
                parameters = [x for x in parameters if x != ',']
                parameters = [x for x in parameters if x != '']
                for parameter in parameters:
                    parameter = parameter.split("=")
                    parameter = [x for x in parameter if x != '=']
                    parameter[0] = re.sub(" ", "", parameter[0])
                    parameter[1] = re.sub(" ", "", parameter[1])
                    cons_type = re.search(r"'(d|b|h)", parameter[1])
                    if not cons_type:
                        parameter[1] = "'d" + parameter[1]
                        cons_type = re.search(r"'(d|b|h)", parameter[1])
                    cons_type = cons_type.group()
                    parameter[1] = re.sub(r"[1-9]*'(b|d|h)", "", parameter[1])
                    if cons_type == "'b":
                        parameter[1] = int(parameter[1], 2)
                    elif cons_type == "'h":
                        parameter[1] = int(parameter[1], 16)
                    else:
                        parameter[1] = int(parameter[1], 10)
                    Parameters_dic[parameter[0]] = int(parameter[1])
                # if not coma:
                #     break
    return Parameters_dic


def get_paranthesis(Token_list: list):
    elements_between = []
    first_index = [i for i, x in enumerate(Token_list) if x == "("]
    first_index = first_index[-1]
    for index in range(len(Token_list)):
        if index > first_index:
            if Token_list[index] == ")":
                last_index = index
                break

    for index in range(len(Token_list)):
        if first_index < index < last_index:
            elements_between.append(Token_list[index])
    return first_index, last_index, elements_between


def get_Module_Name(File: str) -> str:
    with open(File, 'r') as f:
        for line in f:
            pattern = re.compile(r'^.*module\s')
            matches = pattern.finditer(line)
            for match in matches:
                line = re.sub("[\(\[].*?[\)\]]", "", line)
                line = re.sub("[#(]", "", line)
                line = re.sub("module", "", line)
                line = line.replace(' ', '')
                line = line.replace('\n', '')
                return line
    print("File NOT found")
    return 0


def swap(a, b):
    temp = a
    a = b
    b = temp


def xnor(a, b):
    # Make sure a is larger
    if a < b:
        swap(a, b)

    if a == 0 and b == 0:
        return 1;

    # for last bit of a
    a_rem = 0

    # for last bit of b
    b_rem = 0

    # counter for count bit and
    #  set bit in xnor num
    count = 0

    # for make new xnor number
    xnornum = 0

    # for set bits in new xnor
    # number
    while a != 0:

        # get last bit of a
        a_rem = a & 1

        # get last bit of b
        b_rem = b & 1

        # Check if current two
        # bits are same
        if a_rem == b_rem:
            xnornum |= (1 << count)

        # counter for count bit
        count = count + 1

        a = a >> 1
        b = b >> 1

    return xnornum


def ReductionAnd(inp):
    inp_bin = format(inp, "b")
    # Break string into list of integers
    binary_list = [int(x) for x in inp_bin]
    # Perform bitwise AND reduction on list
    result = reduce(lambda x, y: x & y, binary_list)
    return result


def ReductionOr(inp):
    inp_bin = format(inp, "b")
    # Break string into list of integers
    binary_list = [int(x) for x in inp_bin]
    # Perform bitwise AND reduction on list
    result = reduce(lambda x, y: x | y, binary_list)
    return result


def ReductionXor(inp):
    inp_bin = format(inp, "b")
    # Break string into list of integers
    binary_list = [int(x) for x in inp_bin]
    # Perform bitwise AND reduction on list
    result = reduce(lambda x, y: x ^ y, binary_list)
    return result


def not_gate(a, size):
    binary_a = bin(a)[2:].zfill(size)  # Convert decimal input to binary string
    not_a = int(''.join(['1' if bit == '0' else '0' for bit in binary_a]), 2)
    return not_a


def SpaceNum(line: str):
    new_string = ""
    sequence_start = 0
    alpha = string.ascii_lowercase + string.ascii_uppercase

    for i in range(len(line)):
        if sequence_start:
            if not line[i].isdigit():
                sequence_start = 0
                new_string += " " + line[i]
            else:
                new_string += line[i]

        elif line[i].isdigit() and line[i] == line[-1]:
            if line[i - 1] not in alpha and line[i - 1] != "_" and not line[i - 1].isdigit():
                new_string += " " + line[i]
            else:
                new_string += line[i]
        elif line[i].isdigit() and (
                line[i + 1] != "'" and line[i - 1] not in alpha and line[i - 1] != "_" and not line[i - 1].isdigit()):
            new_string += " " + line[i]
            sequence_start = 1

        else:
            new_string += line[i]
    return new_string
