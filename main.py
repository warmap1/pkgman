import sys

import aur, checks, pacman

try:
    argument = sys.argv[1]
    try:
        pkg = sys.argv[2:]
    except IndexError:
        pass
except IndexError:
    op = "-h"

#check package name
if argument != "-h":
    if not pkg:
        sys.exit('Please specify a package')

#make other checks
checks.check_pacman()
checks.check_deps()

if argument == "-A" or argument == "--aur":
    if not pkg: print("'--> Please, specify package name"); sys.exit(1)
    print(f'--> Installing {pkg}')
    aur.install_package_from_aur(pkg)

elif argument == "-P" or argument == "--pac":
    if not pkg: print("'--> Please, specify package name"); sys.exit(1)
    pacman.install(pkg)

elif argument == "-AP" or argument == "--apt":
    print("Soon")

elif argument == "-h" or argument == "--help":
    print("""Help:\n
  -A  --aur    Install AUR package
  -P  --pac    Install official package
  -Ap --apt    Install APT package (may be slow)""")

else: print("Unknown option"); sys.exit(1)