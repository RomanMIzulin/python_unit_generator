import inspect
from dataclasses import dataclass


class NotFullyTypedError(Exception):
    """Raised when a function is not fully typed."""

    pass


def generate_test_case(func):
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
            args_here  # type: ignore

        @dataclass
        class Test:
            name: str
            args: Args
            want: output_type  # type: ignore

        cases: tuple[Test] = (  # type: ignore
            # TODO: add cases here
        )
        print(f"running cases for {func.__name__()} function")
        for case in cases:
            if (v := func(*case.args)) != case.want:
                print(f"{case.name} {func.__name__()} got {v} wanted {case.want}")

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
        .replace("output_type", sig.return_annotation.__name__)
        .replace("args_here", args_txt)
    )

def save_to_file(func, file_path: str| None):
    # by default to the same directory where funtion is defined
    if file_path is None:
        file_path = inspect.getfile(func).replace(".py", "_test.py")
    with open(file_path, "w") as f:
        f.write(generate_test_case(func))

def append_to_file(file_path: str, func):
    with open(file_path, "a") as f:
        f.write('\n\n')
        f.write(generate_test_case(func))

def kek(arg1: int, arg2: str) -> str:
    return str(arg1) + arg2

if __name__ == "__main__":
    print(generate_test_case(kek))
