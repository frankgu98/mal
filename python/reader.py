import re

class Reader():
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
    
    def next(self):
        self.position += 1
        return self.tokens[self.position - 1]

    def peek(self):
        return self.tokens[self.position]


class MalAST():
    def __init__(self, type_, value):
        """
        ASTs
            atoms
                symbol, int
            lists
                list

        token
            any string in the program, no "meaning" yet
        """
        self.type = type_
        self.value = value


def read_str(s):
    reader = Reader(tokenizer(s))
    return read_form(reader)


def tokenizer(s):
    # re.split() vs re.findall() for later??
    # TODO: implement without regex later
    return re.findall(r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"|;.*|[^\s\[\]{}('"`,;)]*)""", s)


def can_be_type(cast_function, s):
    try:
        cast_function(s)
        return True
    except ValueError:
        return False


def read_form(reader):  
    mal_atom = read_atom(reader)
    if mal_atom.type == "symbol" and mal_atom.value == "(":
        mal_list = MalAST("list", [])
        mal_list.value.extend(read_list(reader).value)
        return mal_list
    else:
        return mal_atom
    

def read_list(reader):
    # TODO: try except 
    mal_list = MalAST("list", [])
    while True:
        mal_ast = read_form(reader)
        if mal_ast.type == "symbol" and mal_ast.value == ")":
            return mal_list
        else:
            mal_list.value.append(mal_ast)

# base case of the mutually recursive read_form() and read_list()
def read_atom(reader):
    token = reader.next()
    if can_be_type(int, token):
        return MalAST("int", int(token))
    else: # not convertible to int, assume it's a symbol
        return MalAST("symbol", token)


if __name__ == "__main__":
    tokens = tokenizer("(123 456)")
    
    assert(tokens == ["(", "123", "456", ")", ""])

    tokens = tokenizer("((123 456) 5)")
    reader = Reader(tokens)
    ast = read_form(reader)
    print(ast)
