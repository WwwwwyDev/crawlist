from inspect import signature


class ParamsTypeError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


def check(exclude: list | str):
    """
    Turn the function into a strongly typed function, check if the parameter type is legal, and if not, directly assert.
    \n You could use @check to Turn the function into a strongly typed function.
    :param exclude: Sort the parameters that need to be checked
    :return: Decorator
    """
    if not callable(exclude):
        if exclude is None:
            exclude = []
        assert isinstance(exclude, list) or isinstance(exclude, str)
        if isinstance(exclude, str):
            exclude = [exclude]
        exclude = set(exclude)

    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            args_dict = {}
            index = 0
            for name, type_ in signature(func).parameters.items():
                if name in kwargs:
                    break
                if index >= len(args) and type_.default:
                    args_dict[name] = type_.default
                    continue
                args_dict[name] = args[index]
                index += 1
            all_kwargs = {**args_dict, **kwargs}
            for name, type_ in signature(func).parameters.items():
                if not callable(exclude) and name in exclude:
                    continue
                if name == "self":
                    continue
                if isinstance(all_kwargs[name], int) and type_.annotation is float:
                    all_kwargs[name] = float(all_kwargs.get(name))
                if isinstance(all_kwargs[name], float) and type_.annotation is int:
                    all_kwargs[name] = int(all_kwargs.get(name))
                if not isinstance(all_kwargs[name], type_.annotation):
                    raise ParamsTypeError(f"Parameter {name} must be {type_.annotation}.")
            return func(*args, **kwargs)

        return inner_wrapper

    if callable(exclude):
        return wrapper(exclude)
    return wrapper
