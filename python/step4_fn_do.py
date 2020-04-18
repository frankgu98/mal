import sys, traceback
import reader
import printer
import env

def READ(s):
    return reader.read_str(s)

# eventually returns a python value
def EVAL(mal_s_exp, cur_env):
    if mal_s_exp.type == "list":
        if len(mal_s_exp.value) == 0:
            return mal_s_exp

        # can't eval list to use "def!" and "let*" as function since may not want to evaluate all arguments
        if mal_s_exp.value[0].value == "def!":
            variable_name = mal_s_exp.value[1].value # a MalSExpression symbol's variable name is stored in it's value field 
            variable_value = EVAL(mal_s_exp.value[2], cur_env)
            cur_env.set(variable_name, variable_value)
            return variable_value

        elif mal_s_exp.value[0].value == "let*":
            new_env = env.Env(outer=cur_env)
            mal_list = mal_s_exp.value[1].value
            if len(mal_list)%2 != 0:
                raise Exception("Need an assignment for each variable in new environment")

            bindings = iter(mal_list)
            for binding in bindings:
                variable_name = binding.value # a MalSExpression symbol's variable name is stored in it's value field 
                variable_value = EVAL(next(bindings), new_env)
                new_env.set(variable_name, variable_value)

            return EVAL(mal_s_exp.value[2], new_env)

        else:
            evaluated_list = eval_s_exp(mal_s_exp, cur_env).value
            # can go from MalSExpression to it's python function value here since no more unwrapping to do
            function = evaluated_list[0].value
            # arguments may still be MalSExpressions
            arguments = evaluated_list[1:]
            # takes type from first argument
            return reader.MalSExpression(arguments[0].type, function(*arguments))
    else:
        return eval_s_exp(mal_s_exp, cur_env)

def PRINT(mal_s_exp):
    print(printer.pr_str(mal_s_exp))

def rep(s, cur_env):
    PRINT(EVAL(READ(s), cur_env))

# always returns MalSExpressions
def eval_s_exp(mal_s_exp, cur_env):
    if mal_s_exp.type == "symbol":
        return cur_env.get(mal_s_exp.value)
        
    elif mal_s_exp.type == "list":
        list_value = [EVAL(s_exp, cur_env) for s_exp in mal_s_exp.value] # separated for debugging
        return reader.MalSExpression("list", list_value)

    return mal_s_exp


repl_env = env.Env()
repl_env.set("+", reader.MalSExpression("symbol", lambda a,b: a.value+b.value))
repl_env.set("-", reader.MalSExpression("symbol", lambda a,b: a.value-b.value))
repl_env.set("*", reader.MalSExpression("symbol", lambda a,b: a.value*b.value))
repl_env.set("/", reader.MalSExpression("symbol", lambda a,b: int(a.value/b.value)))

while True:
    print("user> ", end="")
    try:
        rep(input(), repl_env)
    except EOFError:
        print("Exiting.")
        break
    except Exception as e:
        print("".join(traceback.format_exception(*sys.exc_info())))

# (let* (z (+ 2 3)) (+ 1 z))