import sys
import re
from collections import defaultdict

class Node:
    def __init__(self, name=None, length=None):
        self.children = []
        self.name = name
        self.length = length

    def is_leaf(self):
        return len(self.children) == 0

    def __str__(self):
        inner = ""
        if not self.is_leaf():
            inner = "(" + ",".join(str(c) for c in self.children) + ")"
        if self.name is not None:
            inner += self.name
        if self.length is not None:
            inner += f":{self.length}"
        return inner

def parse_newick(s, tokens=None, pos=0):

    if tokens is None:
        tokens = re.findall(r"\(|\)|,|:|;|[^():,;]+", s.strip())
        root, pos = parse_newick(s, tokens, 0)
        return root

    if tokens[pos] == "(":
        node = Node()
        pos += 1  

        child, pos = parse_newick(s, tokens, pos)
        node.children.append(child)

        while tokens[pos] == ",":
            pos += 1
            child, pos = parse_newick(s, tokens, pos)
            node.children.append(child)
        pos += 1  

        if pos < len(tokens) and re.match(r"[^(),:;]+", tokens[pos]):
            node.name = tokens[pos]
            pos += 1

        if tokens[pos] == ":":
            pos += 1
            node.length = float(tokens[pos])
            pos += 1

        return node, pos
    else:
        leaf = Node(name=tokens[pos])
        pos += 1

        if tokens[pos] == ":":
            pos += 1
            leaf.length = float(tokens[pos])
            pos += 1

        return leaf, pos

def assign_internal_names(node, existing_names, counter):
    if node.name is None:
        while True:
            candidate = f"Internal{counter[0]}"
            counter[0] += 1
            if candidate not in existing_names:
                break
        node.name = candidate
        existing_names.add(candidate)
    for child in node.children:
        assign_internal_names(child, existing_names, counter)

def build_adjacency(node, parent=None, adj=None):
    if adj is None:
        adj = defaultdict(list)

    if parent is not None:
        length = node.length if node.length is not None else 0.0
        adj[node.name].append((parent.name, length))
        adj[parent.name].append((node.name, length))

    for child in node.children:
        build_adjacency(child, node, adj)

    return adj

def print_adjacency_table(adj):
    edge_list = []
    for u in adj:
        for v, length in adj[u]:
            if u < v:
                edge_list.append((u, v, length))
    edge_list.sort(key=lambda x: (x[0], x[1]))
    print("node1 node2 length")
    for u, v, length in edge_list:
        print(f"{u} {v} {length}")

def print_degree_table(adj):
    print()
    print("degrees table:")
    print("node degree")
    for node in sorted(adj.keys()):
        print(f"{node} {len(adj[node])}")

def main():
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        newick_str = f.read().strip()

    tree = parse_newick(newick_str)

    print("Parsed tree")
    print(str(tree) + ";")
    print()

    existing_names = set()
    def collect_names(n):
        if n.name is not None:
            existing_names.add(n.name)
        for c in n.children:
            collect_names(c)
    collect_names(tree)

    assign_internal_names(tree, existing_names, counter=[1])

    adj = build_adjacency(tree)

    print("Adjacency table:")
    print_adjacency_table(adj)

    print_degree_table(adj)

if __name__ == "__main__":
    main()
