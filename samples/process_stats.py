#!/usr/bin/env python3

#
# process_stats.py - outputs proc_name pid swap_usage(kb,pct) fd_usage
#
# usage: process_stats.py --sort [fd|swap] [--limit N]
#
# Author: Daniel Suen
#

import argparse
from linux.proc.swap import swap_usage, proc_swap_usage
from linux.proc.fd import proc_fd_usage, fd_usage
import sys
from functools import partial

titles = [ 'name', 'pid', 'swap_usage_kb', 'swap_usage_pct', 'fd_usage' ]
justifications = [ '<', '>', '>', '>', '>' ]

#fd_titles = [ 'name', 'pid', 'fd_usage' ]
#fd_justifications = [ '<', '>', '>' ]

def swap_stop(i, item):
    return item['swap_usage_kb'] == 0


def fd_stop(i, item):
    return item['fd_usage'] == 0

def limit_stop(limit, i, item):
    return i >= limit


def output(stats, titles, widths, justifications, stop):
    t = [ '{' + str(i) + ':' + justifications[i] + str(widths[i]) + '}' for i, x in enumerate(widths) ]
    t_fmt = '    '.join(t)

    print(t_fmt.format(*titles))
    for i, item in enumerate(stats):
        if stop(i, item):
            break
        vv = [ item[x] for x in titles ]
        print(t_fmt.format(*vv))

def usage():
    return 'process_stats.py --sort [fd|swap]'

def check_positive(value):
    n = int(value)
    if n <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return n

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sort', choices=['fd', 'swap'], required=True, help='sort order, either fd or swap', dest='sort')
    parser.add_argument('--limit', type=int, help='number of entries to show')
    args = parser.parse_args()
    stats = None
    stop = None

    if args.limit is not None:
        if args.limit > 0:
            stop = partial(limit_stop, args.limit)
        else:
            print('{}'.format(usage()))
            sys.exit(1)

    if args.sort == 'swap':
        stats = swap_usage()
        if stop is None:
            stop = swap_stop
        for stat in stats:
            stat['fd_usage'] = '-'
            stat['fd_usage'] = proc_fd_usage(stat['pid'])
    if args.sort == 'fd':
        stats = fd_usage()
        if stop is None:
            stop = fd_stop
        for stat in stats:
            t = proc_swap_usage(stat['pid'])
            for x in ['swap_usage_kb', 'swap_usage_pct']:
                stat[x] = '-'
            if t is not None:
                for x in ['swap_usage_kb', 'swap_usage_pct']:
                    stat[x] = t[x]

     

    widths = [ len(x) for x in titles ]
    for item in stats:
        for i, title in enumerate(titles):
            widths[i] = max(widths[i], len(str(item.get(title))))

    output(stats, titles, widths, justifications, stop)
