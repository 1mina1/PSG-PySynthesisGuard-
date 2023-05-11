from source.Parser.CoreFunctions import *
import random

"""
this file contains the base class for all the required nodes by the
parser
"""


class ContinuousAssignment:
    def __init__(self, left, right, lineNum, Asstype):
        self.accept_cond = None
        self.left = left
        self.right = right
        self.line = lineNum
        self.contributors = []
        self.operations = []
        self.type = Asstype
        self.left_nBits = (1 << self.left.size) - 1
        self.get_contributors(self.right)
        self.contributors = list(set(self.contributors))
        self.operations.reverse()
        self.left.add_parent(self)

    def get_contributors(self, objsearch):
        if isinstance(objsearch, UnaryOperations):
            self.operations.append("Reduction " + objsearch.type)
            self.get_contributors(objsearch.operand)
        elif isinstance(objsearch, BaseOperations):
            self.operations.append(objsearch.type)
            self.get_contributors(objsearch.right)
            self.get_contributors(objsearch.left)
        else:
            self.contributors.append(objsearch)

    def run_assignment(self):
        if self.right.value != "x":
            self.left.value = self.right.value & self.left_nBits
        else:
            self.left.value = "x"


class ProcedualAssignment:
    def __init__(self, sensitivity_list, blocks, Start_end_list):
        self.sensitivity_list = sensitivity_list
        self.Allblocks = blocks
        self.start_line = Start_end_list[0]
        self.end_line = Start_end_list[1]
        self.LHS = []
        self.LHSOUTSIDE = []
        self.LHS_LINES = []
        self.LHSOUTSIDE_LINES = []
        self.get_all_LHS(self)

    def get_all_LHS(self, ObjectRecursive):
        if isinstance(ObjectRecursive, ProcedualAssignment):
            for statement in ObjectRecursive.Allblocks:
                if isinstance(statement, ContinuousAssignment):
                    if statement.left.name in self.LHS:
                        index = self.LHS.index(statement.left.name)
                        self.LHS_LINES[index].append(statement.line)

                    else:
                        self.LHS.append(statement.left.name)
                        self.LHS_LINES.append([statement.line])
                        self.LHSOUTSIDE.append(statement.left.name)
                        self.LHSOUTSIDE_LINES.append([statement.line])
                    if statement.left.name in self.LHSOUTSIDE:
                        index = self.LHSOUTSIDE.index(statement.left.name)
                        self.LHSOUTSIDE_LINES[index].append(statement.line)
                    else:
                        self.LHSOUTSIDE.append(statement.left.name)
                        self.LHSOUTSIDE_LINES.append([statement.line])
                elif isinstance(statement, IfCondition):
                    self.get_all_LHS(statement)
                elif isinstance(statement, CaseStatement):
                    self.get_all_LHS(statement)
        elif isinstance(ObjectRecursive, IfCondition):
            for statement in ObjectRecursive.TrueStatements:
                if isinstance(statement, ContinuousAssignment):
                    if statement.left.name in self.LHS:
                        index = self.LHS.index(statement.left.name)
                        self.LHS_LINES[index].append(statement.line)
                    else:
                        self.LHS.append(statement.left.name)
                        self.LHS_LINES.append([statement.line])
                elif isinstance(statement, IfCondition):
                    self.get_all_LHS(statement)
                elif isinstance(statement, CaseStatement):
                    self.get_all_LHS(statement)
            for statement in ObjectRecursive.FalseStatements:
                if isinstance(statement, ContinuousAssignment):
                    if statement.left.name in self.LHS:
                        index = self.LHS.index(statement.left.name)
                        self.LHS_LINES[index].append(statement.line)
                    else:
                        self.LHS.append(statement.left.name)
                        self.LHS_LINES.append([statement.line])
                elif isinstance(statement, IfCondition):
                    self.get_all_LHS(statement)
                elif isinstance(statement, CaseStatement):
                    self.get_all_LHS(statement)
        elif isinstance(ObjectRecursive, CaseStatement):
            for key in ObjectRecursive.items:
                statements = ObjectRecursive.items[key]
                for statement in statements:
                    if isinstance(statement, ContinuousAssignment):
                        if statement.left.name in self.LHS:
                            index = self.LHS.index(statement.left.name)
                            self.LHS_LINES[index].append(statement.line)
                        else:
                            self.LHS.append(statement.left.name)
                            self.LHS_LINES.append([statement.line])
                    elif isinstance(statement, IfCondition):
                        self.get_all_LHS(statement)
                    elif isinstance(statement, CaseStatement):
                        self.get_all_LHS(statement)


