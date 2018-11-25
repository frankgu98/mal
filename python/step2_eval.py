import sys, traceback
import reader
import printer


def READ(s):
    return reader.read_str(s)

def EVAL(mal_s_expression, repl_env):
    if mal_s_expression.type == "list":
        if len(mal_s_expression.value) == 0:
            return mal_s_expression
        else:
            evaluated_list = eval_ast(mal_s_expression, repl_env)
            function = repl_env[evaluated_list[0].value]
            arguments = evaluated_list[1:]
            # takes type from first argument
            return reader.MalSExpression(arguments[0].type, function(*arguments))

    return eval_ast(mal_s_expression, repl_env)

def PRINT(mal_s_expression):
    print(printer.pr_str(mal_s_expression))

def rep(s, repl_env):
    return PRINT(EVAL(READ(s), repl_env))

def eval_ast(mal_s_expression, repl_env):
    if mal_s_expression.type == "symbol":
        if mal_s_expression.value in repl_env.keys():
            return mal_s_expression
        else:
            raise Exception(f"'{mal_s_expression.value}' not found.")
    
    elif mal_s_expression.type == "list":
        return [EVAL(token, repl_env) for token in mal_s_expression.value]

    return mal_s_expression


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
