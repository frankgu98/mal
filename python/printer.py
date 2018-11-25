def pr_str(mal_ast):
    if mal_ast.type == "symbol":
        return mal_ast.value
    elif mal_ast.type == "int":
        return str(mal_ast.value)
    elif mal_ast.type == "list":
        return f'({ " ".join(map(pr_str, mal_ast.value)) })'
