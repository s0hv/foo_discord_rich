import subprocess
from pathlib import Path


def patch(patches):
    cur_dir = Path(__file__).parent.absolute()
    root_dir = cur_dir.parent

    for p in patches:
        assert(p.exists() and p.is_file())

    subprocess.check_call(f"git apply --ignore-whitespace {' '.join(str(p) for p in patches)}", cwd=root_dir, shell=True)
