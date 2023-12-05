# github.com/n0nexist/ApkTear
# utilities.py

import subprocess
import os
from loguru import logger
import shutil
from colorama import Fore, Style, init
from tkinter import messagebox
from threading import Thread as th

init()  # initialize colorama

author = "github.com/n0nexist"
version = "1.1.1"

def getLogo():
    # function to return the ApkTear logo
    return f"""{Fore.CYAN}
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$ $$$$$$$$$$$$$$$$ $$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$  $$$$$$$$$$$$$$ $$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$               $$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$                   $$$$$$$$$$$$$$$
$$$$$$$$$$$$$$    $$$         $$$    $$$$$$$$$$$$$
$$$$$$$$$$$$$     $$$         $$$     $$$$$$$$$$$$
$$$$$$$$$$$$                           $$$$$$$$$$$
$$$$$$$$$$$$                           $$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
$$$$$   $$$$$                          $$$$    $$$
$$$$      $$          {Style.BRIGHT}{Fore.WHITE}ApkTear{Style.RESET_ALL}{Fore.CYAN}           $$      $$
$$$$      $$        {Style.BRIGHT}{Fore.WHITE}Version: {version}{Style.RESET_ALL}{Fore.CYAN}      $$      $$
$$$$      $$   {Style.BRIGHT}{Fore.WHITE}By: {author}{Style.RESET_ALL}{Fore.CYAN}  $$      $$
$$$$      $$                            $$      $$
$$$$      $$                            $$      $$
$$$$      $$                            $$      $$
$$$$      $$                            $$      $$
$$$$     $$$                            $$      $$
$$$$$   $$$$                            $$$   $$$$
$$$$$$$$$$$$                            $$$$$$$$$$
$$$$$$$$$$$$                            $$$$$$$$$$
$$$$$$$$$$$$$                          $$$$$$$$$$$
$$$$$$$$$$$$$$$$$      $$$$$$     $$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$      $$$$$$     $$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$      $$$$$$     $$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    """

# function to display a popup window
def popUpWindowFunction(title, message):
    messagebox.showinfo(title, message)

# function to start a thread for displaying a popup window
def popUpWindow(title, message):
    th(target=popUpWindowFunction, args=(title,message,)).start()

# function to check if a file exists
def fileExists(path):
    if os.path.exists(path) == False:
        logger.critical(f"\"{path}\" Does not exist.")
        return False

    if " " in path:
        logger.warning(f"\"{path}\" Could be invalid because it contains spaces")

    return True

# function to parse the file path
def parsePath(path):
    return os.path.split(path)[-1]

# function to sign an APK
def signApk(path):
    command = [
        "java", "-jar", os.path.join("Dependencies","apksigner.jar"), "sign",
        "--ks", os.path.join("Dependencies","ReleaseKey.keystore"),
        path
    ]

    logger.info(f"Signing \"{path}\"")

    if not fileExists(path):
        return

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)

    while True:
        output = process.stdout.readline()
        if "Keystore password for" in output:
            logger.info("Putting keystore password")
            process.stdin.write("ciaociao\n")
            process.stdin.flush()
        elif output == '' and process.poll() is not None:
            break

        if process.poll() is not None:
            break
    
    process.communicate()

    if process.returncode == 0:
        logger.success("Signed!")
    else:
        logger.error("Error occurred during signing")
        return

    output = os.path.join("Signed_Apks",parsePath(path).replace('.idsig',''))

    logger.debug(f"Output will be: \"{output}\"")

    shutil.move(f"{path}.idsig", output)

# function to clean up temporary files
def cleanUpFramePath():
    logger.info("Cleaning up")

    if os.path.exists("tempframepath"):
        shutil.rmtree("tempframepath")

# function to decompile an APK
def decompApk(path):
    logger.info(f"Decompiling \"{path}\"")

    if not fileExists(path):
        return

    apktool = os.path.join("Dependencies","apktool.jar")
    output = os.path.join("Decompiled_Apks",parsePath(path))

    logger.debug(f"Output will be: \"{output}\"")

    os.system(f"java -jar {apktool} d {path} --frame-path=\"tempframepath\" --output \"{output}\" -f")

    cleanUpFramePath()

    logger.success("Decompiled!")

# function to recompile an APK
def compApk(path):
    logger.info(f"Recompiling \"{path}\"")

    if not fileExists(path):
        return

    apktool = os.path.join("Dependencies","apktool.jar")
    output = os.path.join("Built_Apks",parsePath(path))

    logger.debug(f"Output will be: \"{output}\"")

    os.system(f"java -jar {apktool} b {path} --frame-path=\"tempframepath\" --output \"{output}\" -f")

    cleanUpFramePath()

    logger.success("Recompiled!")

# function to get user input
def getInput(text):
    return input(f"{Fore.CYAN}{Style.BRIGHT}{text}{Fore.WHITE}{Style.DIM}>{Style.NORMAL} ")

# function to clear ApkTear's folders
def clearFolders():
    logger.warning("THIS ACTION IS NOT REVERSIBLE!")
    if getInput("Type \"YES\" to clear ApkTear's folders")=="YES":
        logger.info("Deleting everything...")

        folders = ["Built_Apks", "Decompiled_Apks", "Signed_Apks"]

        for folder in folders:

            if len(os.listdir(folder))==0:
                logger.warning(f"Folder \"{folder}\" is already empty")

            else:
                logger.debug(f"Clearing folder \"{folder}\"")

                try:
                    shutil.rmtree(folder)
                except PermissionError:
                    logger.error(f"Cannot delete folder \"{folder}\" as it may be used by another process")
                except FileNotFoundError:
                    logger.warning(f"Cannot delete folder \"{folder}\" as it doesn't exist")

                try:
                    os.mkdir(folder)
                except FileExistsError:
                    logger.warning(f"Cannot create folder \"{folder}\" as it already exists")

        logger.success("Done!")
    
    else:
        logger.info("You didn't type \"YES\", nothing will be deleted.")