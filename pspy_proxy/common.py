from pathlib import Path
import sys.executeable as execPATH
# out_path = Path('~/.pspy/bin').expanduser()
out_path = Path(execPATH).parent.expanduser()