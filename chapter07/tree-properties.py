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

def find_farthest(start, adj):

    visited = set()
    parent = {}
    dist = {}

    dist[start] = 0.0
    parent[start] = None
    stack = [start]

    while stack:
        u = stack.pop()
        visited.add(u)
        for (v, w) in adj[u]:
            if v not in visited:
                new_dist = dist[u] + w
                if v not in dist or new_dist > dist[v]:
                    dist[v] = new_dist
                    parent[v] = u
                    stack.append(v)

    farthest_node = max(dist.keys(), key=lambda x: dist[x])
    return farthest_node, dist[farthest_node], parent

def recover_path(a, b, parent_map):
    path = []
    cur = b
    while cur is not None:
        path.append(cur)
        cur = parent_map[cur]
    path.reverse()
    return path

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
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <input_newick_file>")
        sys.exit(1)

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

    leaves = [n for n in adj if len(adj[n]) == 1]
    if not leaves:
        print("\nNo leaves found.")
        return

    arbitrary_leaf = leaves[0]

    A, distA, parentA = find_farthest(arbitrary_leaf, adj)

    B, diameter, parentB = find_farthest(A, adj)

    path_A_to_B = recover_path(A, B, parentB)

    print()
    print(f"Diameter of the tree: {diameter}")
    print("Longest path from leaf to leaf:")
    print(" -> ".join(path_A_to_B))

    half_dist = diameter / 2.0

    edge_length = {}
    for u in adj:
        for v, w in adj[u]:
            edge_length[(u, v)] = w

    cum_dist = 0.0
    midpoint_edge = None
    for i in range(len(path_A_to_B) - 1):
        u = path_A_to_B[i]
        v = path_A_to_B[i + 1]
        w = edge_length[(u, v)]
        if cum_dist + w >= half_dist:
            midpoint_edge = (u, v)
            break
        cum_dist += w

    if midpoint_edge:
        u, v = midpoint_edge
        print(f"Mid-point root would lie on the branch between {u} and {v}.")
    else:
        print("Mid-point lies exactly at a node (no single branch).")

if __name__ == "__main__":
    main()
