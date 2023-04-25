# import re
#
# from PyQt5.QtCore import QRegularExpression
#
# text = """/*test cases covered:
# 1-reading and writing while in reset mode and check if its always empty and there is nothing to read
# 2-writing the whole fifo until full then reading it until empty
# 3-reading and writing simultanesly
# */"""
# print(re.findall(r"/\*(?s:.*?)\*/", text))
# # => ['123\ndef\n356']
# print(re.findall(r"^123[\w\W]*?\*/", text, re.M))
# commentStartExpression = re.compile("/\*")
# commentEndExpression = re.compile("\*/")
# match = commentStartExpression.match(text)
# if match:
#     print(1)
#     print(match.start())
#     print(match.end())
#
# match = commentEndExpression.search(text)
# if match:
#     print(2)
#     print(match.start())
#     print(match.end())
#     print(text[222])
#
# # => ['123\ndef\n356']

string = "123abc456def[789gh0x12i'f1234j'g5678"

new_string = ""
current_number = ""
import string
#
# for i in range(len(string)):
#     if string[i].isdigit() and not current_number:
#         # Start of a new number sequence
#         if i == 0 or string[i - 1] not in "bdh":
#             # Add space before number
#             new_string += " "
#         current_number = string[i]
#     elif string[i].isdigit() and current_number:
#         # Continuation of current number sequence
#         current_number += string[i]
#     elif not string[i].isdigit() and current_number:
#         # End of current number sequence
#         if string[i - 1] not in "bdh":
#             # Add space after number
#             new_string += current_number + " "
#         else:
#             new_string += current_number
#         current_number = ""
#     if not current_number and string[i] != " ":
#         # Add other characters to the new string
#         new_string += string[i]
#
# if current_number:
#     # Handle end of string if current number is still in progress
#     if string[-1] not in "bdh":
#         # Add space after number
#         new_string += current_number + " "
#     else:
#         new_string += current_number
#
# print(new_string)
print(string.ascii_lowercase)
