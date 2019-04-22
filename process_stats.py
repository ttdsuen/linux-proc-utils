#!/usr/bin/env python3


from linux.proc.swap import *
from linux.proc.fd import *

titles = [ 'name', 'pid', 'swap_usage_kb', 'swap_usage_pct', 'num_fds' ]
justifications= [ '<', '>', '>', '>', '>' ]


def output(stats, titles, widths, justifications):
    t = [ '{' + str(i) + ':' + justifications[i] + str(widths[i]) + '}' for i, x in enumerate(widths) ]
    t_fmt = '    '.join(t)

    print(t_fmt.format(*titles))
    for item in stats:
        vv = [ item[x] for x in titles ]
        print(t_fmt.format(*vv))


if __name__ == '__main__':
    stats = process_swap_usage()

    for stat in stats:
        #num_fds = num_fds_pid(stat['pid'])
        stat['num_fds'] = num_fds_pid(stat['pid'])

    widths = [ len(x) for x in titles ]
    for item in stats:
        for i, title in enumerate(titles):
            widths[i] = max(widths[i], len(str(item.get(title))))

    output(stats, titles, widths, justifications)
    
