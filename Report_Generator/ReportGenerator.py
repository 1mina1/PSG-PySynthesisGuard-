"""
this file contains the debugger and report extractor which is coming from the engine
"""
from source.Engine.EngineChecker import *


class ReportGenerator:
    def __init__(self, Error_dictionary, File_name, Filepath):
        self.results_dic = None
        self.Error_dic = Error_dictionary
        self.File_name = File_name
        self.FilePath = Filepath
        self.Text_string = """====================================================================
(PSG) Lint Check Report
Design : """ + str(File_name) + """Sections
    Section 1 : Check Summary
    Section 2 : Check Details
====================================================================


====================================================================
Section 1 : Check Summary

------------------
| Errors (""" + str(sum(Error_dictionary["Num errors"])) + """) |
------------------
    Arithmetic over flow        :   """ + str(Error_dictionary["Num errors"][0]) + """
    Unreachable Blocks          :   """ + str(Error_dictionary["Num errors"][1]) + """
    Unreachable FSM State       :   """ + str(Error_dictionary["Num errors"][2]) + """
    Un-initialized Register     :   """ + str(Error_dictionary["Num errors"][3]) + """
    Multi-Driven Bus/Register   :   """ + str(Error_dictionary["Num errors"][4]) + """
    Non Full/Parallel Case      :   """ + str(Error_dictionary["Num errors"][5]) + """
    Infer Latch                 :   """ + str(Error_dictionary["Num errors"][6]) + """
====================================================================



====================================================================
Section 2 : Check Details
"""
        self.Arange_lines(self.Error_dic)
        self.print_lines()

    def Arange_lines(self, results):
        self.results_dic = {}
        # arithmetic overflow
        for i in range(len(results["Error line"][0])):
            if results["Error line"][0][i] in self.results_dic:
                self.results_dic[results["Error line"][0][i]].append("-- Arithmetic overflow error at line " + str(
                    results["Error line"][0][i]) + " in variable " + str(results["variable Impacted"][0][i]))
            else:
                self.results_dic[results["Error line"][0][i]] = ["Arithmetic overflow error at line " + str(
                    results["Error line"][0][i]) + " in variable " + str(results["variable Impacted"][0][i])]
        for i in range(len(results["Error line"][1])):
            if results["Error line"][1][i] in self.results_dic:
                self.results_dic[results["Error line"][1][i]].append("unreachable Block error at line " + str(
                    results["Error line"][1][i]) + " with variables may be the cause ")
                for j in range(len(results["variable Impacted"][1][i])):
                    self.results_dic[results["Error line"][1][i]][-1] += str(
                        results["variable Impacted"][1][i][j]) + " "
            else:
                self.results_dic[results["Error line"][1][i]] = ["unreachable Block error at line " + str(
                    results["Error line"][1][i]) + " with variables may be the cause "]
                for j in range(len(results["variable Impacted"][1][i])):
                    self.results_dic[results["Error line"][1][i]][0] += str(results["variable Impacted"][1][i][j]) + " "
        for i in range(len(results["Error line"][2])):
            if results["Error line"][2][i] in self.results_dic:
                self.results_dic[results["Error line"][2][i]].append("unreachable finite state machine at line " + str(
                    results["Error line"][2][i]) + " because " + str(
                    results["variable Impacted"][2][i]) + " is unreachable")
            else:
                self.results_dic[results["Error line"][2][i]] = ["unreachable finite state machine at line " + str(
                    results["Error line"][2][i]) + " because " + str(
                    results["variable Impacted"][2][i]) + " is unreachable"]
        for i in range(len(results["Error line"][3])):
            if results["Error line"][3][i] in self.results_dic:
                self.results_dic[results["Error line"][3][i]].append("uninitialized register declared at line " + str(
                    results["Error line"][3][i]) + " in reg " + str(results["variable Impacted"][3][i]))
            else:
                self.results_dic[results["Error line"][3][i]] = ["uninitialized register declared at line " + str(
                    results["Error line"][3][i]) + " in reg " + str(results["variable Impacted"][3][i])]
        for i in range(len(results["variable Impacted"][4])):
            for line in results["Error line"][4][i]:
                if line in self.results_dic:
                    self.results_dic[line].append("multidriven block at line " + str(line) + " in variable " + str(
                        results["variable Impacted"][4][i]))
                else:
                    self.results_dic[line] = ["multidriven block at line " + str(line) + " in variable " + str(
                        results["variable Impacted"][4][i])]
        for i in range(len(results["Error line"][5])):
            if results["Error line"][5][i] in self.results_dic:
                self.results_dic[results["Error line"][5][i]].append("Non Full case statement at line " + str(
                    results["Error line"][5][i]) + " with variables may be the cause ")
                for j in range(len(results["variable Impacted"][5][i])):
                    self.results_dic[results["Error line"][5][i]][-1] += str(
                        results["variable Impacted"][5][i][j]) + " "
            else:
                self.results_dic[results["Error line"][5][i]] = ["Non Full case statement at line " + str(
                    results["Error line"][5][i]) + " with variables may be the cause "]
                for j in range(len(results["variable Impacted"][5][i])):
                    self.results_dic[results["Error line"][5][i]][0] += str(results["variable Impacted"][5][i][j]) + " "
        for i in range(len(results["Error line"][6])):
            if results["Error line"][6][i] in self.results_dic:
                self.results_dic[results["Error line"][6][i]].append("Non parallel case statement at line " + str(
                    results["Error line"][6][i]) + " with variables may be the cause ")
                for j in range(len(results["variable Impacted"][6][i])):
                    self.results_dic[results["Error line"][6][i]][-1] += str(
                        results["variable Impacted"][6][i][j]) + " "
            else:
                self.results_dic[results["Error line"][6][i]] = ["Non parallel case statement at line " + str(
                    results["Error line"][6][i]) + " with variables may be the cause "]
                for j in range(len(results["variable Impacted"][6][i])):
                    self.results_dic[results["Error line"][6][i]][0] += str(results["variable Impacted"][6][i][j]) + " "
        for i in range(len(results["variable Impacted"][7])):
            for line in results["Error line"][7][i]:
                if line in self.results_dic:
                    self.results_dic[line].append("latch infered at line " + str(line) + " in variable " + str(
                        results["variable Impacted"][7][i]))
                else:
                    self.results_dic[line] = ["latch infered at line " + str(line) + " in variable " + str(
                        results["variable Impacted"][7][i])]

    def print_lines(self):
        lines_sorted = sorted(self.results_dic.keys())
        for line in lines_sorted:
            for text in self.results_dic[line]:
                self.Text_string += "\t" + text + "\n"
        self.Text_string += """====================================================================
Finish
====================================================================
        """
        with open(self.FilePath + "/" + "Lint_check_rpt.txt", "w") as WriteFile:
            WriteFile.write(self.Text_string)


# Check = Checks("E:/EECE_2023_4thyear_Final_term/Automatic_cad_tools/Lint_Tool/example/adder.v")
# Check.do_all_checks()
# RG = ReportGenerator(Check.error_panel, Check.module_name,"E:/EECE_2023_4thyear_Final_term/Automatic_cad_tools/Lint_Tool/example")
# print(Check.error_panel)
