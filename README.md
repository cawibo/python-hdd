# HDD with ddminish

This is an implementation of Hierarchical Delta Debugging in Python. The pruning/ testing phase utilizes a total search instead of Andreas Zeller's ddmin, as a result, it is easier to understand and implement but not as efficient.

## How to use

In its current state, the structure is hard coded to listen for 'asdf'. If the string is found, then the test will pass, otherwise it will fail and reattempt with another configuration.

`python3 src/main.py`

### Example

```bash
$ python3 src/main.py
Source Before:
def foo(a, b=None):
print("asdddddd")

a = 10
foo(a)
c = 23
print(c)
print("as", end="")
print("df", end="")

Source After:
print('as', end='')
print('df', end='')
```

## How to run tests

`python3 -m unittest discover`
