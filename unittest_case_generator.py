import inspect
from dataclasses import dataclass
from typing import Any, Callable, TypeVar, ParamSpec


ReturnType = TypeVar("ReturnType")  # the callable/awaitable return type
Param = ParamSpec("Param")  # the callable parameters



class NotFullyTypedError(Exception):
    """Raised when a function is not fully typed."""

    pass



def generate_test_case(func: Callable[Param, ReturnType]) -> str: # type: ignore
    sig: inspect.Signature = inspect.signature(func)

    # check if all parameters are annotated
    for param in sig.parameters.values():
        if param.annotation is inspect.Parameter.empty:
            raise NotFullyTypedError(
                f"Parameter '{param.name}' of function '{func.__name__}' is not typed"
            )
    # Check if return type is annotated
    if sig.return_annotation is inspect.Signature.empty:
        raise NotFullyTypedError(f"Return type of function '{func.__name__}' is not typed")

    def test_func():
        @dataclass
        class Args:
            ...

        @dataclass
        class Test:
            name: str
            args: Args
            want: ReturnType

        cases: tuple[Test] = (  # type: ignore
            # TODO: add cases here
        )
        print(f"running cases for {func.__name__} function")
        for case in cases:
            if (v := func(*case.args)) != case.want: # type: ignore
                print(f"{case.name} {func.__name__} got {v} wanted {case.want}")

    test_func.__name__ = f"test_{func.__name__}"

    args_txt = ""
    cnt = 0
    for _, v in sig.parameters.items():
        if cnt != 0:
            args_txt += " " * 12 + str(v) + "\n"
        else:
            args_txt = str(v) + "\n"
            cnt += 1

    return (
        inspect.getsource(test_func)
        .replace("test_func", f"test_{func.__name__}")
        .replace("ReturnType", sig.return_annotation.__name__)
        .replace("...", args_txt)
        .replace("# type: ignore", "")
    )

def save_to_file(func: Callable[Param, Any], file_path: str| None):
    # by default to the same directory where funtion is defined
    if file_path is None:
        file_path = inspect.getfile(func).replace(".py", "_test.py")
    with open(file_path, "w") as f:
        f.write(generate_test_case(func))

def append_to_file(file_path: str, func: Callable[Param, Any]):
    with open(file_path, "a") as f:
        f.write('\n\n')
        f.write(generate_test_case(func))

def kek(foo: int, bar: str) -> str:
    return str(foo) + bar

if __name__ == "__main__":
    print(generate_test_case(kek))
