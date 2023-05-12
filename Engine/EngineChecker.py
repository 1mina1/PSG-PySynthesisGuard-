from source.Parser.VerilogParser import *
import itertools


################################################################################
#################################################################

class Checks:
    def __init__(self, file):  # add attribuites
        LHS_LIST_LINES = None
        LHS_LIST = None
        l = Lexer(file)
        l.doLexing()
        v = VerilogParser(file)
        self.error_panel = {
            "Type": ("Arithmetic Overflow", "Unreachable Blocks", "Unreachable FSM State", "Un-initialized Register",
                     "Multi-Driven Bus/Register", "Non Full", "Non parallel", "Infer Latch"),
            "Num errors": [0, 0, 0, 0, 0, 0, 0, 0],
            "Error line": [[], [], [], [], [], [], [], []],
            "variable Impacted": [[], [], [], [], [], [], [], []]
        }
        self.main_node = v.Parse()
        self.module_name = self.main_node.module_name

        ##################################################################

    # Arithmetic Overflow
    def check_arithmetic_overflow(self, Recursiveobject):
        if isinstance(Recursiveobject, VerilogModule):
            for cont_assignment in Recursiveobject.continuous_assignment:
                if cont_assignment.left.size < cont_assignment.right.size:
                    self.error_panel["Num errors"][0] += 1
                    self.error_panel["Error line"][0].append(cont_assignment.line)
                    self.error_panel["variable Impacted"][0].append(cont_assignment.left.name)
            for always_block in Recursiveobject.procedual_assignment:
                for Assignment in always_block.Allblocks:
                    if isinstance(Assignment, ContinuousAssignment):
                        if Assignment.left.size < Assignment.right.size:
                            self.error_panel["Num errors"][0] += 1
                            self.error_panel["Error line"][0].append(Assignment.line)
                            self.error_panel["variable Impacted"][0].append(Assignment.left.name)
                    elif isinstance(Assignment, IfCondition):
                        self.check_arithmetic_overflow(Assignment)
                    elif isinstance(Assignment, CaseStatement):
                        self.check_arithmetic_overflow(Assignment)
        elif isinstance(Recursiveobject, IfCondition):
            for Assignment in Recursiveobject.TrueStatements:
                if isinstance(Assignment, ContinuousAssignment):
                    if Assignment.left.size < Assignment.right.size:
                        self.error_panel["Num errors"][0] += 1
                        self.error_panel["Error line"][0].append(Assignment.line)
                        self.error_panel["variable Impacted"][0].append(Assignment.left.name)
                elif isinstance(Assignment, IfCondition):
                    self.check_arithmetic_overflow(Assignment)
                elif isinstance(Assignment, CaseStatement):
                    self.check_arithmetic_overflow(Assignment)
            for Assignment in Recursiveobject.FalseStatements:
                if isinstance(Assignment, ContinuousAssignment):
                    if Assignment.left.size < Assignment.right.size:
                        self.error_panel["Num errors"][0] += 1
                        self.error_panel["Error line"][0].append(Assignment.line)
                        self.error_panel["variable Impacted"][0].append(Assignment.left.name)
                elif isinstance(Assignment, IfCondition):
                    self.check_arithmetic_overflow(Assignment)
                elif isinstance(Assignment, CaseStatement):
                    self.check_arithmetic_overflow(Assignment)
        elif isinstance(Recursiveobject, CaseStatement):
            for keys in Recursiveobject.items:
                statements = Recursiveobject.items[keys]
                for Assignment in statements:
                    if isinstance(Assignment, ContinuousAssignment):
                        if Assignment.left.size < Assignment.right.size:
                            self.error_panel["Num errors"][0] += 1
                            self.error_panel["Error line"][0].append(Assignment.line)
                            self.error_panel["variable Impacted"][0].append(Assignment.left.name)
                    elif isinstance(Assignment, IfCondition):
                        self.check_arithmetic_overflow(Assignment)
                    elif isinstance(Assignment, CaseStatement):
                        self.check_arithmetic_overflow(Assignment)

    ##################################################################
    # Unreachable Blocks Func
    def check_unreachable_blocks(self, Recursiveobject):
        if isinstance(Recursiveobject, VerilogModule):
            for always_block in Recursiveobject.procedual_assignment:
                for Assignment in always_block.Allblocks:
                    if isinstance(Assignment, ContinuousAssignment):
                        pass
                    elif isinstance(Assignment, IfCondition):
                        found_1 = 0
                        found_0 = 0
                        contributors = {}
                        for cond_cont in Assignment.condition_contributors:
                            if isinstance(cond_cont, SignalNode):
                                if cond_cont.portype == "input":
                                    if cond_cont.name not in contributors:
                                        contributors[cond_cont.name] = cond_cont
                                elif cond_cont.portype == "internal" or cond_cont.portype == "output":
                                    for cond_cont_cont in cond_cont.contributors:
                                        if cond_cont_cont.name not in contributors:
                                            contributors[cond_cont_cont.name] = cond_cont_cont
                        value_combinations = [range(2 ** input_obj.size) for input_obj in contributors.values()]
                        combinations = list(itertools.product(*value_combinations))
                        # Check that all combinations occur in the dictionary
                        for combination in combinations:
                            for input_name, input_obj in contributors.items():
                                # Get the value for this input from the current combination
                                input_value = combination[list(contributors.keys()).index(input_name)]
                                # Set the input value in the dictionary
                                input_obj.value = input_value
                                if Assignment.condition.value == 0:
                                    found_0 = 1
                                elif Assignment.condition.value != "x":
                                    found_1 = 1
                                if found_1 and found_0:
                                    break
                        if not (found_0 and found_1):
                            self.error_panel["Num errors"][1] += 1
                            self.error_panel["Error line"][1].append(Assignment.start_line)
                            list_cont = []
                            for cont in Assignment.condition_contributors:
                                list_cont.append(cont.name)
                            self.error_panel["variable Impacted"][1].append(list_cont)
                        self.check_unreachable_blocks(Assignment)
                    elif isinstance(Assignment, CaseStatement):
                        self.check_unreachable_blocks(Assignment)
        elif isinstance(Recursiveobject, IfCondition):
            for Assignment in Recursiveobject.TrueStatements:
                if isinstance(Assignment, ContinuousAssignment):
                    pass
                elif isinstance(Assignment, IfCondition):
                    found_1 = 0
                    found_0 = 0
                    contributors = {}
                    for cond_cont in Assignment.condition_contributors:
                        if isinstance(cond_cont, SignalNode):
                            if cond_cont.portype == "input":
                                if cond_cont.name not in contributors:
                                    contributors[cond_cont.name] = cond_cont
                            elif cond_cont.portype == "internal" or cond_cont.portype == "output":
                                for cond_cont_cont in cond_cont.contributors:
                                    if cond_cont_cont.name not in contributors:
                                        contributors[cond_cont_cont.name] = cond_cont_cont
                    value_combinations = [range(2 ** input_obj.size) for input_obj in contributors.values()]
                    combinations = list(itertools.product(*value_combinations))
                    # Check that all combinations occur in the dictionary
                    for combination in combinations:
                        for input_name, input_obj in contributors.items():
                            # Get the value for this input from the current combination
                            input_value = combination[list(contributors.keys()).index(input_name)]
                            # Set the input value in the dictionary
                            input_obj.value = input_value
                            if Assignment.condition.value == 0:
                                found_0 = 1
                            elif Assignment.condition.value != "x":
                                found_1 = 1
                            if found_1 and found_0:
                                break
                    if not (found_0 and found_1):
                        self.error_panel["Num errors"][1] += 1
                        self.error_panel["Error line"][1].append(Assignment.start_line)
                        list_cont = []
                        for cont in Assignment.condition_contributors:
                            list_cont.append(cont.name)
                        self.error_panel["variable Impacted"][1].append(list_cont)
                    self.check_unreachable_blocks(Assignment)
                elif isinstance(Assignment, CaseStatement):
                    self.check_unreachable_blocks(Assignment)
            for Assignment in Recursiveobject.FalseStatements:
                if isinstance(Assignment, ContinuousAssignment):
                    pass
                elif isinstance(Assignment, IfCondition):
                    found_1 = 0
                    found_0 = 0
                    contributors = {}
                    for cond_cont in Assignment.condition_contributors:
                        if isinstance(cond_cont, SignalNode):
                            if cond_cont.portype == "input":
                                if cond_cont.name not in contributors:
                                    contributors[cond_cont.name] = cond_cont
                            elif cond_cont.portype == "internal" or cond_cont.portype == "output":
                                for cond_cont_cont in cond_cont.contributors:
                                    if cond_cont_cont.name not in contributors:
                                        contributors[cond_cont_cont.name] = cond_cont_cont
                    value_combinations = [range(2 ** input_obj.size) for input_obj in contributors.values()]
                    combinations = list(itertools.product(*value_combinations))
                    # Check that all combinations occur in the dictionary
                    for combination in combinations:
                        for input_name, input_obj in contributors.items():
                            # Get the value for this input from the current combination
                            input_value = combination[list(contributors.keys()).index(input_name)]
                            # Set the input value in the dictionary
                            input_obj.value = input_value
                            if Assignment.condition.value == 0:
                                found_0 = 1
                            elif Assignment.condition.value != "x":
                                found_1 = 1
                            if found_1 and found_0:
                                break
                    if not (found_0 and found_1):
                        self.error_panel["Num errors"][1] += 1
                        self.error_panel["Error line"][1].append(Assignment.start_line)
                        list_cont = []
                        for cont in Assignment.condition_contributors:
                            list_cont.append(cont.name)
                        self.error_panel["variable Impacted"][1].append(list_cont)
                    self.check_unreachable_blocks(Assignment)
                elif isinstance(Assignment, CaseStatement):
                    self.check_unreachable_blocks(Assignment)
        elif isinstance(Recursiveobject, CaseStatement):
            for keys in Recursiveobject.items:
                statements = Recursiveobject.items[keys]
                for Assignment in statements:
                    if isinstance(Assignment, ContinuousAssignment):
                        pass
                    elif isinstance(Assignment, IfCondition):
                        found_1 = 0
                        found_0 = 0
                        contributors = {}
                        for cond_cont in Assignment.condition_contributors:
                            if isinstance(cond_cont, SignalNode):
                                if cond_cont.portype == "input":
                                    if cond_cont.name not in contributors:
                                        contributors[cond_cont.name] = cond_cont
                                elif cond_cont.portype == "internal" or cond_cont.portype == "output":
                                    for cond_cont_cont in cond_cont.contributors:
                                        if cond_cont_cont.name not in contributors:
                                            contributors[cond_cont_cont.name] = cond_cont_cont
                        value_combinations = [range(2 ** input_obj.size) for input_obj in contributors.values()]
                        combinations = list(itertools.product(*value_combinations))
                        # Check that all combinations occur in the dictionary
                        for combination in combinations:
                            for input_name, input_obj in contributors.items():
                                # Get the value for this input from the current combination
                                input_value = combination[list(contributors.keys()).index(input_name)]
                                # Set the input value in the dictionary
                                input_obj.value = input_value
                                if Assignment.condition.value == 0:
                                    found_0 = 1
                                elif Assignment.condition.value != "x":
                                    found_1 = 1
                                if found_1 and found_0:
                                    break
                        if not (found_0 and found_1):
                            self.error_panel["Num errors"][1] += 1
                            self.error_panel["Error line"][1].append(Assignment.start_line)
                            list_cont = []
                            for cont in Assignment.condition_contributors:
                                list_cont.append(cont.name)
                            self.error_panel["variable Impacted"][1].append(list_cont)
                        self.check_arithmetic_overflow(Assignment)
                    elif isinstance(Assignment, CaseStatement):
                        self.check_arithmetic_overflow(Assignment)

    ##################################################################
    # Unreachable FSM State Func
    def check_unreachable_fSM_state(self, Recursiveobject):
        if isinstance(Recursiveobject, VerilogModule):
            for always_block in Recursiveobject.procedual_assignment:
                for Assignment in always_block.Allblocks:
                    if isinstance(Assignment, ContinuousAssignment):
                        pass
                    elif isinstance(Assignment, IfCondition):
                        self.check_unreachable_fSM_state(Assignment)
                    elif isinstance(Assignment, CaseStatement):
                        self.check_unreachable_fSM_state(Assignment)
        elif isinstance(Recursiveobject, IfCondition):
            for Assignment in Recursiveobject.TrueStatements:
                if isinstance(Assignment, ContinuousAssignment):
                    pass
                elif isinstance(Assignment, IfCondition):
                    self.check_unreachable_fSM_state(Assignment)
                elif isinstance(Assignment, CaseStatement):
                    self.check_unreachable_fSM_state(Assignment)
            for Assignment in Recursiveobject.FalseStatements:
                if isinstance(Assignment, ContinuousAssignment):
                    pass
                elif isinstance(Assignment, IfCondition):
                    self.check_unreachable_fSM_state(Assignment)
                elif isinstance(Assignment, CaseStatement):
                    self.check_unreachable_fSM_state(Assignment)
        elif isinstance(Recursiveobject, CaseStatement):
            found = {}
            for key in Recursiveobject.items:
                found[key] = 0
            if len(Recursiveobject.case_contributors) == 1:
                if Recursiveobject.case_contributors[0].name in self.main_node.ALLFF:
                    All_possible_transition = []
                    if not Recursiveobject.case_contributors[0].internal_contributors:
                        if Recursiveobject.case_contributors[0].contributors:
                            contributors = {}
                            for cont in Recursiveobject.case_contributors[0].contributors:
                                contributors[cont.name] = cont
                            value_combinations = [range(2 ** input_obj.size) for input_obj in contributors.values()]
                            combinations = list(itertools.product(*value_combinations))
                            # Check that all combinations occur in the dictionary
                            for combination in combinations:
                                for input_name, input_obj in contributors.items():
                                    # Get the value for this input from the current combination
                                    input_value = combination[list(contributors.keys()).index(input_name)]
                                    # Set the input value in the dictionary
                                    input_obj.value = input_value
                                    x = Recursiveobject.case_contributors[0].value
                        x = Recursiveobject.case_contributors[0].value
                        All_possible_transition = Recursiveobject.case_contributors[0].possible_values
                    else:
                        internal_cont = Recursiveobject.case_contributors[0].internal_contributors[0]
                        x = internal_cont.value
                        All_possible_transition = internal_cont.possible_values
                    for transition in All_possible_transition:
                        if transition in Recursiveobject.items:
                            found[transition] = 1
                    for transition in found:
                        if found[transition] == 0:
                            self.error_panel["Num errors"][2] += 1
                            self.error_panel["Error line"][2].append(Recursiveobject.items_line[transition][0])
                            self.error_panel["variable Impacted"][2].append("state " + str(transition))
            for keys in Recursiveobject.items:
                statements = Recursiveobject.items[keys]
                for Assignment in statements:
                    if isinstance(Assignment, ContinuousAssignment):
                        pass
                    elif isinstance(Assignment, IfCondition):
                        self.check_unreachable_fSM_state(Assignment)
                    elif isinstance(Assignment, CaseStatement):
                        self.check_unreachable_fSM_state(Assignment)

    ###########################################################################
    # Un-initialized Register Func
    def check_uninitialized_register(self, Recursiveobject, SignalsDic):
        if isinstance(Recursiveobject, VerilogModule):
            for always_block in Recursiveobject.procedual_assignment:
                Flip_FLop = 0
                for key in always_block.sensitivity_list:
                    if always_block.sensitivity_list[key] == "posedge" or always_block.sensitivity_list[
                        key] == "negedge":
                        Flip_FLop = 1
                        break
                if not Flip_FLop:
                    continue
                for Signal in always_block.LHS:
                    if Signal in self.main_node.ALLFF:
                        SignalsDic[Signal] = 0
                for Assignment in always_block.Allblocks:
                    if isinstance(Assignment, ContinuousAssignment):
                        if isinstance(Assignment.right, Constant) and Assignment.left.name in SignalsDic:
                            SignalsDic[Assignment.left.name] = 1
                    elif isinstance(Assignment, IfCondition):
                        self.check_uninitialized_register(Assignment, SignalsDic)
                    elif isinstance(Assignment, CaseStatement):
                        self.check_uninitialized_register(Assignment, SignalsDic)
            for signal in SignalsDic:
                if not SignalsDic[signal]:
                    if signal in Recursiveobject.inputs:
                        self.error_panel["Error line"][3].append(Recursiveobject.inputs[signal].declaration_line)
                    elif signal in Recursiveobject.outputs:
                        self.error_panel["Error line"][3].append(Recursiveobject.outputs[signal].declaration_line)
                    elif signal in Recursiveobject.internal:
                        self.error_panel["Error line"][3].append(Recursiveobject.internal[signal].declaration_line)
                    self.error_panel["Num errors"][3] += 1
                    self.error_panel["variable Impacted"][3].append(signal)
        elif isinstance(Recursiveobject, IfCondition):
            for Assignment in Recursiveobject.TrueStatements:
                if isinstance(Assignment, ContinuousAssignment):
                    if isinstance(Assignment.right, Constant) and Assignment.left.name in SignalsDic:
                        SignalsDic[Assignment.left.name] = 1
                elif isinstance(Assignment, IfCondition):
                    self.check_uninitialized_register(Assignment, SignalsDic)
                elif isinstance(Assignment, CaseStatement):
                    self.check_uninitialized_register(Assignment, SignalsDic)
            for Assignment in Recursiveobject.FalseStatements:
                if isinstance(Assignment, ContinuousAssignment):
                    if isinstance(Assignment.right, Constant) and Assignment.left.name in SignalsDic:
                        SignalsDic[Assignment.left.name] = 1
                elif isinstance(Assignment, IfCondition):
                    self.check_uninitialized_register(Assignment, SignalsDic)
                elif isinstance(Assignment, CaseStatement):
                    self.check_uninitialized_register(Assignment, SignalsDic)
        elif isinstance(Recursiveobject, CaseStatement):
            for keys in Recursiveobject.items:
                statements = Recursiveobject.items[keys]
                for Assignment in statements:
                    if isinstance(Assignment, ContinuousAssignment):
                        if isinstance(Assignment.right, Constant) and Assignment.left.name in SignalsDic:
                            SignalsDic[Assignment.left.name] = 1
                    elif isinstance(Assignment, IfCondition):
                        self.check_uninitialized_register(Assignment, SignalsDic)
                    elif isinstance(Assignment, CaseStatement):
                        self.check_uninitialized_register(Assignment, SignalsDic)

    ##################################################################
    # Multi-Driven Bus/Register
    def check_multi_Driven_bus_register(self, Recursiveobject):
        if isinstance(Recursiveobject, VerilogModule):
            LHS_LIST = []
            LHS_LIST_OVERLAP = []
            LHS_LIST_OVERLAP_LINES = []
            LHS_LIST_LINES = []
            for cont_assignment in Recursiveobject.continuous_assignment:
                if cont_assignment.left.name in LHS_LIST:
                    if cont_assignment.left.name in LHS_LIST_OVERLAP:
                        index = LHS_LIST_OVERLAP.index(cont_assignment.left.name)
                        LHS_LIST_OVERLAP_LINES[index].append(cont_assignment.line)
                    else:
                        LHS_LIST_OVERLAP.append(cont_assignment.left.name)
                        index = LHS_LIST.index(cont_assignment.left.name)
                        LHS_LIST_OVERLAP_LINES.append([LHS_LIST_LINES[index], cont_assignment.line])
                else:
                    LHS_LIST.append(cont_assignment.left.name)
                    LHS_LIST_LINES.append(cont_assignment.line)

            ##################################################################################################################################################
            list_non_overlab = []
            z = []
            diff = []
            i = 1
            for always_block in Recursiveobject.procedual_assignment:
                j = 1
                for always_block_2 in Recursiveobject.procedual_assignment:
                    if always_block == always_block_2:
                        continue
                    else:
                        common = list(set(always_block.LHS).intersection(set(always_block_2.LHS)))
                        if not list_non_overlab:
                            list_non_overlab = common
                            diff = list_non_overlab
                        elif set(common) ^ set(list_non_overlab):
                            diff = list(set(common) - set(list_non_overlab))
                            list_non_overlab = list(list_non_overlab)
                            for diff_elem in diff:
                                list_non_overlab.append(diff_elem)
                        length = len(list_non_overlab)
                        for i in range(length - len(z)):
                            z.append([])

                        mixed_list = []

                        for index in common:
                            if index in list_non_overlab:
                                elem_ind = list_non_overlab.index(index)
                                x = always_block.LHS.index(index)
                                lines_1st_always = always_block.LHS_LINES[x]
                                y = always_block_2.LHS.index(index)
                                lines_2st_always = always_block_2.LHS_LINES[y]
                                mixed_list = lines_1st_always + lines_2st_always
                                if not z[elem_ind]:
                                    z[elem_ind] = mixed_list
                                else:
                                    z[elem_ind] = z[elem_ind] + mixed_list

            for t in range(len(list_non_overlab)):
                z[t] = sorted(list(dict.fromkeys(z[t])))

            for error_cont, error_cont_line in zip(LHS_LIST_OVERLAP, LHS_LIST_OVERLAP_LINES):
                list_non_overlab.append(error_cont)
                z.append(error_cont_line)

            self.error_panel["Num errors"][4] = len(list_non_overlab)
            self.error_panel["Error line"][4] = z
            self.error_panel["variable Impacted"][4] = list_non_overlab

    # ################################################################################################3

    ####################################################################
    # Non full parallel Case func
    def check_non_full_parallel_case(self, Recursiveobject):
        if isinstance(Recursiveobject, VerilogModule):
            for always_block in Recursiveobject.procedual_assignment:
                for Assignment in always_block.Allblocks:
                    if isinstance(Assignment, ContinuousAssignment):
                        pass
                    elif isinstance(Assignment, IfCondition):
                        self.check_non_full_parallel_case(Assignment)
                    elif isinstance(Assignment, CaseStatement):
                        self.check_non_full_parallel_case(Assignment)
        elif isinstance(Recursiveobject, IfCondition):
            for Assignment in Recursiveobject.TrueStatements:
                if isinstance(Assignment, ContinuousAssignment):
                    pass
                elif isinstance(Assignment, IfCondition):
                    self.check_non_full_parallel_case(Assignment)
                elif isinstance(Assignment, CaseStatement):
                    self.check_non_full_parallel_case(Assignment)
            for Assignment in Recursiveobject.FalseStatements:
                if isinstance(Assignment, ContinuousAssignment):
                    pass
                elif isinstance(Assignment, IfCondition):
                    self.check_non_full_parallel_case(Assignment)
                elif isinstance(Assignment, CaseStatement):
                    self.check_non_full_parallel_case(Assignment)
        elif isinstance(Recursiveobject, CaseStatement):
            Full_case = 0
            if "default" in Recursiveobject.items:
                Full_case = 1
            else:
                if 2 ** Recursiveobject.statement.size == len(list(set(Recursiveobject.items.keys()))):
                    Full_case = 1
                if not Full_case:
                    self.error_panel["Num errors"][5] += 1
                    self.error_panel["Error line"][5].append(Recursiveobject.lines[0])
                    cont_list = []
                    for cont in Recursiveobject.case_contributors:
                        cont_list.append(cont.name)
                    self.error_panel["variable Impacted"][5].append(cont_list)
            if Recursiveobject.Non_parallel:
                self.error_panel["Num errors"][6] += 1
                self.error_panel["Error line"][6].append(Recursiveobject.lines[0])
                cont_list = []
                for cont in Recursiveobject.case_contributors:
                    cont_list.append(cont.name)
                self.error_panel["variable Impacted"][6].append(cont_list)
            for keys in Recursiveobject.items:
                statements = Recursiveobject.items[keys]
                for Assignment in statements:
                    if isinstance(Assignment, ContinuousAssignment):
                        pass
                    elif isinstance(Assignment, IfCondition):
                        self.check_non_full_parallel_case(Assignment)
                    elif isinstance(Assignment, CaseStatement):
                        self.check_non_full_parallel_case(Assignment)

    ##################################################################
    # Infer Latch func
    def check_infer_latch(self, Recursiveobject, ParentLHS):
        if isinstance(Recursiveobject, VerilogModule):
            for always_block in Recursiveobject.procedual_assignment:
                Flip_FLop = 0
                for Assignment in always_block.Allblocks:
                    for key in always_block.sensitivity_list:
                        if always_block.sensitivity_list[key] == "posedge" or always_block.sensitivity_list[
                            key] == "negedge":
                            Flip_FLop = 1
                            break
                    if Flip_FLop:
                        continue
                    if isinstance(Assignment, ContinuousAssignment):
                        pass
                    elif isinstance(Assignment, IfCondition):
                        self.check_infer_latch(Assignment, always_block.LHSOUTSIDE)
                    elif isinstance(Assignment, CaseStatement):
                        self.check_infer_latch(Assignment, always_block.LHSOUTSIDE)
        elif isinstance(Recursiveobject, IfCondition):
            latch_infered = 0
            difference = list(set(Recursiveobject.TRUE_LHS) - set(Recursiveobject.FALSE_LHS)) + list(
                set(Recursiveobject.FALSE_LHS) - set(Recursiveobject.TRUE_LHS))
            difference = list(set(difference))
            for diff in difference:
                if diff in ParentLHS:
                    latch_infered = 0
                else:
                    if diff in Recursiveobject.TRUE_LHS:
                        index = Recursiveobject.TRUE_LHS.index(diff)
                        index = Recursiveobject.TRUE_LHS_LINES[index]
                    elif diff in Recursiveobject.FALSE_LHS:
                        index = Recursiveobject.FALSE_LHS.index(diff)
                        index = Recursiveobject.FALSE_LHS_LINES[index]
                    if diff in self.error_panel["variable Impacted"][7]:
                        position = self.error_panel["variable Impacted"][7].index(diff)
                        for ind in index:
                            self.error_panel["Error line"][7][position].append(ind)
                    else:
                        self.error_panel["Num errors"][7] += 1
                        self.error_panel["Error line"][7].append(index)
                        self.error_panel["variable Impacted"][7].append(diff)
            for Assignment in Recursiveobject.TrueStatements:
                if isinstance(Assignment, ContinuousAssignment):
                    pass
                elif isinstance(Assignment, IfCondition):
                    self.check_infer_latch(Assignment, ParentLHS + Recursiveobject.TRUEOUTSIDE_LHS)
                elif isinstance(Assignment, CaseStatement):
                    self.check_infer_latch(Assignment, ParentLHS + Recursiveobject.TRUEOUTSIDE_LHS)
            for Assignment in Recursiveobject.FalseStatements:
                if isinstance(Assignment, ContinuousAssignment):
                    pass
                elif isinstance(Assignment, IfCondition):
                    self.check_infer_latch(Assignment, ParentLHS + Recursiveobject.FALSEOUTSIDE_LHS)
                elif isinstance(Assignment, CaseStatement):
                    self.check_infer_latch(Assignment, ParentLHS + Recursiveobject.FALSEOUTSIDE_LHS)
        elif isinstance(Recursiveobject, CaseStatement):
            difference = []
            for item in Recursiveobject.items:
                for item_2 in Recursiveobject.items:
                    if item == item_2:
                        continue
                    else:
                        difference += list(
                            set(Recursiveobject.LHS_ITEMS[item]) - set(Recursiveobject.LHS_ITEMS[item_2])) + list(
                            set(Recursiveobject.LHS_ITEMS[item_2]) - set(Recursiveobject.LHS_ITEMS[item]))
            difference = list(set(difference))
            for diff in difference:
                if diff not in ParentLHS:
                    index = []
                    for item in Recursiveobject.items:
                        if diff in Recursiveobject.LHS_ITEMS[item]:
                            index_2 = Recursiveobject.LHS_ITEMS[item].index(diff)
                            index += Recursiveobject.LHS_ITEMS_LINES[item][index_2]
                    if diff in self.error_panel["variable Impacted"][7]:
                        position = self.error_panel["variable Impacted"][7].index(diff)
                        for ind in index:
                            self.error_panel["Error line"][7][position].append(ind)
                    else:
                        self.error_panel["Num errors"][7] += 1
                        self.error_panel["Error line"][7].append(index)
                        self.error_panel["variable Impacted"][7].append(diff)

            for keys in Recursiveobject.items:
                statements = Recursiveobject.items[keys]
                for Assignment in statements:
                    if isinstance(Assignment, ContinuousAssignment):
                        pass
                    elif isinstance(Assignment, IfCondition):
                        self.check_infer_latch(Assignment, ParentLHS + Recursiveobject.LHSOUTSIDE_ITEMS[keys])
                    elif isinstance(Assignment, CaseStatement):
                        self.check_infer_latch(Assignment, ParentLHS + Recursiveobject.LHSOUTSIDE_ITEMS[keys])

    def do_all_checks(self):
        self.check_arithmetic_overflow(self.main_node)
        self.check_multi_Driven_bus_register(self.main_node)
        self.check_uninitialized_register(self.main_node, {})
        self.check_infer_latch(self.main_node, [])
        self.check_unreachable_blocks(self.main_node)
        self.check_non_full_parallel_case(self.main_node)
        self.check_unreachable_fSM_state(self.main_node)
        print(self.error_panel)


# Check = Checks("E:/EECE_2023_4thyear_Final_term/Automatic_cad_tools/Lint_Tool/example/adder.v")
# Check.do_all_checks()
# print(Check.error_panel)
