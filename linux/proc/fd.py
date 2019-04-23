"""Linux /proc File Descriptor Module

This module supports querying related to file descriptors

"""
from pathlib import Path
import re
from concurrent import futures
from ..common import _retrieve

_regex_table = {
    'proc_name': {
        'regex': r'^Name:\s*(\S.*)',
        'value_index': lambda x: x.group(1),
    },
}

def _process(pid):
    """Returns process file descriptor usage

    :param pid: The process ID
    :type pid: str
    :returns: A dictionary with keys:
        name: Process name
        pid: Process pid
        fd_usage: Number of file descriptors used
    """
    proc_fd_dir = Path('/proc/{}/fd'.format(pid))
    v = _retrieve(
        Path('/proc/{}/status'.format(pid)),
        ['proc_name'],
        _regex_table
    )
    fds = [ x for x in proc_fd_dir.iterdir() if re.match(r'^\d+$', x.name) ]
    if v['proc_name'] is None:
        return None
    return { 'name': v['proc_name'], 'pid': str(pid), 'fd_usage': len(fds) }


def proc_fd_usage(pid):
    """Returns number of used file descriptors of process with process ID `pid`

    :param pid: The process ID
    :type pid: str
    :returns: Number of file descriptors used or None if the process no
        longer exists
    :rtype: int
    """
    r = _process(pid)
    if r is None:
        return r
    return r['fd_usage']


def fd_usage():
    """Returns a list of process file descriptor usage in descending order

    :returns: A list of process file descriptor usage, each list element
        is a dictionary with keys:
            name: Process name
            pid: Process pid
            fd_usage: Number of file descriptors used
    :rtype: list
    """
    # based on pid directories under /proc
    pids = [
        p.name  for p in Path('/proc').iterdir()
        if p.is_dir() and re.match(r'^\d+$', p.name)
    ]
    with futures.ThreadPoolExecutor() as executor:
        res = executor.map(_process, pids)

    # collect only results that is not None
    stats = [ x for x in list(res) if x is not None ]
    stats.sort(reverse=True, key=lambda x: x['fd_usage'])
    return stats
