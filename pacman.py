import os
import subprocess as sp

def install(package):
    for pack in package:
        print(f'--> Installing {pack}')
        sp.run(f'sudo pacman -S {pack} --noconfirm', shell=True, check=True)

def remove(package):
    for pack in package():
        print(f'--> Removing {pack}')
        sp.run(f'sudo pacman -R {pack} --noconfirm', shell=True, check=True)

def update_system():
    sp.run('sudo pacman -Syu', shell=True, check=True)