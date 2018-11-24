import reader
import printer

def READ(s):
    return reader.read_str(s)

def EVAL(token):
    return token

def PRINT(token):
    print(printer.pr_str(token))

def rep(s):
    return PRINT(EVAL(READ(s)))

while True:
    print("user> ", end="")
    try:
        rep(input())
    except EOFError:
        print()
        break