class IfCondition:
    def __init__(self, cond, TrueStatements, FalseStatements, lines):
        self.condition = cond
        self.TrueStatements = TrueStatements
        self.FalseStatements = FalseStatements
        self.start_line = lines[0]
        self.stop_line = lines[1]
        self.current_statements = []
        self.TRUE_LHS = []
        self.TRUEOUTSIDE_LHS = []
        self.TRUEOUTSIDE_LHS_LINES = []
        self.TRUE_LHS_LINES = []
        self.FALSEOUTSIDE_LHS = []
        self.FALSEOUTSIDE_LHS_LINES = []
        self.FALSE_LHS = []
        self.FALSE_LHS_LINES = []
        self.condition_contributors = []
        self.get_contributors(self.condition)
        self.get_TRUE_LHS(self)
        self.get_FALSE_LHS(self)

    def get_TRUE_LHS(self, ObjectRecursive):
        if ObjectRecursive == self:
            for statement in ObjectRecursive.TrueStatements:
                if isinstance(statement, ContinuousAssignment):
                    if statement.left.name in self.TRUE_LHS:
                        index = self.TRUE_LHS.index(statement.left.name)
                        self.TRUE_LHS_LINES[index].append(statement.line)
                    else:
                        self.TRUE_LHS.append(statement.left.name)
                        self.TRUE_LHS_LINES.append([statement.line])
                    if statement.left.name in self.TRUEOUTSIDE_LHS:
                        index = self.TRUEOUTSIDE_LHS.index(statement.left.name)
                        self.TRUEOUTSIDE_LHS_LINES[index].append(statement.line)
                    else:
                        self.TRUEOUTSIDE_LHS.append(statement.left.name)
                        self.TRUEOUTSIDE_LHS_LINES.append([statement.line])
                elif isinstance(statement, IfCondition):
                    self.get_TRUE_LHS(statement)
                elif isinstance(statement, CaseStatement):
                    self.get_TRUE_LHS(statement)
        elif isinstance(ObjectRecursive, IfCondition):
            for statement in ObjectRecursive.TrueStatements:
                if isinstance(statement, ContinuousAssignment):
                    if statement.left.name in self.TRUE_LHS:
                        index = self.TRUE_LHS.index(statement.left.name)
                        self.TRUE_LHS_LINES[index].append(statement.line)
                    else:
                        self.TRUE_LHS.append(statement.left.name)
                        self.TRUE_LHS_LINES.append([statement.line])
                elif isinstance(statement, IfCondition):
                    self.get_TRUE_LHS(statement)
                elif isinstance(statement, CaseStatement):
                    self.get_TRUE_LHS(statement)
            for statement in ObjectRecursive.FalseStatements:
                if isinstance(statement, ContinuousAssignment):
                    if statement.left.name in self.TRUE_LHS:
                        index = self.TRUE_LHS.index(statement.left.name)
                        self.TRUE_LHS_LINES[index].append(statement.line)
                    else:
                        self.TRUE_LHS.append(statement.left.name)
                        self.TRUE_LHS_LINES.append([statement.line])
                elif isinstance(statement, IfCondition):
                    self.get_TRUE_LHS(statement)
                elif isinstance(statement, CaseStatement):
                    self.get_TRUE_LHS(statement)
        elif isinstance(ObjectRecursive, CaseStatement):
            for key in ObjectRecursive.items:
                statements = ObjectRecursive.items[key]
                for statement in statements:
                    if isinstance(statement, ContinuousAssignment):
                        if statement.left.name in self.TRUE_LHS:
                            index = self.TRUE_LHS.index(statement.left.name)
                            self.TRUE_LHS_LINES[index].append(statement.line)
                        else:
                            self.TRUE_LHS.append(statement.left.name)
                            self.TRUE_LHS_LINES.append([statement.line])
                    elif isinstance(statement, IfCondition):
                        self.get_TRUE_LHS(statement)
                    elif isinstance(statement, CaseStatement):
                        self.get_TRUE_LHS(statement)

    def get_FALSE_LHS(self, ObjectRecursive):
        if ObjectRecursive == self:
            for statement in ObjectRecursive.FalseStatements:
                if isinstance(statement, ContinuousAssignment):
                    if statement.left.name in self.FALSE_LHS:
                        index = self.FALSE_LHS.index(statement.left.name)
                        self.FALSE_LHS_LINES[index].append(statement.line)
                    else:
                        self.FALSE_LHS.append(statement.left.name)
                        self.FALSE_LHS_LINES.append([statement.line])
                    if statement.left.name in self.FALSEOUTSIDE_LHS:
                        index = self.FALSEOUTSIDE_LHS.index(statement.left.name)
                        self.FALSEOUTSIDE_LHS_LINES[index].append(statement.line)
                    else:
                        self.FALSEOUTSIDE_LHS.append(statement.left.name)
                        self.FALSEOUTSIDE_LHS_LINES.append([statement.line])
                elif isinstance(statement, IfCondition):
                    self.get_FALSE_LHS(statement)
                elif isinstance(statement, CaseStatement):
                    self.get_FALSE_LHS(statement)
        elif isinstance(ObjectRecursive, IfCondition):
            for statement in ObjectRecursive.TrueStatements:
                if isinstance(statement, ContinuousAssignment):
                    if statement.left.name in self.FALSE_LHS:
                        index = self.FALSE_LHS.index(statement.left.name)
                        self.FALSE_LHS_LINES[index].append(statement.line)
                    else:
                        self.FALSE_LHS.append(statement.left.name)
                        self.FALSE_LHS_LINES.append([statement.line])
                elif isinstance(statement, IfCondition):
                    self.get_FALSE_LHS(statement)
                elif isinstance(statement, CaseStatement):
                    self.get_FALSE_LHS(statement)
            for statement in ObjectRecursive.FalseStatements:
                if isinstance(statement, ContinuousAssignment):
                    if statement.left.name in self.FALSE_LHS:
                        index = self.FALSE_LHS.index(statement.left.name)
                        self.FALSE_LHS_LINES[index].append(statement.line)
                    else:
                        self.FALSE_LHS.append(statement.left.name)
                        self.FALSE_LHS_LINES.append([statement.line])
                elif isinstance(statement, IfCondition):
                    self.get_FALSE_LHS(statement)
                elif isinstance(statement, CaseStatement):
                    self.get_FALSE_LHS(statement)
        elif isinstance(ObjectRecursive, CaseStatement):
            for key in ObjectRecursive.items:
                statements = ObjectRecursive.items[key]
                for statement in statements:
                    if isinstance(statement, ContinuousAssignment):
                        if statement.left.name in self.FALSE_LHS:
                            index = self.FALSE_LHS.index(statement.left.name)
                            self.FALSE_LHS_LINES[index].append(statement.line)
                        else:
                            self.FALSE_LHS.append(statement.left.name)
                            self.FALSE_LHS_LINES.append([statement.line])
                    elif isinstance(statement, IfCondition):
                        self.get_FALSE_LHS(statement)
                    elif isinstance(statement, CaseStatement):
                        self.get_FALSE_LHS(statement)

    def get_contributors(self, Op):
        if isinstance(Op, BaseOperations):
            self.get_contributors(Op.left)
            self.get_contributors(Op.right)
        elif isinstance(Op, UnaryOperations):
            self.get_contributors(Op.operand)
        elif isinstance(Op, SignalNode):
            self.condition_contributors.append(Op)


