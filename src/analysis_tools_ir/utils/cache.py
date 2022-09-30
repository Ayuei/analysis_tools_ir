import functools
import os
import weakref
from inspect import signature

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
            is_instance=False,
    ):
        self.cache_dir = cache_dir
        self.hash_self = hash_self
        self.compress = compress
        self.function = function
        self.ignore_args = ignore_args
        self.is_instance = is_instance

        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def __call__(self, *args, instance=None, **kwargs):
        if 'disable_cache' in kwargs and kwargs['disable_cache']:
            kwargs.pop('disable_cache')
            if instance:
                args = list(args)
                args.insert(0, instance)

            return self.function(*args, **kwargs)

        args = list(args)

        if self.ignore_args:
            for curr, idx in enumerate(sorted(self.ignore_args)):
                args.pop(idx - curr)

        if self.hash_self and self.is_instance:
            self_hash = str(hash(instance)) + "-"
        else:
            str_params = ",".join(signature(self.function).parameters)
            self_hash = generate_md5_hash(self.function.__name__+str_params)

        key = self_hash + generate_md5_hash(args, **kwargs)
        output_path = os.path.join(self.cache_dir, key)

        if os.path.exists(output_path):
            print("called")
            return dill.load(open(output_path, 'rb'))

        if instance:
            args.insert(0, instance)

        output = self.function(*args, **kwargs)
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
        has_self = 'self' in signature(function).parameters

        if has_self:
            c = _Cache(function, cache_dir, compress,
                       hash_self, ignore_args, is_instance=True)

            @functools.wraps(function)
            def wrapper(self, *args, **kwargs):
                return c(*args, instance=weakref.ref(self)(), **kwargs)

            return wrapper
        else:
            return _Cache(function,
                          cache_dir="./cache",
                          compress=False,
                          hash_self=False,
                          ignore_args=None)
    else:
        def wrapper(fun):
            return Cache(fun, cache_dir, compress, hash_self, ignore_args)

        return wrapper


#if __name__ == "__main__":
#    class Tester:
#        def __init__(self):
#            self.lst = []
#
#        @Cache
#        def add(self, item=0):
#            self.lst.append(item)
#            return self.lst
#
#
#    t = Tester()
#    t.add()
#    t.add(1)
#    t.add(2)
#    t.add(2)
#
#    print(t.lst)
#
#    @Cache
#    def tester(number):
#        return number+1
#
#    print(tester(1))
#    print(tester(1))
#    print(tester(2))
#