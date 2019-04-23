"""Linux /proc Swap Module

This module supports querying related to swap
"""

from pathlib import Path
import re
from concurrent import futures
from collections import namedtuple
from linux.common import _retrieve

_TaskInput = namedtuple('_TaskInput', 'swap_total, pid, path')

_regex_table = {
    'swap_total': {
        'regex': r'SwapTotal:\s*(\d+)\s*(\w+)',
        'value_index': lambda x: float(x.group(1)),
        'unit_index': lambda x: x.group(2).lower(),
    },
    'swap_free': {
        'regex': r'SwapFree:\s*(\d+)\s*(\w+)',
        'value_index': lambda x: float(x.group(1)),
        'unit_index': lambda x: x.group(2).lower(),
    },
    'proc_name': {
        'regex': r'^Name:\s*(\S.*)',
        'value_index': lambda x: x.group(1),
    },
    'proc_vmswap': {
        'regex': r'VmSwap:\s*(\d+)\s*(\w+)',
        'value_index': lambda x: float(x.group(1)),
        'unit_index': lambda x: x.group(2).lower(),
    }
}


def swap_total():
    """Returns total swap size in kb

    :returns: Total swap size in kb or None if
        `/proc/meminfo[SwapTotal]` not found
    :rtype: float or None if the SwapTotal not found

    """
    meminfo_fpath = Path('/proc/meminfo')
    v = _retrieve(meminfo_fpath, ['swap_total'], _regex_table)
    return v['swap_total']


def swap_free():
    """Returns free swap size in kb

    :returns: Free swap size in kb or None if
        `/proc/meminfo[SwapFree]` not found
    :rtype: float or None

    """
    meminfo_fpath = Path('/proc/meminfo')
    v = _retrieve(meminfo_fpath, ['swap_free'], _regex_table)
    return v['swap_free']


def swap_info():
    """Returns swap info (total and free) in kb

    :returns: A dictionary with keys:
        swap_total: Total swap size in kb or None if
            `/proc/meminfo[SwapTotal]` is not found
        swap_free: Free swap size in kb or None if
            `/proc/meminfo[SwapFree]` is not found
    :rtype: dict
    """
    meminfo_fpath = Path('/proc/meminfo')
    v = _retrieve(meminfo_fpath, ['swap_total', 'swap_free'], _regex_table)
    return v


def _process(task_input):
    """Returns process swap usage

    :param task_input: a namedtuple of type TaskInput
    :type task_input: TaskInput
    :returns: None if process no longer exists. Otherwise, a
        dictionary with keys:
            name: Process name
            pid: Process pid
            swap_usage_kb: Swap used in kb
            swap_usage_pct: Swap used as percentage of total
    :rtype: dict
    """
    v = _retrieve(task_input.path, ['proc_vmswap', 'proc_name'], _regex_table)
    pct = None
    if v['proc_vmswap'] is not None:
        pct = v['proc_vmswap'] / task_input.swap_total * 100.0
    if v['proc_name'] is None or v['proc_vmswap'] is None:
        return None
    return {
        'name': v['proc_name'],
        'pid': task_input.pid,
        'swap_usage_kb': v['proc_vmswap'],
        'swap_usage_pct': pct
    };

def swap_usage():
    """Returns a list of process swap usage in descending order

    :returns: A list of process swap usage, each list
        element is a dictionary with keys:
        name: Process name
        pid: Process pid
        swap_usage_kb: Swap used in kb
        swap_usage_pct: Swap used as percentage of total
    :rtype: list

    """

    total = swap_total()
    # based on pid directories under /proc
    task_inputs = [
        _TaskInput(swap_total=total, pid=p.name, path=Path(p, 'status'))
        for p in Path('/proc').iterdir()
        if p.is_dir() and re.match(r'^\d+$', p.name)
    ]
    with futures.ThreadPoolExecutor() as executor:
        res = executor.map(_process, task_inputs)

    # collect only results that is not None
    stats = [ x for x in list(res) if x is not None ]
    stats.sort(reverse=True, key=lambda x: x['swap_usage_pct'])
    return stats


def proc_swap_usage(pid):
    """Returns process swap usage

    :param pid: The process ID
    :type pid: str
    :returns: A dictionary of swap usage with the following keys:
        name: Process name
        pid: Process pid
        swap_usage_kb: Swap used in kb
        swap_usage_pct: Swap used as percentage of total

        or None if the process no longer exists
    :rtype: dict
    """
    total = swap_total()
    status_fpath = Path('/proc', str(pid), 'status')
    input = _TaskInput(swap_total=total, pid=str(pid), path=status_fpath)
    return _process(input)