class CaseStatement:
    def __init__(self, Statement, Items, Items_lines, lines, Non_parallel):
        self.statement = Statement
        self.items = Items
        self.items_line = Items_lines
        self.lines = lines
        self.current_item = []
        self.LHS_ITEMS = {}
        self.LHS_ITEMS_LINES = {}
        self.LHSOUTSIDE_ITEMS = {}
        self.LHSOUTSIDE_ITEMS_LINES = {}
        self.case_contributors = []
        self.Non_parallel = Non_parallel
        self.get_contributors(self.statement)
        self.get_LHS(self, [])

    def get_LHS(self, ObjectRecursive, Add_list_item):
        if isinstance(ObjectRecursive, CaseStatement) and ObjectRecursive == self:
            for item in self.items:
                self.LHS_ITEMS[item] = []
                self.LHS_ITEMS_LINES[item] = []
                self.LHSOUTSIDE_ITEMS[item] = []
                self.LHSOUTSIDE_ITEMS_LINES[item] = []
                for statement in self.items[item]:
                    if isinstance(statement, ContinuousAssignment):
                        if statement.left.name in self.LHS_ITEMS[item]:
                            index = self.LHS_ITEMS[item].index(statement.left.name)
                            self.LHS_ITEMS_LINES[item][index].append(statement.line)
                        else:
                            self.LHS_ITEMS[item].append(statement.left.name)
                            self.LHS_ITEMS_LINES[item].append([statement.line])
                        if statement.left.name in self.LHSOUTSIDE_ITEMS[item]:
                            index = self.LHSOUTSIDE_ITEMS[item].index(statement.left.name)
                            self.LHSOUTSIDE_ITEMS_LINES[item][index].append(statement.line)
                        else:
                            self.LHSOUTSIDE_ITEMS[item].append(statement.left.name)
                            self.LHSOUTSIDE_ITEMS_LINES[item].append([statement.line])
                    elif isinstance(statement, IfCondition):
                        self.get_LHS(statement, item)
                    elif isinstance(statement, CaseStatement):
                        self.get_LHS(statement, item)
        elif isinstance(ObjectRecursive, IfCondition):
            for statement in ObjectRecursive.TrueStatements:
                if isinstance(statement, ContinuousAssignment):
                    if statement.left.name in self.LHS_ITEMS[Add_list_item]:
                        index = self.LHS_ITEMS[Add_list_item].index(statement.left.name)
                        self.LHS_ITEMS_LINES[Add_list_item][index].append(statement.line)
                    else:
                        self.LHS_ITEMS[Add_list_item].append(statement.left.name)
                        self.LHS_ITEMS_LINES[Add_list_item].append([statement.line])
                elif isinstance(statement, IfCondition):
                    self.get_LHS(statement, Add_list_item)
                elif isinstance(statement, CaseStatement):
                    self.get_LHS(statement, Add_list_item)
            for statement in ObjectRecursive.FalseStatements:
                if isinstance(statement, ContinuousAssignment):
                    if statement.left.name in self.LHS_ITEMS[Add_list_item]:
                        index = self.LHS_ITEMS[Add_list_item].index(statement.left.name)
                        self.LHS_ITEMS_LINES[Add_list_item][index].append(statement.line)
                    else:
                        self.LHS_ITEMS[Add_list_item].append(statement.left.name)
                        self.LHS_ITEMS_LINES[Add_list_item].append([statement.line])
                elif isinstance(statement, IfCondition):
                    self.get_LHS(statement, Add_list_item)
                elif isinstance(statement, CaseStatement):
                    self.get_LHS(statement, Add_list_item)
        elif isinstance(ObjectRecursive, CaseStatement):
            for key in ObjectRecursive.items:
                statements = ObjectRecursive.items[key]
                for statement in statements:
                    if isinstance(statement, ContinuousAssignment):
                        if statement.left.name in self.LHS_ITEMS[Add_list_item]:
                            index = self.LHS_ITEMS[Add_list_item].index(statement.left.name)
                            self.LHS_ITEMS_LINES[Add_list_item][index].append(statement.line)
                        else:
                            self.LHS_ITEMS[Add_list_item].append(statement.left.name)
                            self.LHS_ITEMS_LINES[Add_list_item].append([statement.line])
                    elif isinstance(statement, IfCondition):
                        self.get_LHS(statement, Add_list_item)
                    elif isinstance(statement, CaseStatement):
                        self.get_LHS(statement, Add_list_item)

    def get_contributors(self, Op):
        if isinstance(Op, BaseOperations):
            self.get_contributors(Op.left)
            self.get_contributors(Op.right)
        elif isinstance(Op, UnaryOperations):
            self.get_contributors(Op.operand)
        elif isinstance(Op, SignalNode):
            self.case_contributors.append(Op)


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
    def __init__(self, name, type, size, observer, line, portype):
        self._value = "x"
        self.size = size
        self.name = name
        self.type = type
        self.portype = portype
        self.declaration_line = line
        self.observer = observer
        self.parents = []
        self.contributors = []
        self.internal_contributors = []
        self.possible_values = []
        self.visited = []
        self.complete_flag = 0

    def add_parent(self, parent):
        self.parents.append(parent)
        self.get_contributors(self)

    def get_contributors(self, ObjectRecursive):
        if isinstance(ObjectRecursive, SignalNode):
            if ObjectRecursive.portype == "internal" or ObjectRecursive.portype == "output":
                for parent in ObjectRecursive.parents:
                    for parent_cont in parent.contributors:
                        # if isinstance(parent_cont, SignalNode) and ObjectRecursive.name == "current_state_5":
                        #     print(parent_cont.name)
                        #     print(parent_cont.portype)
                        #     print(ObjectRecursive is self)
                        if isinstance(parent_cont, SignalNode) and parent_cont.name not in self.visited:
                            self.visited.append(parent_cont.name)
                            if parent_cont != self:
                                self.get_contributors(parent_cont)
                        if isinstance(parent_cont,
                                      SignalNode) and ObjectRecursive is self and parent_cont.portype == "internal":
                            # print(parent_cont.name)
                            # print(parent_cont.portype)
                            self.internal_contributors.append(parent_cont)
                            self.internal_contributors = list(set(self.internal_contributors))
                            # print(self.internal_contributors[0].name)
            elif ObjectRecursive.portype == "input":
                self.contributors.append(ObjectRecursive)
                self.contributors = list(set(self.contributors))

    @property
    def value(self):
        for parent in self.parents:
            parent.run_assignment()
            if self._value != "x":
                self.possible_values.append(self._value)
                self.possible_values = list(set(self.possible_values))
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
        self.internal = {}
        self.continuous_assignment = []
        self.procedual_assignment = []
        self.ALLFF = []

    def add_input(self, inputAdd: SignalNode):
        self.inputs[inputAdd.name] = inputAdd

    def add_output(self, outputAdd: SignalNode):
        self.outputs[outputAdd.name] = outputAdd

    def add_internal(self, internalAdd: SignalNode):
        self.internal[internalAdd.name] = internalAdd

    def add_always(self, alwaysAdd):
        self.procedual_assignment.append(alwaysAdd)
        self.get_FF(alwaysAdd)

    def add_assign(self, assignAdd: ContinuousAssignment):
        self.continuous_assignment.append(assignAdd)

    def get_FF(self, Recursiveobject):
        if isinstance(Recursiveobject, ProcedualAssignment):
            Flip_FLop = 0
            for key in Recursiveobject.sensitivity_list:
                if Recursiveobject.sensitivity_list[key] == "posedge" or Recursiveobject.sensitivity_list[
                    key] == "negedge":
                    Flip_FLop = 1
                    break
            if Flip_FLop:
                for Assignment in Recursiveobject.Allblocks:
                    if isinstance(Assignment, ContinuousAssignment):
                        if Assignment.type == "NonBlocking":
                            if Assignment.left.name not in self.ALLFF:
                                self.ALLFF.append(Assignment.left.name)
                        elif Assignment.type == "Blocking":
                            flag = self.check_FF(Recursiveobject, Assignment.line, Assignment.left.name)
                            if flag:
                                if Assignment.left.name in self.ALLFF:
                                    del self.ALLFF[Assignment.left.name]
                            else:
                                self.ALLFF.append(Assignment.left.name)
                    elif isinstance(Assignment, IfCondition):
                        self.get_FF(Assignment)
                    elif isinstance(Assignment, CaseStatement):
                        self.get_FF(Assignment)
        elif isinstance(Recursiveobject, IfCondition):
            for Assignment in Recursiveobject.TrueStatements:
                if isinstance(Assignment, ContinuousAssignment):
                    if Assignment.type == "NonBlocking":
                        if Assignment.left.name not in self.ALLFF:
                            self.ALLFF.append(Assignment.left.name)
                    elif Assignment.type == "Blocking":
                        flag = self.check_FF(Recursiveobject, Assignment.line, Assignment.left.name)
                        if flag:
                            if Assignment.left.name in self.ALLFF:
                                del self.ALLFF[Assignment.left.name]
                        else:
                            self.ALLFF.append(Assignment.left.name)
                elif isinstance(Assignment, IfCondition):
                    self.get_FF(Assignment)
                elif isinstance(Assignment, CaseStatement):
                    self.get_FF(Assignment)
            for Assignment in Recursiveobject.FalseStatements:
                if isinstance(Assignment, ContinuousAssignment):
                    if Assignment.type == "NonBlocking":
                        if Assignment.left.name not in self.ALLFF:
                            self.ALLFF.append(Assignment.left.name)
                    elif Assignment.type == "Blocking":
                        flag = self.check_FF(Recursiveobject, Assignment.line, Assignment.left.name)
                        if flag:
                            if Assignment.left.name in self.ALLFF:
                                del self.ALLFF[Assignment.left.name]
                        else:
                            self.ALLFF.append(Assignment.left.name)
                elif isinstance(Assignment, IfCondition):
                    self.get_FF(Assignment)
                elif isinstance(Assignment, CaseStatement):
                    self.get_FF(Assignment)
        elif isinstance(Recursiveobject, CaseStatement):
            for keys in Recursiveobject.items:
                statements = Recursiveobject.items[keys]
                for Assignment in statements:
                    if isinstance(Assignment, ContinuousAssignment):
                        if Assignment.type == "NonBlocking":
                            if Assignment.left.name not in self.ALLFF:
                                self.ALLFF.append(Assignment.left.name)
                        elif Assignment.type == "Blocking":
                            flag = self.check_FF(Recursiveobject, Assignment.line, Assignment.left.name)
                            if flag:
                                if Assignment.left.name in self.ALLFF:
                                    del self.ALLFF[Assignment.left.name]
                            else:
                                self.ALLFF.append(Assignment.left.name)
                    elif isinstance(Assignment, IfCondition):
                        self.get_FF(Assignment)
                    elif isinstance(Assignment, CaseStatement):
                        self.get_FF(Assignment)

    def check_FF(self, ObjectRecursive, line, name):
        if isinstance(ObjectRecursive, ProcedualAssignment):
            for Assignments in ObjectRecursive.Allblocks:
                if isinstance(Assignments, ContinuousAssignment):
                    if name in Assignments.contributors and line > Assignments.line:
                        return True
                elif isinstance(Assignments, IfCondition):
                    if name in Assignments.condition_contributors and line > Assignments.start_line:
                        return True
                    flag = self.check_FF(Assignments, line, name)
                    if flag:
                        return True
                elif isinstance(Assignments, CaseStatement):
                    if name == Assignments.statement.name:
                        return True
                    flag = self.check_FF(Assignments, line, name)
                    if flag:
                        return True
            return False
        elif isinstance(ObjectRecursive, IfCondition):
            for Assignments in ObjectRecursive.TrueStatements:
                if isinstance(Assignments, ContinuousAssignment):
                    if name in Assignments.contributors and line > Assignments.line:
                        return True
                elif isinstance(Assignments, IfCondition):
                    if name in Assignments.condition_contributors and line > Assignments.start_line:
                        return True
                    flag = self.check_FF(Assignments, line, name)
                    if flag:
                        return True
                elif isinstance(Assignments, CaseStatement):
                    if name == Assignments.statement.name:
                        return True
                    flag = self.check_FF(Assignments, line, name)
                    if flag:
                        return True
            for Assignments in ObjectRecursive.FalseStatements:
                if isinstance(Assignments, ContinuousAssignment):
                    if name in Assignments.contributors and line > Assignments.line:
                        return True
                elif isinstance(Assignments, IfCondition):
                    if name in Assignments.condition_contributors and line > Assignments.start_line:
                        return True
                    flag = self.check_FF(Assignments, line, name)
                    if flag:
                        return True
                elif isinstance(Assignments, CaseStatement):
                    if name == Assignments.statement.name:
                        return True
                    flag = self.check_FF(Assignments, line, name)
                    if flag:
                        return True
            return False
        elif isinstance(ObjectRecursive, CaseStatement):
            for keys in ObjectRecursive.items:
                statements = ObjectRecursive.items[keys]
                for Assignments in statements:
                    if isinstance(Assignments, ContinuousAssignment):
                        if name in Assignments.contributors and line > Assignments.line:
                            return True
                    elif isinstance(Assignments, IfCondition):
                        if name in Assignments.condition_contributors and line > Assignments.start_line:
                            return True
                        flag = self.check_FF(ObjectRecursive, line, name)
                        if flag:
                            return True
                    elif isinstance(Assignments, CaseStatement):
                        if name == Assignments.statement.name:
                            return True
                        flag = self.check_FF(ObjectRecursive, line, name)
                        if flag:
                            return True
            return False


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
                if self.right.value != 0:
                    return self.left.value / self.right.value
            elif self.type == "~^" or self.type == "^~":
                return xnor(self.left.value, self.right.value)
            elif self.type == "<<":
                return self.left.value << self.right.value
            elif self.type == ">>":
                return self.left.value >> self.right.value
            elif self.type == "<":
                return int(self.left.value < self.right.value)
            elif self.type == "<=":
                return int(self.left.value <= self.right.value)
            elif self.type == ">":
                return int(self.left.value > self.right.value)
            elif self.type == ">=":
                return int(self.left.value >= self.right.value)
            elif self.type == "==":
                return int(self.left.value == self.right.value)
            elif self.type == "!=":
                return int(self.left.value != self.right.value)
            elif self.type == "&&":
                return int(self.left.value and self.right.value)
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
            elif self.type == "!":
                return int(not self.operand.value)
            else:
                return "x"
        else:
            return "x"
