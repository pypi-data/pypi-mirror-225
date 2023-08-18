import inspect
import typing
from functools import wraps


def _find_type_origin(type_hint):
    if isinstance(type_hint, typing._SpecialForm):
        # case of typing.Any, typing.ClassVar, typing.Final, typing.Literal,
        # typing.NoReturn, typing.Optional, or typing.Union without parameters
        return

    actual_type = typing.get_origin(type_hint) or type_hint  # requires Python 3.8
    if isinstance(actual_type, typing._SpecialForm):
        # case of typing.Union[…] or typing.ClassVar[…] or …
        for origins in map(_find_type_origin, typing.get_args(type_hint)):
            yield from origins
    else:
        yield actual_type


def _check_types(func, parameters, hints):
    for name, value in parameters.items():
        type_hint = hints.get(name, object)
        actual_types = tuple(_find_type_origin(type_hint))
        if actual_types and not isinstance(value, actual_types):
            raise TypeError(
                f"Problem on function {func.__name__}, Expected type '{type_hint}' for argument '{name}' but received type"
                f" '{type(value)}' instead"
            )


def enforce_types(callable):
    def decorate(func):
        hints = typing.get_type_hints(func)
        signature = inspect.signature(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            parameters = dict(zip(signature.parameters, args))
            parameters.update(kwargs)
            _check_types(callable, parameters, hints)

            return func(*args, **kwargs)

        return wrapper

    if inspect.isclass(callable):
        callable.__init__ = decorate(callable.__init__)
        return callable

    return decorate(callable)


def enforce_strict_types(callable):
    def decorate(func):
        hints = typing.get_type_hints(func)
        signature = inspect.signature(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound = signature.bind(*args, **kwargs)
            bound.apply_defaults()
            parameters = dict(zip(signature.parameters, bound.args))
            parameters.update(bound.kwargs)
            _check_types(callable, parameters, hints)

            return func(*args, **kwargs)

        return wrapper

    if inspect.isclass(callable):
        callable.__init__ = decorate(callable.__init__)
        return callable

    return decorate(callable)
