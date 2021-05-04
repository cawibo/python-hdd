import sys
import ast, astor

from hdd import hdd

source = """
def foo(a, b=None):
    print("asdddddd")

a = 10
foo(a)
c = 23
print(c)
print("as", end="")
print("df", end="")
"""

my_ast = ast.parse(source)

res = hdd(my_ast)

# exec(compile(res, filename='<ast>', mode='exec'))

print("Source Before:")
print(source)

after = astor.to_source(res)
print("Source After:")
print(after)