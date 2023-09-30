# WIP: unit test case generator for python in golang style


now it geneates for python function:

```python
def kek(arg1: int, arg2: str) -> str:
    return str(arg1) + arg2

```

source code like this:

```python
    def test_kek():
        @dataclass
        class Args:
            arg1: int
            arg2: str


        @dataclass
        class Test:
            name: str
            args: Args
            want: str

        cases: tuple[Test] = (
            # TODO: add cases here
        )
        for case in cases:
            if (v := func(*case.args)) != case.want:
                print(f"{func.__name__()} got {v} wanted {case.want}")
```

