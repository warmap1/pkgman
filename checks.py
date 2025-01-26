import subprocess as sp
import sys

def check_pacman():
    pm = sp.run("pacman -h", shell=True, stdout=sp.PIPE, text=True)
    if not "command not found" not in pm.stdout:
        print("--> This program is currently orientated on using pacman package manager, and so cannot run on your system because you don`t have it"); sys.exit(1)

def check_deps():
    #deps variables
    paru = 0
    debtap = 0

    print("--> Checking dependencies...")

    #paru
    p = sp.run("paru --version", shell=True, stdout=sp.PIPE, text=True)
    if "command not found" not in p.stdout: paru = 1

    #debtap
    dt = sp.run("debtap -h", shell=True, stdout=sp.PIPE, text=True)
    if "command not found" not in dt.stdout: debtap = 1

    if paru == 0 and debtap == 0: print("--> Please, install paru and debtap before running this program"); sys.exit(1)
    if paru == 1 and debtap == 0: print("--> Please, install debtap before running this program"); sys.exit(1)
    if paru == 0 and debtap == 1: print("--> Please, install paru before running this program"); sys.exit(1)
