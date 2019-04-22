# linux-proc-utils
Python3 module to facilitate reading run-time information from `/proc` filesystem.

## Supported Operations

| Module | Function | Return | Description | Source |
| --- | --- | --- | --- | --- |
| `linux.proc.swap` | `swap_total()` | `float` | system swap total in kb | `/proc/meminfo[SwapTotal]` |
| `linux.proc.swap` | `swap_free()` | `float` | system swap free in kb | `/proc/meminfo[SwapFree]` |
| `linux.proc.swap` | `swap_info()` | `dict(swap_total: x, swap_free: y)` | system swap total and free in kb | `/proc/meminfo[SwapTotal,SwapFree]` |
| `linux.proc.swap` | `proc_swap_usage(pid)` | `dict(name: proc_name, pid: pid, swap_usage_kb: x, swap_usage_pct: y)` | process swap usage in kb and pct | `/proc/pid/status[Name,VmSwap]` |
| `linux.proc.swap` | `proc_swap_usage()` | `list[dict(name: proc_name, pid: pid, swap_usage_kb: x, swap_usage_pct: y)]` | list of process swap usage in kb and pct in descending order by usage | `/proc/pids, /proc/pid/status[Name,VmSwap]` |
| `linux.proc.fd` | `proc_fd_usage(pid)` | `dict(name: proc_name, pid: pid, fd_usage: x)` | process file descriptor usage | `/proc/pid/fd/` |
| `linux.proc.fd` | `proc_fd_usage(pid)` | `list[dict(name: proc_name, pid: pid, fd_usage: x)]` | list of process file descriptor usage in descending order by usage | `/proc/pids, /proc/pid/status[Name], /proc/pid/fd/` |

### Missing Values

All values fetched are initialized to be None, and replaced by actual values if found.

### Exceptions

In general, some files in `/proc` should be present, and if not, you may be
running a customized kernel. In such cases, calling the functions above will
raise a `FileNotFoundError` exception.

As processes can come and go, it is not an error to open a missing process status file. They
are simply skipped.

Usually, the values fetched are in kb, and conversion is supported if they are in
mb, gb, tb, and pb. If the unit is not one of those, a `ValueError` exception is
raised.

### Timing Issues

Some functions will operate with multiple files of the /proc filesystem. This may
have synchronization issues, where for instance, the pid returned does not match the process
name. This usually is not a problem for long-running processes. But for relatively short-lived
processes, this should be something to keep in mind.

## Dependencies


## Getting Started


