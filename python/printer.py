def pr_str(ast):
    if ast.type == "symbol":
        return ast.value
    elif ast.type == "int":
        return str(ast.value)
    elif ast.type == "list":
        return f'({ " ".join(map(pr_str, ast.value)) })'
