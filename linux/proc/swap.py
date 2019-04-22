from pathlib import Path
import re
from concurrent import futures
from collections import namedtuple
from linux.common import _retrieve

TaskInput = namedtuple('TaskInput', 'swap_total, pid, path')


regex_table = {
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
    """Returns total swap size in kb"""
    meminfo_fpath = Path('/proc/meminfo')
    v = _retrieve(meminfo_fpath, ['swap_total'], regex_table)
    return v['swap_total']


def swap_free():
    """Returns free swap size in kb"""
    meminfo_fpath = Path('/proc/meminfo')
    v = _retrieve(meminfo_fpath, ['swap_free'], regex_table)
    return v['swap_free']


def swap_info():
    """Returns dict(total_swap: x, swap_free: y) where x and y are in kb"""
    meminfo_fpath = Path('/proc/meminfo')
    v = _retrieve(meminfo_fpath, ['swap_total', 'swap_free'], regex_table)
    return v


def process(task_input):
    """Returns instance of TaskOutput"""
    try:
        v = _retrieve(task_input.path, ['proc_vmswap', 'proc_name'], regex_table)
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
    except FileNotFoundError:
        return None

def proc_swap_usage(pid=None):
    total = swap_total()
    if pid is None:
        """Returns list of process info on swap usage -
           each element of the list is a dict(), keyed by
    
           name: (str)
           pid: (str)
           swap_usage_kb: (float)
           swap_usage_pct: (float)
        """
        # based on pid directories under /proc
        task_inputs = [
            TaskInput(swap_total=total, pid=p.name, path=Path(p, 'status'))
            for p in Path('/proc').iterdir()
            if p.is_dir() and re.match(r'^\d+$', p.name)
        ]
        with futures.ThreadPoolExecutor() as executor:
            res = executor.map(process, task_inputs)
    
        # collect only results that is not None
        stats = [ x for x in list(res) if x is not None ]
        stats.sort(reverse=True, key=lambda x: x['swap_usage_pct'])
        return stats
    else:
        status_fpath = Path('/proc', str(pid), 'status')
        input = TaskInput(swap_total=total, pid=str(pid), path=status_fpath)
        return process(input)
