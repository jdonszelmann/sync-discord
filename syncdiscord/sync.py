import asyncio
from typing import Coroutine
from inspect import iscoroutinefunction, isfunction

eventloop = asyncio.get_event_loop()

syncclasses = {}


def syncargwrapper(func):
    def result_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TypeError:
            # Maybe the first arg had to be a coroutine so wrap it in one
            if not isfunction(args[0]):
                raise

            # TODO: maybe try all combinations of *args until no typeerror occurs
            async def async_wrapper(*async_args, **async_kwargs):
                return args[0](*async_args, **async_kwargs)

            return func(async_wrapper, *args[1:], **kwargs)


    return result_function


def syncwrapper(func: Coroutine):
    def result_function():
        result = eventloop.run_until_complete(func)
        if result.__class__ in syncclasses:
            result.__class__ = syncclasses[result.__class__]

    return syncargwrapper(result_function)


def make_sync(cls):
    global syncclasses

    newdict = {}
    for key, value in cls.__dict__.items():
        if iscoroutinefunction(value):
            newdict[key] = syncwrapper(value)
        else:
            newdict[key] = syncargwrapper(value)

    newcls = type(
        cls.__name__,
        (cls,),
        newdict
    )

    syncclasses[cls] = newcls

    return newcls
