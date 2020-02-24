from pathlib import Path
from sys import executable
# out_path = Path('~/.pspy/bin').expanduser()
out_path = Path(executable).parent.expanduser()