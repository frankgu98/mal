def pr_str(mal_s_exp):
    if mal_s_exp.type == "symbol" or mal_s_exp.type == "int":
        return str(mal_s_exp.value)
    elif mal_s_exp.type == "list":
        return f'({ " ".join(map(pr_str, mal_s_exp.value)) })'
