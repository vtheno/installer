import sys
from subprocess import call
from pathlib import Path

print("Installing binaries...")
call([sys.executable, str(Path(__file__).parent / "actual_setup.py")])
call([sys.executable, str(Path(__file__).parent / "install_binary.py")])
