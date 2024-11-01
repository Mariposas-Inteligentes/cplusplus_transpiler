import networkx as nx
import matplotlib.pyplot as plt

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
    
    def add_to_graph(self, graph, parent_id=None):
        node_id = id(self)
        label = f"{self.n_type}\nValue: {self.value}" if self.value else self.n_type
        graph.add_node(node_id, label=label)

        if parent_id is not None:
            graph.add_edge(parent_id, node_id)

        for child in self.children:
            child.add_to_graph(graph, node_id)

    def visualize(self):
        G = nx.DiGraph()
        self.add_to_graph(G)

        pos = self._hierarchical_layout(G, id(self))
        labels = nx.get_node_attributes(G, 'label')

        plt.figure(figsize=(10, 8))
        nx.draw(
            G, 
            pos, 
            labels=labels, 
            with_labels=True, 
            node_size=2000, 
            node_color="lightblue", 
            font_size=8, 
            font_color="black", 
            arrows=False
        )
        plt.title("Mariposas Inteligentes: AST")
        plt.show()

    def _hierarchical_layout(self, G, root):
        layers = self._bfs_layers(G, root)
        pos = {}
        for depth, layer in enumerate(layers):
            for i, node in enumerate(layer):
                pos[node] = (i - len(layer) / 2, -depth)
        return pos

    def _bfs_layers(self, G, root):
        layers = []
        visited = set()
        queue = [(root, 0)]
        current_layer = []
        current_depth = 0
        while queue:
            node, depth = queue.pop(0)
            if depth != current_depth:
                layers.append(current_layer)
                current_layer = []
                current_depth = depth
            current_layer.append(node)
            visited.add(node)
            for neighbor in G.neighbors(node):
                if neighbor not in visited:
                    queue.append((neighbor, depth + 1))
        if current_layer:
            layers.append(current_layer)
        return layers