import copy
import uuid
import os
import dill
from hashlib import md5

from typing import List


def generate_md5_hash(*args, **kwargs):
    return str(md5((str(args) + str(kwargs)).encode()).hexdigest())


class _Cache(object):
    def __init__(
        self,
        function,
        cache_dir="./cache/",
        compress=False,
        hash_self=False,
        ignore_args=None,
    ):
        self.cache_dir = cache_dir
        self.hash_self = hash_self
        self.compress = compress
        self.function = function
        self.ignore_args = ignore_args

        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def __call__(self, *args, **kwargs):
        if 'disable_cache' in kwargs and kwargs['disable_cache']:
            kwargs.pop('disable_cache')
            return self.function(*args, **kwargs)

        args = list(args)
        args_copy = copy.copy(args)
        self_hash = ""

        if self.ignore_args:
            for curr, idx in enumerate(sorted(self.ignore_args)):
                args.pop(idx - curr)

        if self.hash_self:
            self_hash = str(hash(args.pop(0)))+"-"

        key = self_hash + generate_md5_hash(args, **kwargs)
        output_path = os.path.join(self.cache_dir, key)

        if os.path.exists(output_path):
            return dill.load(open(output_path, 'rb'))

        output = self.function(*args_copy, **kwargs)
        dill.dump(output, open(output_path, "wb+"))

        return output


def Cache(
    function=None,
    cache_dir="./cache",
    compress=False,
    hash_self=False,
    ignore_args: List[int] = None,
):
    if function:
        return _Cache(function)
    else:
        def wrapper(fun):
            return _Cache(fun, cache_dir, compress, hash_self, ignore_args)

        return wrapper
