from pathlib import Path
from sys import executable as execPATH
# out_path = Path('~/.pspy/bin').expanduser()
out_path = Path(execPATH).parent.expanduser()