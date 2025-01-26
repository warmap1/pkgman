import os
import subprocess as sp
import requests as req

AUR_BASE_URL = "https://aur.archlinux.org/rpc/?v=5&type=info&arg[]="


def get_aur_package_info(pkg_name):
    response = req.get(f"{AUR_BASE_URL}{pkg_name}")
    if response.status_code == 200:
        data = response.json()
        if data['resultcount'] > 0:
            return data['results'][0]
    return None

def install_package_from_aur(pkg_name):
    print(f"Installing AUR package: {pkg_name}")
    sp.run(f"git clone --depth 1 https://aur.archlinux.org/{pkg_name}.git ~/.cache/pkgman/{pkg_name}", shell=True)
    directory = os.getcwd()
    sp.run(f"cd ~/.cache/pkgman/{pkg_name} && makepkg", shell=True)

    pkg_file = None
    for file in os.listdir('.'):
        if file.endswith(".pkg.tar.zst") and '-debug' not in file:
            pkg_file = file
            break

    if pkg_file:
        sp.run(f"sudo pacman -U {pkg_file}", shell=True)
    else:
        print(f"Error: Couldn't find the main package for {pkg_name}.")

    os.chdir(directory)
    print(f"Installed {pkg_name}")

def install_package_and_dependencies(pkg_name, installed=set()):
    if pkg_name in installed:
        return

    pkg_info = get_aur_package_info(pkg_name)
    if pkg_info:
        dependencies = pkg_info.get('Depends', [])
        if dependencies:
            print(f"Dependencies for {pkg_name}: {dependencies}")
            for dep in dependencies:
                if is_in_official_repo(dep):
                    sp.run(f"sudo pacman -S --noconfirm {dep}", shell=True)
                else:
                    install_package_and_dependencies(dep, installed)

        install_package_from_aur(pkg_name)
        installed.add(pkg_name)
        cleanup()
    else:
        print(f"Error: Package {pkg_name} not found in AUR.")

def is_in_official_repo(pkg_name):
    result = sp.run(f"pacman -Si {pkg_name}", shell=True, stdout=sp.PIPE)
    return result.returncode == 0

def cleanup():
    sp.run("sudo rm -rf ~/.cache/pkgman/", shell=True)
    print("Temporary files removed.")
