# linux-proc-utils
Python3 module provides an API to facilitate reading run-time information from Linux's `/proc` filesystem.

## Getting Started

It's best to go through an example. There is a usable sample script in
the `samples/` directory.


```
import linux.proc.swap

try:
    swap_total_kb = swap_total()
    if swap_total_kb is not None:
        print('swap total (kb): {}'.format(swap_total_kb))
    swap_free_kb = swap_free()
    if swap_free_kb is not None:
        print('swap free (kb): {}'.format(swap_free_kb))

    swap_info_dict = swap_info()
    if swap_info_dict['swap_total'] is not None:
        print('swap total (kb): {}'.format(swap_info_dict['swap_total']))
    if swap_info_dict['swap_free'] is not None:
        print('swap free (kb): {}'.format(swap_info_dict['swap_free']))

except RuntimeException as e:
    print('error: {}'.format(e))
```

The module `linux.proc.swap` is imported on line 1 as we are querying
swap metrics. `swap_total()` returns a `float`, and so is `swap_free()`.
If the value cannot be fetched due to missing attributes in the target
file(s) under `/proc`, the values returned will be None. If the target
file(s) are missing in `proc`, a RuntimeError exception is raised.

For values with byte units (kb, mb, for instance) in the
target file(s) under `/proc`, if the unit is not supported, i.e. not one of
the followings: kb, gb, tb, pb, ub, a RuntimeError exception is
raised.

As processes come and go, when using `swap_usage()` and `fd_usage()`,
no RuntimeError exception is raised if some target processes are no longer
present during the run.

Some functions would require super-user access to run. Noticably
those related to file descriptors.

You can always read the documentation through regular Python ```help()```.
For instance,

```
Python 3.6.7 (default, Oct 22 2018, 11:32:17) 
[GCC 8.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import linux.proc.fd
>>> help(linux.proc.fd)

elp on module linux.proc.fd in linux.proc:

NAME
    linux.proc.fd - Linux /proc File Descriptor Module

DESCRIPTION
    This module supports querying related to file descriptors

FUNCTIONS
    fd_usage()
        Returns a list of process file descript...
...

```

## License

This project is licensed under the MIT License - see the
[LICENSE.md](LICENSE.md) file for details
