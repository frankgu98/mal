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

class MalToken():
    def __init__(self, type_, value):
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
    token = read_atom(reader)
    if token.type == "symbol" and token.value == "(":
        tokens = MalToken("list", [])
        tokens.value.extend(read_list(reader).value)
        return tokens
    else:
        return token
    

def read_list(reader):
    # TODO: try except 
    tokens = MalToken("list", [])
    while True:
        token = read_form(reader)
        if token.type == "symbol" and token.value == ")":
            return tokens
        else:
            tokens.value.append(token)

# base case of the mutually recursive read_form() and read_list()
def read_atom(reader):
    token_value = reader.next()
    if can_be_type(int, token_value):
        return MalToken("int", int(token_value))
    else: # not convertible to int, assume it's a symbol
        return MalToken("symbol", token_value)


if __name__ == "__main__":
    tokens = tokenizer("(123 456)")
    
    assert(tokens == ["(", "123", "456", ")", ""])

    tokens = tokenizer("((123 456) 5)")
    reader = Reader(tokens)
    form = read_form(reader)
    print(form)
