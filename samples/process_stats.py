#!/usr/bin/env python3


from linux.proc.swap import *
from linux.proc.fd import *

swap_titles = [ 'name', 'pid', 'swap_usage_kb', 'swap_usage_pct', 'num_fds' ]
swap_justifications = [ '<', '>', '>', '>', '>' ]

fd_titles = [ 'name', 'pid', 'fd_usage' ]
fd_justifications = [ '<', '>', '>' ]

def swap_stop(item):
    return item['swap_usage_kb'] == 0


def fd_stop(item):
    return item['fd_usage'] == 0


def output(stats, titles, widths, justifications, stop):
    t = [ '{' + str(i) + ':' + justifications[i] + str(widths[i]) + '}' for i, x in enumerate(widths) ]
    t_fmt = '    '.join(t)

    print(t_fmt.format(*titles))
    for item in stats:
        if stop(item):
            break
        vv = [ item[x] for x in titles ]
        print(t_fmt.format(*vv))


if __name__ == '__main__':
    swap_stats = proc_swap_usage()

    for stat in swap_stats:
        stat['num_fds'] = proc_fd_usage(stat['pid'])

    swap_widths = [ len(x) for x in swap_titles ]
    for item in swap_stats:
        for i, title in enumerate(swap_titles):
            swap_widths[i] = max(swap_widths[i], len(str(item.get(title))))

    output(swap_stats, swap_titles, swap_widths, swap_justifications, swap_stop)

    print('\n\n\n')

    fd_stats = proc_fd_usage()
    fd_widths = [ len(x) for x in fd_titles ]
    for item in fd_stats:
        for i, title in enumerate(fd_titles):
            fd_widths[i] = max(fd_widths[i], len(str(item.get(title))))

    output(fd_stats, fd_titles, fd_widths, fd_justifications, fd_stop)
