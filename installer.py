import os
import socket
#functions
import sys
import json
from globals import *
from random import randint
global session
session = randint(1, 199999)
space = " "

user_input = sys.argv
if len(user_input) > 1:
    option = sys.argv[1]
    if option == "-install":

        console_log("You selected install option", session)
        console_log("Trying to install deployer.py",session)
        deployer_set(session)
    if option == "-debugclear":
        debug_clear()
        console_log("All Debug Files Deleted", session)
    if option == "-requirements":
        requirements()


else:
    parser_data = json.load(open("parser.json", "r"))
    # print(parser_data)
    
    console_log("Program Executed without operation specified", session)
    # print(parser_data)
    print("[+]Usage: python3 installer.py [options] [value]")

    # for z in parser_data:
    #     print(f"{2*space}[{z}]")
    #     for i in parser_data[z]:
    #         if len(parser_data[z][i]) == 1:
    #             prefix = "-"
    #             suffix = ""
    #         elif parser_data[z][i].startswith("-"):
    #             prefix = "\n\t[value]\n\t\t"
    #             suffix = ""
    #         else:
    #             prefix = "-> "
    #             suffix = ""
    #         print(f"{4*space}{prefix}{parser_data[z][i]}{suffix}",end=" ")
    #     print("\n")


