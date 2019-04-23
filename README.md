# linux-proc-utils
Python3 module provides an API to facilitate reading run-time information from Linux's `/proc` filesystem.

## Getting Started

It's best to go through some examples. There are other sample scripts in
the `samples/` directory.

1. Fetch system swap total:

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
file(s) under `/proc`, the returned values will be None.

If a value that requires conversion is fetched with the unit stated
in the target file(s) under `/proc` is not supported, i.e. not one of
the followings: kb, gb, tb, pb, ub, a RuntimeError exception is
raised. So is the case where the target file(s) do not exist. The last
case only happens (exception being raised) if the operation is not an
aggregate operations (operate on a set of processes for instance).


Some functions would require super-user access to run. Noticably
those related to file descriptors.

