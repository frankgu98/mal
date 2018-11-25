import sys, traceback
import reader
import printer


def READ(s):
    return reader.read_str(s)

def EVAL(mal_ast, repl_env):
    if mal_ast.type == "list":
        if len(mal_ast.value) == 0:
            return mal_ast
        else:
            evaluated_list = eval_ast(mal_ast, repl_env)
            function = repl_env[evaluated_list[0].value]
            arguments = evaluated_list[1:]
            # takes type from first argument
            return reader.MalAST(arguments[0].type, function(*arguments))

    return eval_ast(mal_ast, repl_env)

def PRINT(mal_ast):
    print(printer.pr_str(mal_ast))

def rep(s, repl_env):
    return PRINT(EVAL(READ(s), repl_env))

def eval_ast(mal_ast, repl_env):
    if mal_ast.type == "symbol":
        if mal_ast.value in repl_env.keys():
            return mal_ast
        else:
            raise Exception(f"'{mal_ast.value}' not found.")
    
    elif mal_ast.type == "list":
        return [EVAL(token, repl_env) for token in mal_ast.value]

    return mal_ast


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
