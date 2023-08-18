# PyCodeCage

PyCodeCage is a Python library for running code in a sandboxed environment.

## Installation

Use the package manager pip to install PyCodeCage.

```bash
pip install PyCodeCage
```

## Example

```python
from pycodecage import TestCase, TrustedEnvironment, run_tests

code = """
a = int(input("Enter an integer:"))

if a % 2 != 0 and a > 20:
    print("Not Weird")
elif a % 2 != 0:
    print("Weird")
elif a % 2 == 0 and 2 <= a <= 5:
    print("Not Weird")
elif a % 2 == 0 and 6 <= a <= 20:
    print("Weird")
"""

env = TrustedEnvironment(code)
tests = [
    TestCase('test1', [1], ['Weird']),
    TestCase('test2', [3], ['Weird']),
    TestCase('test3', [2], ['Not Weird']),
    TestCase('test4', [4], ['Not Weird']),
    TestCase('test5', [6], ['Weird']),
    TestCase('test6', [8], ['Weird']),
    TestCase('test7', [20], ['Weird']),
    TestCase('test8', [39], ['Not Weird']),
]
run_tests(tests, env)
```


