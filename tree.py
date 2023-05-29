from sys import argv

class Node:
    def __init__(self, val):
        self.left = None
        self.right = None
        self.val = val

    def set_left(self, left):
        self.left = left

    def set_right(self, right):
        self.right = right

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def set_val(self, val):
        self.val = val

    def get_val(self):
        return self.val    

class Tree:
    def __init__(self):
        self.root = None

    def add(self, val):
        if self.root is None:
            self.root = Node(val)
            return
        


if __name__ == "__main__":
    if len(argv) == 1:
        print(f"Invalid usage: python3 {argv[0]} <expr>")
        exit(-1)
    expr = argv[1]
    print(f"expr: {expr}")
    