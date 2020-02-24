from pathlib import Path
from subprocess import call
import sys
out_path = Path('~/.local/bin').expanduser()


def main():
    call([str((out_path / "pspy-blueprint").absolute()), *sys.argv])
