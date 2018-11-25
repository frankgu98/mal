import sys, traceback
import reader
import printer


def READ(s):
    return reader.read_str(s)

def EVAL(ast, repl_env):
    if ast.type == "list":
        if len(ast.value) == 0:
            return ast
        else:
            evaluated_list = eval_ast(ast, repl_env)
            function = repl_env[evaluated_list[0].value]
            arguments = evaluated_list[1:]
            # takes type from first argument
            return reader.MalToken(arguments[0].type, function(*arguments))

    return eval_ast(ast, repl_env)

def PRINT(ast):
    print(printer.pr_str(ast))

def rep(s, repl_env):
    return PRINT(EVAL(READ(s), repl_env))

def eval_ast(ast, repl_env):
    if ast.type == "symbol":
        if ast.value in repl_env.keys():
            return ast
        else:
            raise Exception(f"'{ast.value}' not found.")
    
    elif ast.type == "list":
        return [EVAL(token, repl_env) for token in ast.value]

    return ast


repl_env = {'+': lambda a,b: a.value+b.value,
            '-': lambda a,b: a.value-b.value,
            '*': lambda a,b: a.value*b.value,
            '/': lambda a,b: int(a.value/b.value)}

while True:
    print("user> ", end="")
    try:
        rep(input(), repl_env)
    except EOFError:
        print("Exiting.")
        break
    except Exception as e:
        print("".join(traceback.format_exception(*sys.exc_info())))
