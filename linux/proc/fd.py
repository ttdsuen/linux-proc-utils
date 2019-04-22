from pathlib import Path
import re

def num_fds_pid(pid):
    proc_fd_dir = Path('/proc/{}/fd'.format(pid))
    if not proc_fd_dir.exists() or not proc_fd_dir.is_dir():
        return None
    fds = [ x for x in proc_fd_dir.iterdir() if re.match(r'^\d+$', x.name) ]
    return len(fds)
