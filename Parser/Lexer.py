import re
from source.Parser.CoreFunctions import *

"""
this file is responsible for the lexer but what is the importance of the lexer
the lexer is used to prepare the data so that the parser can understand and 
send create the AST
"""


class Tokens:
    allTokens = []
    allTokensType = []
    allTokensLines = []

    def insert_token(self, token, type, line):
        Tokens.allTokens.append(token)
        Tokens.allTokensType.append(type)
        Tokens.allTokensLines.append(line)

    def get_token(self):
        return Tokens.allTokens.pop(0), Tokens.allTokensType.pop(0), Tokens.allTokensLines.pop(0)


class Lexer:
    def __init__(self, file):
        self.current_line = 0
        self.file = file
        self.Token = Tokens()
        self.assign_id = 0
        self.inputs, _, _, self.outputs, _, _ = get_in_out_signal_names(file)

    # the function  PrepTokenAssignment is responsible for reformating the information contains in any
    # assignment for example the input must be as ["out", "=", "in1","+","in2",";"] and
    # we can expect the output to be ["out","=", "ADD(in1, in2)",";""
    # it contains a list of all operations according to priority

    def PrepTokenAssignment(self, newToken: list):
        ALL_operations = ["*", "/", "+", "-", "<<", ">>", "&", "^", "~^", "^~", "|"]
        UniaryOP = ["~", "&", "|", "~&", "~|", "^", "~^", "^~"]
        while "(" in newToken or ")" in newToken:
            first_index, last_index, new_list = get_paranthesis(newToken)
            new_list = self.PrepTokenAssignment(new_list)
            del newToken[first_index:last_index + 1]
            for add_index in range(len(new_list)):
                newToken.insert(first_index + add_index, new_list[add_index])
        for op in UniaryOP:
            uind_op = [i for i, x in enumerate(newToken) if x == op]
            for index in uind_op:
                if index == 0 or (newToken[index - 1] in ALL_operations or newToken[index - 1] == "=" or newToken[
                    index - 1] == "<="):
                    if op == "~":
                        Final_op = "NOT(" + str(newToken[index + 1]) + ")"
                    elif op == "&":
                        Final_op = "RAND(" + str(newToken[index + 1]) + ")"
                    elif op == "~&":
                        Final_op = "RNAND(" + str(newToken[index + 1]) + ")"
                    elif op == "^":
                        Final_op = "RXOR(" + str(newToken[index + 1]) + ")"
                    elif op == "~^" or op == "^~":
                        Final_op = "RXNR(" + str(newToken[index + 1]) + ")"
                    elif op == "|":
                        Final_op = "ROR(" + str(newToken[index + 1]) + ")"
                    elif op == "~|":
                        Final_op = "RNOR(" + str(newToken[index + 1]) + ")"
                    del newToken[index]
                    del newToken[index]
                    newToken.insert(index, Final_op)
        for op in ALL_operations:
            while op in newToken:
                ind_op = newToken.index(op)
                if ind_op != 0 and newToken[ind_op - 1] not in ALL_operations and newToken[ind_op - 1] != "=" and \
                        newToken[ind_op - 1] != "<=":
                    if op == "*":
                        Final_op = "MUL(" + str(newToken[ind_op - 1]) + "," + str(
                            newToken[ind_op + 1]) + ")"
                    elif op == "/":
                        Final_op = "DIV(" + str(newToken[ind_op - 1]) + "," + str(
                            newToken[ind_op + 1]) + ")"
                    elif op == "+":
                        Final_op = "ADD(" + str(newToken[ind_op - 1]) + "," + str(
                            newToken[ind_op + 1]) + ")"
                    elif op == "-":
                        Final_op = "Sub(" + str(newToken[ind_op - 1]) + "," + str(
                            newToken[ind_op + 1]) + ")"
                    elif op == "<<":
                        Final_op = "ShiftLeft(" + str(newToken[ind_op - 1]) + "," + str(
                            newToken[ind_op + 1]) + ")"
                    elif op == ">>":
                        Final_op = "ShiftRight(" + str(newToken[ind_op - 1]) + "," + str(
                            newToken[ind_op + 1]) + ")"
                    elif op == "&":
                        Final_op = "AND(" + str(newToken[ind_op - 1]) + "," + str(
                            newToken[ind_op + 1]) + ")"
                    elif op == "^":
                        Final_op = "XOR(" + str(newToken[ind_op - 1]) + "," + str(
                            newToken[ind_op + 1]) + ")"
                    elif op == "~^" or op == "^~":
                        Final_op = "XNR(" + str(newToken[ind_op - 1]) + "," + str(
                            newToken[ind_op + 1]) + ")"
                    elif op == "|":
                        Final_op = "BOR(" + str(newToken[ind_op - 1]) + "," + str(
                            newToken[ind_op + 1]) + ")"
                    del newToken[ind_op - 1]
                    del newToken[ind_op - 1]
                    del newToken[ind_op - 1]
                    newToken.insert(ind_op - 1, Final_op)
        return newToken

    # this function prepares an assignment block into the list mentioned aboved
    # to be able to be parsed into the previous function
    def prep_line(self, line) -> list:
        line = SpaceNum(line)
        line = re.sub("\(", " ( ", line)
        line = re.sub("\)", " ) ", line)
        matches = re.finditer("[1-9]*'(b|d|h)[0-9]*", line)
        for match in matches:
            line = re.sub(match.group(), " " + match.group() + " ", line)
        for inp in self.inputs:
            line = re.sub(inp, " " + inp + " ", line)
        for out in self.outputs:
            line = re.sub(out, " " + out + " ", line)
        newToken = line.split(" ")
        newToken = [x for x in newToken if x != '']
        return newToken

    def doLexing(self):
        always_cont = 0
        with open(self.file, "r") as readVerilog:
            for line in readVerilog:
                self.current_line += 1
                line = re.sub("\n", "", line)
                assign = re.search("assign\s+", line)
                always = re.search(r"always@\(.+\)", line)
                if assign:
                    newToken = ""
                    self.assign_id += 1
                    newToken = self.prep_line(line)
                    newToken.remove("assign")
                    self.PrepTokenAssignment(newToken)
                    self.Token.insert_token(newToken, "assign " + str(self.assign_id), self.current_line)
                elif always or always_cont:
                    end = re.search("end", line)
                    if end:
                        always_cont = 0
                        newToken = newToken[:-1]
                        newToken += "])"
                        self.Token.insert_token(newToken, "always", [start_line, self.current_line])
                        print(newToken)
                    elif always:
                        newToken = ""
                        start_line = self.current_line
                        always_cont = 1
                        Sensitivity_list = re.sub(r"(always@|\(|\)|begin)", "", line)
                        Sensitivity_list = Sensitivity_list.split(" ")
                        Sensitivity_list = [x for x in Sensitivity_list if x != '']
                        newToken = "always(\""
                        for element in range(len(Sensitivity_list)):
                            if Sensitivity_list[element] == Sensitivity_list[-1]:
                                newToken += Sensitivity_list[element]
                            else:
                                newToken += Sensitivity_list[element] + " "
                        newToken += "\",["
                    elif always_cont:
                        Blocking = re.search("=", line)
                        NonBlocking = re.search("<=", line)
                        if Blocking or NonBlocking:
                            tempToken = self.prep_line(line)
                            print(tempToken)
                            tempToken = self.PrepTokenAssignment(tempToken)
                        if Blocking and not NonBlocking:
                            newToken += "ContinuousAssignment(" + str(tempToken[0]) + "," + str(
                                tempToken[2]) + "," + str(self.current_line) + "),"
