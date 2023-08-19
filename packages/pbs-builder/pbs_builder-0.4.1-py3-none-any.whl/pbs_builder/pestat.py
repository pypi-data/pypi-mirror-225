import sys
import subprocess
from pathlib import Path

def run():
    exe = Path(__file__).parent / "bin" / "pestat"
    args = [str(exe), ] + sys.argv[1:]
    return subprocess.call(args, shell=False)

