def READ(s):
    return s

def EVAL(s):
    return s

def PRINT(s):
    print(s)

def rep(s):
    return PRINT(EVAL(READ(s)))

while True:
    print("user> ", end="")
    try:
        rep(input())
    except EOFError:
        print()
        break

