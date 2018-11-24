def pr_str(token):
    if token.type == "symbol" or token.type == "int":
        return token.value
    elif token.type == "list":
        return "(" + " ".join(map(pr_str, token.value)) + ")"
