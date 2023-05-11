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
        if Tokens.allTokens:
            return Tokens.allTokens.pop(0), Tokens.allTokensType.pop(0), Tokens.allTokensLines.pop(0)
        else:
            return None, None, None


class Lexer:
    def __init__(self, file):
        self.old_lines = None
        self.current_line = 0
        self.file = file
        self.VerilogFile = open(self.file, "r")
        self.lines = self.VerilogFile.readlines()
        self.VerilogFile.close()
        self.Token = Tokens()
        self.assign_id = 0
        self.inputs, _, _, _, self.outputs, _, _, _, self.internals, _, _, _ = get_in_out_signal_names(file)
        self.AllParameters = getParameters(file)

    # the function  PrepTokenAssignment is responsible for reformating the information contains in any
    # assignment for example the input must be as ["out", "=", "in1","+","in2",";"] and
    # we can expect the output to be ["out","=", "ADD(in1, in2)",";""
    # it contains a list of all operations according to priority

    def PrepTokenAssignment(self, newToken: list):
        ALL_operations = ["*", "/", "+", "-", "<<", ">>", ">", ">=", "<", "<=", "==", "!=", "&", "^", "~^", "^~", "|",
                          "&&"]
        UniaryOP = ["!", "~", "&", "|", "~&", "~|", "^", "~^", "^~"]
        while "(" in newToken or ")" in newToken:
            first_index, last_index, new_list = get_paranthesis(newToken)
            new_list = self.PrepTokenAssignment(new_list)
            del newToken[first_index:last_index + 1]
            for add_index in range(len(new_list)):
                newToken.insert(first_index + add_index, new_list[add_index])
        for op in UniaryOP:
            flag = 1
            while flag:
                index_list = [i for i in range(len(newToken)) if newToken[i] == op]
                flag = 0
                for index in index_list:
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
                        elif op == "!":
                            Final_op = "LOGNEG(" + str(newToken[index + 1]) + ")"
                        del newToken[index]
                        del newToken[index]
                        newToken.insert(index, Final_op)
                        flag = 1
                        break
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
                        Final_op = "SUB(" + str(newToken[ind_op - 1]) + "," + str(
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
                    elif op == "<":
                        Final_op = "LessThan(" + str(newToken[ind_op - 1]) + "," + str(
                            newToken[ind_op + 1]) + ")"
                    elif op == "<=":
                        Final_op = "LessThanEqual(" + str(newToken[ind_op - 1]) + "," + str(
                            newToken[ind_op + 1]) + ")"
                    elif op == ">":
                        Final_op = "GreaterThan(" + str(newToken[ind_op - 1]) + "," + str(
                            newToken[ind_op + 1]) + ")"
                    elif op == ">=":
                        Final_op = "GreaterThanEqual(" + str(newToken[ind_op - 1]) + "," + str(
                            newToken[ind_op + 1]) + ")"
                    elif op == "==":
                        Final_op = "Equal(" + str(newToken[ind_op - 1]) + "," + str(
                            newToken[ind_op + 1]) + ")"
                    elif op == "!=":
                        Final_op = "NotEqual(" + str(newToken[ind_op - 1]) + "," + str(
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
                    elif op == "&&":
                        Final_op = "LAND(" + str(newToken[ind_op - 1]) + "," + str(
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
        line = re.sub("\n", "", line)
        line = re.sub(r"\t", "", line)
        matches = re.finditer("[1-9]*'(b|d|h)[0-9]*", line)
        strange_keywords = [r"=!", r"=\|", r"=&", r"=~", r"=\^"]
        strange_replace = ["=!", "=|", "=&", "=~", "=^"]
        for word, replace in zip(strange_keywords, strange_replace):
            line = re.sub(rf"{word}", replace[0] + " " + replace[1:len(word)], line)
        found = re.search(r"!([a-z]*|[A-Z]*)", line)
        if found:
            found = found.group()
            line = re.sub(found, found[0] + " " + found[1:len(found)], line)
        found = re.search(r"([a-z]*|[A-Z]*)!", line)
        if found:
            found = found.group()
            line = re.sub(found, found[0:len(found) - 1] + " " + found[-1], line)
        for match in matches:
            line = re.sub(match.group(), " " + match.group() + " ", line)
        for inp in self.inputs:
            line = re.sub(r"(?<!([a-z]|[A-Z]|_))" + inp + r"(?!([0-9]|_|[a-z]|[A-Z]))", " " + inp + " ", line)
        for out in self.outputs:
            line = re.sub(r"(?<!([a-z]|[A-Z]|_))" + out + r"(?!([0-9]|_|[a-z]|[A-Z]))", " " + out + " ", line)
        for internal in self.internals:
            line = re.sub(r"(?<!([a-z]|[A-Z]|_))" + internal + r"(?!([0-9]|_|[a-z]|[A-Z]))", " " + internal + " ", line)
        for param in self.AllParameters:
            line = re.sub(r"(?<!([a-z]|[A-Z]|_))" + param + r"(?!([0-9]|_|[a-z]|[A-Z]))",
                          " " + str(self.AllParameters[param]) + " ", line)
        newToken = line.split(" ")
        newToken = [x for x in newToken if x != '']
        for i in range(len(newToken)):
            if newToken[i].isdigit():
                newToken[i] = "'d" + newToken[i]
        if "!" in newToken:
            index = newToken.index("!")
            if newToken[index + 1] == "=":
                newToken[index] = "!="
                del newToken[index + 1]
        return newToken

    # define a function used to extract information from if conditions
    def if_lexer(self, newToken):
        mayBeNextline = 0
        MultiLine = 0
        line = self.lines[self.current_line - 1]
        start_line = self.get_line_position(self.lines[self.current_line - 1])
        # print(line)
        condition = re.search(r"if\s*\(.*\)", line).group()
        condition = re.sub(r"(?<!([a-z]|[A-Z]|_))" + r"if" + r"(?!([0-9]|_|[a-z]|[A-Z]))", "", condition)
        condition = self.prep_line(condition)
        condition = self.PrepTokenAssignment(condition)
        condition = condition[0]
        # print(condition)
        newToken = newToken + "IF(" + condition + "," + "["
        mayBeNextline = not re.search("begin", line)
        if mayBeNextline:
            line = self.lines[self.current_line]
            self.current_line += 1
            line = re.sub(r'//.*', '', line)
            line = re.sub(r"/\*.*", "", line)
            line = re.sub(r'\n', '', line)
            line = re.sub(r"\t", "", line)
            MultiLine = re.search("begin", line)
        else:
            MultiLine = True
        if not MultiLine:
            tempToken = self.prep_line(line)
            if "=" in tempToken:
                tempToken1 = tempToken[2:len(tempToken)]
                tempToken = tempToken[0:2]
                tempToken.append(self.PrepTokenAssignment(tempToken1)[0])
                newToken += "Blocking(" + str(tempToken[0]) + "," + str(
                    tempToken[2]) + "," + str(
                    self.get_line_position(self.lines[self.current_line - 1])) + "),"
                endline = self.get_line_position(self.lines[self.current_line - 1])
                line = self.lines[self.current_line]
                self.current_line += 1
                line = re.sub(r'//.*', '', line)
                line = re.sub(r"/\*.*", "", line)
                line = re.sub(r'\n', '', line)
                line = re.sub(r"\t", "", line)
            elif "<=" in tempToken and "=" not in tempToken:
                tempToken1 = tempToken[2:len(tempToken)]
                tempToken = tempToken[0:2]
                tempToken.append(self.PrepTokenAssignment(tempToken1)[0])
                newToken += "NonBlocking(" + str(tempToken[0]) + "," + str(
                    tempToken[2]) + "," + str(
                    self.get_line_position(self.lines[self.current_line - 1])) + "),"
                endline = self.get_line_position(self.lines[self.current_line - 1])
                line = self.lines[self.current_line]
                self.current_line += 1
                line = re.sub(r'//.*', '', line)
                line = re.sub(r"/\*.*", "", line)
                line = re.sub(r'\n', '', line)
                line = re.sub(r"\t", "", line)
        else:
            end = re.search("end", line)
            line = self.lines[self.current_line]
            self.current_line += 1
            while not end:
                if_cond = re.search("if\s*\(.*\)", line)
                case = re.search("case\s*\(.*\)", line)
                if if_cond:
                    newToken = self.if_lexer(newToken)
                    newToken += ","
                    line = self.lines[self.current_line - 1]
                    line = re.sub(r'//.*', '', line)
                    line = re.sub(r"/\*.*", "", line)
                    line = re.sub(r'\n', '', line)
                    line = re.sub(r"\t", "", line)
                elif case:
                    newToken = self.Case_lexing(newToken)
                    line = self.lines[self.current_line]
                    self.current_line += 1
                    line = re.sub(r'//.*', '', line)
                    line = re.sub(r"/\*.*", "", line)
                    line = re.sub(r'\n', '', line)
                    line = re.sub(r"\t", "", line)
                else:
                    tempToken = self.prep_line(line)
                    if "=" in tempToken:
                        tempToken1 = tempToken[2:len(tempToken)]
                        tempToken = tempToken[0:2]
                        tempToken.append(self.PrepTokenAssignment(tempToken1)[0])
                        newToken += "Blocking(" + str(tempToken[0]) + "," + str(
                            tempToken[2]) + "," + str(
                            self.get_line_position(self.lines[self.current_line - 1])) + "),"
                    elif "<=" in tempToken and "=" not in tempToken:
                        tempToken1 = tempToken[2:len(tempToken)]
                        tempToken = tempToken[0:2]
                        tempToken.append(self.PrepTokenAssignment(tempToken1)[0])
                        newToken += "NonBlocking(" + str(tempToken[0]) + "," + str(
                            tempToken[2]) + "," + str(
                            self.get_line_position(self.lines[self.current_line - 1])) + "),"
                    line = self.lines[self.current_line]
                    self.current_line += 1
                    line = re.sub(r'//.*', '', line)
                    line = re.sub(r"/\*.*", "", line)
                    line = re.sub(r'\n', '', line)
                    line = re.sub(r"\t", "", line)
                end = re.search("end", line)
                if end:
                    endline = self.get_line_position(self.lines[self.current_line - 1])
                    line = self.lines[self.current_line]
                    self.current_line += 1
                    line = re.sub(r'//.*', '', line)
                    line = re.sub(r"/\*.*", "", line)
                    line = re.sub(r'\n', '', line)
                    line = re.sub(r"\t", "", line)
        newToken = newToken[:-1]
        else_cond = re.search("else((\s)+|$)", line)
        else_if_cond = re.search("else\s+if\(.*\)", line)
        if else_if_cond:
            endline = self.get_line_position(self.lines[self.current_line - 1])
            newToken += "],["
            newToken = self.if_lexer(newToken)
        elif else_cond:
            newToken += "],["
            mayBeNextline = not re.search("begin", line)
            if mayBeNextline:
                line = self.lines[self.current_line]
                self.current_line += 1
                MultiLine = re.search("begin", line)
            else:
                MultiLine = True
            if not MultiLine:
                tempToken = self.prep_line(line)
                if "=" in tempToken:
                    tempToken1 = tempToken[2:len(tempToken)]
                    tempToken = tempToken[0:2]
                    tempToken.append(self.PrepTokenAssignment(tempToken1)[0])
                    newToken += "Blocking(" + str(tempToken[0]) + "," + str(
                        tempToken[2]) + "," + str(
                        self.get_line_position(self.lines[self.current_line - 1])) + "),"
                    endline = self.get_line_position(self.lines[self.current_line - 1])
                    line = self.lines[self.current_line]
                    self.current_line += 1
                    line = re.sub(r'//.*', '', line)
                    line = re.sub(r"/\*.*", "", line)
                    line = re.sub(r'\n', '', line)
                    line = re.sub(r"\t", "", line)
                elif "<=" in tempToken and "=" not in tempToken:
                    tempToken1 = tempToken[2:len(tempToken)]
                    tempToken = tempToken[0:2]
                    tempToken.append(self.PrepTokenAssignment(tempToken1)[0])
                    newToken += "NonBlocking(" + str(tempToken[0]) + "," + str(
                        tempToken[2]) + "," + str(
                        self.get_line_position(self.lines[self.current_line - 1])) + "),"
                    endline = self.get_line_position(self.lines[self.current_line - 1])
                    line = self.lines[self.current_line]
                    self.current_line += 1
                    line = re.sub(r'//.*', '', line)
                    line = re.sub(r"/\*.*", "", line)
                    line = re.sub(r'\n', '', line)
                    line = re.sub(r"\t", "", line)
                if newToken[-1] == ",":
                    newToken = newToken[:-1]
            else:
                end = re.search("end", line)
                line = self.lines[self.current_line]
                self.current_line += 1
                while not end:
                    if_cond = re.search("if\s*\(.*\)", line)
                    case = re.search("case\s*\(.*\)", line)
                    if if_cond:
                        newToken = self.if_lexer(newToken)
                        newToken += ","
                        line = self.lines[self.current_line - 1]
                        line = re.sub(r'//.*', '', line)
                        line = re.sub(r"/\*.*", "", line)
                        line = re.sub(r'\n', '', line)
                        line = re.sub(r"\t", "", line)
                    elif case:
                        newToken = self.Case_lexing(newToken)
                        line = self.lines[self.current_line]
                        self.current_line += 1
                        line = re.sub(r'//.*', '', line)
                        line = re.sub(r"/\*.*", "", line)
                        line = re.sub(r'\n', '', line)
                        line = re.sub(r"\t", "", line)
                    else:
                        tempToken = self.prep_line(line)
                        if "=" in tempToken:
                            tempToken1 = tempToken[2:len(tempToken)]
                            tempToken = tempToken[0:2]
                            tempToken.append(self.PrepTokenAssignment(tempToken1)[0])
                            newToken += "Blocking(" + str(tempToken[0]) + "," + str(
                                tempToken[2]) + "," + str(
                                self.get_line_position(self.lines[self.current_line - 1])) + "),"
                        elif "<=" in tempToken and "=" not in tempToken:
                            tempToken1 = tempToken[2:len(tempToken)]
                            tempToken = tempToken[0:2]
                            tempToken.append(self.PrepTokenAssignment(tempToken1)[0])
                            newToken += "NonBlocking(" + str(tempToken[0]) + "," + str(
                                tempToken[2]) + "," + str(
                                self.get_line_position(self.lines[self.current_line - 1])) + "),"
                        line = self.lines[self.current_line]
                        self.current_line += 1
                        line = re.sub(r'//.*', '', line)
                        line = re.sub(r"/\*.*", "", line)
                        line = re.sub(r'\n', '', line)
                        line = re.sub(r"\t", "", line)
                    end = re.search("end", line)
                    if end:
                        endline = self.get_line_position(self.lines[self.current_line - 1])
                        line = self.lines[self.current_line]
                        self.current_line += 1
                        line = re.sub(r'//.*', '', line)
                        line = re.sub(r"/\*.*", "", line)
                        line = re.sub(r'\n', '', line)
                        line = re.sub(r"\t", "", line)

                if newToken[-1] == ",":
                    newToken = newToken[:-1]
        else:
            if newToken[-1] == ",":
                newToken = newToken[:-1]
            newToken += "],["
            # line = self.lines[self.current_line]
            # self.current_line += 1
        newToken = newToken + "]" + "," + "[" + str(start_line) + "," + str(endline) + "]" + ")"
        return newToken

    def Case_lexing(self, newToken):
        line = self.lines[self.current_line - 1]
        start_line = self.get_line_position(self.lines[self.current_line - 1])
        case_statement = re.sub(r"(?<!([a-z]|[A-Z]|_))" + r"case" + r"(?!([0-9]|_|[a-z]|[A-Z]))", "", line)
        case_statement = re.sub(r"(\(|\)|\s|\t)", "", case_statement)
        case_statement = self.prep_line(case_statement)
        case_statement = self.PrepTokenAssignment(case_statement)[0]
        EndCase = 0
        first_time = 1
        lineToken = ""
        list_items = []
        Non_parallel = 0
        newToken += "CASE(" + case_statement + ","
        while True:
            line = self.lines[self.current_line]
            self.current_line += 1
            case_item = re.search(r"(?<!(\[))" + r".*:", line)
            EndCase = re.search("endcase", line)
            if EndCase:
                if newToken[-1] == ",":
                    newToken = newToken[:-1]
                if lineToken[-1] == ",":
                    lineToken = lineToken[:-1]
                    lineToken += "}"

                line_list_str = "[" + str(start_line) + "," + str(
                    self.get_line_position(self.lines[self.current_line - 1])) + "]"
                newToken += "}," + lineToken + "," + line_list_str + "," + str(Non_parallel) + "),"
                return newToken
            if case_item:
                case_item = case_item.group()
                case_item = re.sub("(:|\s|\t)", "", case_item)
                search_num = re.search(r"[1-9]*'(d|b|h)[0-9]*", case_item)
                if case_item == "default":
                    case_item = "\"default\""
                else:
                    if search_num:
                        constant_str = search_num.group()
                        cons_type = re.search(r"'(d|b|h)", constant_str).group()
                        constant = re.sub(r"[1-9]*'(b|d|h)", "", constant_str)
                        if cons_type == "'b":
                            constant = int(constant, 2)
                        elif cons_type == "'h":
                            constant = int(constant, 16)
                        else:
                            constant = int(constant, 10)
                        case_item = re.sub(r"(?<!([1-9]))" + constant_str + r"(?!([0-9]|_))",
                                           str(constant), case_item)
                    for param in self.AllParameters:
                        if param == case_item:
                            case_item = self.AllParameters[param]
                if case_item in list_items:
                    Non_parallel = 1
                else:
                    list_items.append(case_item)
                if first_time:
                    newToken += "{" + str(case_item) + ":" + "["
                    lineToken += "{" + str(case_item) + ":" + "[" + str(
                        self.get_line_position(self.lines[self.current_line - 1])) + ","
                    first_time = 0
                else:
                    newToken += str(case_item) + ":" + "["
                    lineToken += str(case_item) + ":" + "[" + str(
                        self.get_line_position(self.lines[self.current_line - 1])) + ","
                line = re.sub(".*:", "", line)
                found = re.search("(=|<=)", line)
                if found:
                    MultiLine = False
                else:
                    mayBeNextline = not re.search("begin", line)
                    if mayBeNextline:
                        line = self.lines[self.current_line]
                        self.current_line += 1
                        MultiLine = re.search("begin", line)
                    else:
                        MultiLine = True
                if not MultiLine:
                    tempToken = self.prep_line(line)
                    if "=" in tempToken:
                        tempToken1 = tempToken[2:len(tempToken)]
                        tempToken = tempToken[0:2]
                        tempToken.append(self.PrepTokenAssignment(tempToken1)[0])
                        newToken += "Blocking(" + str(tempToken[0]) + "," + str(
                            tempToken[2]) + "," + str(self.get_line_position(self.lines[self.current_line - 1])) + "),"
                        endline = self.get_line_position(self.lines[self.current_line - 1])
                    elif "<=" in tempToken and "=" not in tempToken:
                        tempToken1 = tempToken[2:len(tempToken)]
                        tempToken = tempToken[0:2]
                        tempToken.append(self.PrepTokenAssignment(tempToken1)[0])
                        newToken += "NonBlocking(" + str(tempToken[0]) + "," + str(
                            tempToken[2]) + "," + str(self.get_line_position(self.lines[self.current_line - 1])) + "),"
                        endline = self.get_line_position(self.lines[self.current_line - 1])
                    if newToken[-1] == ",":
                        newToken = newToken[:-1]
                else:
                    end = re.search("end", line)
                    line = self.lines[self.current_line]
                    self.current_line += 1
                    while not end:
                        if_cond = re.search("if\s*\(.*\)", line)
                        if if_cond:
                            newToken = self.if_lexer(newToken)
                            newToken += ","
                            line = self.lines[self.current_line - 1]
                            line = re.sub(r'//.*', '', line)
                            line = re.sub(r"/\*.*", "", line)
                            line = re.sub(r'\n', '', line)
                            line = re.sub(r"\t", "", line)
                        else:
                            tempToken = self.prep_line(line)
                            if "=" in tempToken:
                                tempToken1 = tempToken[2:len(tempToken)]
                                tempToken = tempToken[0:2]
                                tempToken.append(self.PrepTokenAssignment(tempToken1)[0])
                                newToken += "Blocking(" + str(tempToken[0]) + "," + str(
                                    tempToken[2]) + "," + str(
                                    self.get_line_position(self.lines[self.current_line - 1])) + "),"
                            elif "<=" in tempToken and "=" not in tempToken:
                                tempToken1 = tempToken[2:len(tempToken)]
                                tempToken = tempToken[0:2]
                                tempToken.append(self.PrepTokenAssignment(tempToken1)[0])
                                newToken += "NonBlocking(" + str(tempToken[0]) + "," + str(
                                    tempToken[2]) + "," + str(
                                    self.get_line_position(self.lines[self.current_line - 1])) + "),"
                            line = self.lines[self.current_line]
                            self.current_line += 1
                            line = re.sub(r'//.*', '', line)
                            line = re.sub(r"/\*.*", "", line)
                            line = re.sub(r'\n', '', line)
                            line = re.sub(r"\t", "", line)
                        end = re.search("end", line)
                        if end:
                            endline = self.get_line_position(self.lines[self.current_line - 1])
                if newToken[-1] == ",":
                    newToken = newToken[:-1]
                newToken += "],"
                lineToken += str(endline) + "],"
                # print(newToken)

    def get_line_position(self, line):
        possible_lines = [i + 1 for i in range(len(self.old_lines)) if self.old_lines[i] == line]
        if len(possible_lines) == 1:
            return possible_lines[0]
        else:
            actual_lines = [i + 1 for i in range(len(self.lines)) if self.lines[i] == line]
            j = actual_lines.index(self.current_line)
            return possible_lines[j]

    def doLexing(self):
        always_cont = 0
        pattern = re.compile(r'^\s*$')
        self.old_lines = self.lines
        self.lines = [line for line in self.lines if not pattern.match(line)]
        while self.current_line < len(self.lines):
            line = self.lines[self.current_line]
            self.current_line += 1
            line = re.sub("\n", "", line)
            line = re.sub(r"\t", "", line)
            line = re.sub("(//|/\*).*", "", line)
            assign = re.search("assign\s+", line)
            always = re.search(r"always\s*@\s*\(.+\)", line)
            if assign:
                newToken = ""
                self.assign_id += 1
                newToken = self.prep_line(line)
                newToken.remove("assign")
                self.PrepTokenAssignment(newToken)
                print(newToken)
                self.Token.insert_token(newToken, "assign " + str(self.assign_id),
                                        self.get_line_position(self.lines[self.current_line - 1]))
            elif always or always_cont:
                end = re.search("end", line)
                if_cond = re.search(r"if\s*\(.*\)", line)
                case = re.search(r"case", line)
                if end:
                    always_cont = 0
                    if newToken[-1] == ",":
                        newToken = newToken[:-1]
                    newToken += "],[" + str(start_line) + "," + str(
                        self.get_line_position(self.lines[self.current_line - 1])) + "])"
                    self.Token.insert_token(newToken, "always",
                                            [start_line, self.get_line_position(self.lines[self.current_line - 1])])
                    print(newToken)
                elif case:
                    newToken = self.Case_lexing(newToken)
                elif if_cond:
                    newToken = self.if_lexer(newToken)
                    newToken += ","
                    self.current_line -= 1
                elif always:
                    newToken = ""
                    start_line = self.get_line_position(self.lines[self.current_line - 1])
                    always_cont = 1
                    Sensitivity_list = re.sub(r"(always|@|\(|\)|begin)", "", line)
                    Sensitivity_list = Sensitivity_list.split(" ")
                    Sensitivity_list = [x for x in Sensitivity_list if x != '']
                    newToken = "Always({"
                    skip_next = 0
                    for element in range(len(Sensitivity_list)):
                        if skip_next:
                            skip_next = 0
                            continue
                        elif Sensitivity_list[element] == "*":
                            newToken += "\"*\":\"*\"}"
                        elif Sensitivity_list[element] == "posedge" or Sensitivity_list[element] == "negedge":
                            newToken += Sensitivity_list[element + 1] + ":\"" + Sensitivity_list[element] + "\","
                            skip_next = 1
                        elif Sensitivity_list[element] == "or":
                            continue
                        else:
                            newToken += Sensitivity_list[element] + ":\"*\"" + ","

                    if newToken[-1] == ",":
                        newToken = newToken[:-1]
                        newToken += "}"
                    newToken += ",["
                elif always_cont:
                    tempToken = self.prep_line(line)
                    Blocking = ("=" in tempToken)
                    NonBlocking = ("<=" in tempToken)
                    if Blocking or NonBlocking:
                        tempToken = self.prep_line(line)
                        tempToken1 = tempToken[2:len(tempToken)]
                        tempToken = tempToken[0:2]
                        tempToken.append(self.PrepTokenAssignment(tempToken1)[0])
                    if Blocking:
                        newToken += "Blocking(" + str(tempToken[0]) + "," + str(
                            tempToken[2]) + "," + str(self.get_line_position(self.lines[self.current_line - 1])) + "),"
                    elif NonBlocking and not Blocking:
                        newToken += "NonBlocking(" + str(tempToken[0]) + "," + str(
                            tempToken[2]) + "," + str(self.get_line_position(self.lines[self.current_line - 1])) + "),"
