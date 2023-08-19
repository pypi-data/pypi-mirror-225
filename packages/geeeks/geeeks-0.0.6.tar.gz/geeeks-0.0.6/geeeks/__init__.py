class StringFunctions:
    def reverse_str(self, data):
        return "".join(list(data)[::-1])
    
    def make_link(self, line):
        return "-".join(line.lower().split(" "))