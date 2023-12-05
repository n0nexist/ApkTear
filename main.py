# github.com/n0nexist/ApkTear
# main.py

import utilities as ut
from utilities import getInput
import readline
from loguru import logger
from colorama import Fore, Style, init

init()  # initialize colorama

print(ut.getLogo())  # print the logo

ut.initFolders() # creates ApkTear's folders

# start a loop for command inputs
while True:
    cmd = getInput("ApkTear")  # get user input for commands
    print("")  # print an empty line

    # check the user input for specific commands
    if cmd == "help":
        print(f"""{Fore.CYAN}{Style.BRIGHT}build {Fore.WHITE}{Style.DIM}- {Fore.CYAN}{Style.NORMAL}build a decompiled directory
{Fore.CYAN}{Style.BRIGHT}decompile {Fore.WHITE}{Style.DIM}- {Fore.CYAN}{Style.NORMAL}decompile an .apk file into a directory
{Fore.CYAN}{Style.BRIGHT}sign {Fore.WHITE}{Style.DIM}- {Fore.CYAN}{Style.NORMAL}sign a built .apk file
{Fore.CYAN}{Style.BRIGHT}delete {Fore.WHITE}{Style.DIM}- {Fore.CYAN}{Style.NORMAL}clears ApkTear's folders
{Fore.CYAN}{Style.BRIGHT}quit {Fore.WHITE}{Style.DIM}- {Fore.CYAN}{Style.NORMAL}exits from ApkTear""")

    # handle 'quit' command by logging and exiting the program
    elif cmd == "quit":
        logger.info("Exiting")
        exit(0)

    # execute the 'build' command by compiling an APK and displaying a message
    elif cmd == "build":
        ut.compApk(getInput("Decompiled directory path"))
        ut.popUpWindow("ApkTear Build", "The built command has finished")

    # execute the 'decompile' command by decompiling an APK and displaying a message
    elif cmd == "decompile":
        ut.decompApk(getInput("Apk file path"))
        ut.popUpWindow("ApkTear Decompile", "The decompile command has finished")

    # execute the 'sign' command by signing an APK and displaying a message
    elif cmd == "sign":
        ut.signApk(getInput("Apk file path"))
        ut.popUpWindow("ApkTear Sign", "The sign command has finished")

    # execute the 'delete' command by clearing ApkTear's folders and displaying a message
    elif cmd == "delete":
        ut.clearFolders()
        ut.popUpWindow("ApkTear Delete", "The delete command has finished")

    # handle unrecognized commands by logging a warning message
    else:
        logger.warning("Command not found. type \"help\"")

    print("")  # print an empty line for separation