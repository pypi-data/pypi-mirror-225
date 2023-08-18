"""
Define debugging/timing tools.
"""

from datetime import datetime as dt
from numba import njit


def _do_nothing(*args):
    pass

def _do_nothing_ts(*args, **kwargs):
    pass


def _timestamp(previous=None, msg=None, minutes=False):
    now = dt.now()
    if previous is not None and msg is not None:
        elapsed_sec = (now-previous).total_seconds()
        if minutes:
            elapsed_min = elapsed_sec / 60.0
            print(f"{msg}: {elapsed_min:.2f} min")
        else:
            print(f"{msg}: {elapsed_sec:.1f} sec")
    elif msg is not None:
        print(f"{msg} [{now:%Y-%m-%d %H:%M:%S}]")
    return now


def set_debugfunctions(*, debug=0, timestamps=0, compile=True):
    dp0 = print if debug >= 0 else njit(_do_nothing) if compile else _do_nothing
    dp1 = print if debug >= 1 else njit(_do_nothing) if compile else _do_nothing
    dp2 = print if debug >= 2 else njit(_do_nothing) if compile else _do_nothing
    ts0 = _timestamp if timestamps >= 0 else _do_nothing_ts
    ts1 = _timestamp if timestamps >= 1 else _do_nothing_ts
    ts2 = _timestamp if timestamps >= 2 else _do_nothing_ts

    global debugprint
    global timestamp
    debugprint = dp0, dp1, dp2
    timestamp = ts0, ts1, ts2
    return debugprint, timestamp

set_debugfunctions()
