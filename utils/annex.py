# import functools

# ls = [True, False, False, True, False, True, False]

# print( functools.reduce( lambda x, y: (x or y), ls))

x = True

def f():
    print("yo")

def ff():
    print("mo")
    
f() if x else ff()
