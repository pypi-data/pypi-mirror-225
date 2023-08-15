import os

from pathlib import Path
from joblib import Memory
from functools import wraps

from dsp.utils import dotdict


cache_turn_on = True


def noop_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


cachedir = os.environ.get('DSP_CACHEDIR') or os.path.join(Path.home(), 'cachedir_joblib')
CacheMemory = Memory(location=cachedir, verbose=0)

cachedir2 = os.environ.get('DSP_NOTEBOOK_CACHEDIR')
NotebookCacheMemory = dotdict()
NotebookCacheMemory.cache = noop_decorator

if cachedir2:
    NotebookCacheMemory = Memory(location=cachedir2, verbose=0)


if not cache_turn_on:
    CacheMemory = dotdict()
    CacheMemory.cache = noop_decorator

    NotebookCacheMemory = dotdict()
    NotebookCacheMemory.cache = noop_decorator
