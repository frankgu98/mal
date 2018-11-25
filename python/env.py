
class Env:
    def __init__(self, outer=None, data={}):
        self.outer = outer
        self.data = dict(data) # copies to avoid references

    def set(self, symbol, mal_s_exp):
        self.data[symbol] = mal_s_exp

    def find(self, symbol):
        if symbol in self.data.keys():
            return self
        elif self.outer is not None:
            return self.outer.find(symbol)
        return None

    def get(self, symbol):
        env = self.find(symbol)
        if env is None:
            raise Exception(f"'{symbol}' not found.")
        return env.data[symbol]
