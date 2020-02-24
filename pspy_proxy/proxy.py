from subprocess import call
from pspy_placeholder import out_path
import sys


def main():
    call([str((out_path / "pspy-blueprint").absolute()), *sys.argv[1:]])
