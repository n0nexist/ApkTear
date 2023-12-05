import utilities as ut
from utilities import getInput
import readline
from loguru import logger
from colorama import Fore, Style, init

init()

print(ut.getLogo())

while True:
    cmd = getInput("ApkTear")
    print("")
    if cmd == "help":
        print(f"""{Fore.CYAN}{Style.BRIGHT}build {Fore.WHITE}{Style.DIM}- {Fore.CYAN}{Style.NORMAL}build a decompiled directory
{Fore.CYAN}{Style.BRIGHT}decompile {Fore.WHITE}{Style.DIM}- {Fore.CYAN}{Style.NORMAL}decompile an .apk file into a directory
{Fore.CYAN}{Style.BRIGHT}sign {Fore.WHITE}{Style.DIM}- {Fore.CYAN}{Style.NORMAL}sign a built .apk file
{Fore.CYAN}{Style.BRIGHT}delete {Fore.WHITE}{Style.DIM}- {Fore.CYAN}{Style.NORMAL}clears ApkTear's folders
{Fore.CYAN}{Style.BRIGHT}quit {Fore.WHITE}{Style.DIM}- {Fore.CYAN}{Style.NORMAL}exits from ApkTear""")

    elif cmd == "quit":
        logger.info("Exiting")
        exit(0)

    elif cmd == "build":
        ut.compApk(getInput("Decompiled directory path"))

    elif cmd == "decompile":
        ut.decompApk(getInput("Apk file path"))

    elif cmd == "sign":
        ut.signApk(getInput("Apk file path"))

    elif cmd == "delete":
        ut.clearFolders()

    else:
        logger.warning("Command not found. type \"help\"")

    print("")