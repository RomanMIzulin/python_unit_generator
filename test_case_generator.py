import inspect
from dataclasses import dataclass, make_dataclass
from typing import NewType


def generate_test_case(func):
    sig: inspect.Signature = inspect.signature(func)
    input_ = sig.parameters
    output_type = NewType("output_type", sig.return_annotation)
    args_type = make_dataclass("args", [(k, v.annotation) for k, v in input_.items()], slots=True)

    def test_func():
        @dataclass
        class Args:
            args_here

        @dataclass
        class Test:
            name: str
            args: Args
            want: output_type

        cases: tuple[Test] = (
            # TODO: add cases here
        )
        for case in cases:
            if (v := func(*case.args)) != case.want:
                print(f"{func.__name__()} got {v} wanted {case.want}")

    test_func.__name__ = f"test_{func.__name__}"

    #args_txt = '\n'.join([str(v) for k,v in sig.parameters.items()[]])
    args_txt = ''
    cnt=0
    for k,v in sig.parameters.items():
        if cnt!=0:
            args_txt += ' '*12+str(v)+'\n'
        else:
            args_txt = str(v)+'\n'
            cnt+=1

    return (
        inspect.getsource(test_func)
        .replace("test_func", f"test_{func.__name__}")
        .replace("output_type", sig.return_annotation.__name__)
        .replace('args_here',args_txt)
    )


def kek(arg1: int, arg2: str) -> str:
    return str(arg1) + arg2


print(generate_test_case(kek))
