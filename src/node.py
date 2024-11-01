class Node:
    def __init__(self, n_type, children=None, value=None):
        self.n_type = n_type
        self.children = children if children else []
        self.value = value
        
    def __str__(self, level=0):
        indent = "  " * level
        result = f"{indent}Node(type={self.n_type}, value={self.value})\n"
        for child in self.children:
            result += child.__str__(level + 1)
        return result