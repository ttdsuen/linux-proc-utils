from pathlib import Path
import re
from concurrent import futures
from linux.common import _retrieve

regex_table = {
    'proc_name': {
        'regex': r'^Name:\s*(\S.*)',
        'value_index': lambda x: x.group(1),
    },
}

def process(pid):
    proc_fd_dir = Path('/proc/{}/fd'.format(pid))
    try:
        v = _retrieve(
            Path('/proc/{}/status'.format(pid)),
            ['proc_name'],
            regex_table
        )
        fds = [ x for x in proc_fd_dir.iterdir() if re.match(r'^\d+$', x.name) ]
        if v['proc_name'] is None:
            return None
        return { 'name': v['proc_name'], 'pid': str(pid), 'fd_usage': len(fds) }
    except FileNotFoundError:
        return None


def proc_fd_usage(pid=None):
    if pid is None:
        """Returns list of process info on swap usage -
           each element of the list is a dict(), keyed by
    
           name: (str)
           pid: (str)
           swap_usage_kb: (float)
           swap_usage_pct: (float)
        """
        # based on pid directories under /proc
        pids = [
            p.name  for p in Path('/proc').iterdir()
            if p.is_dir() and re.match(r'^\d+$', p.name)
        ]
        with futures.ThreadPoolExecutor() as executor:
            res = executor.map(process, pids)
    
        # collect only results that is not None
        stats = [ x for x in list(res) if x is not None ]
        stats.sort(reverse=True, key=lambda x: x['fd_usage'])
        return stats
    else:
        r = process(pid)
        if r is None:
            return r
        return r['fd_usage']
