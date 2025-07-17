import sys
import re
from collections import defaultdict, deque
##
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

def get_leaf_names(node, leaf_list):

    if node.is_leaf():
        leaf_list.append(node.name)
    else:
        for c in node.children:
            get_leaf_names(c, leaf_list)

def compute_pairwise_leaf_distances(leaf_names, adj):

    distances = {leaf: {} for leaf in leaf_names}

    for leaf in leaf_names:
        # BFS
        queue = deque()
        queue.append((leaf, 0.0))
        visited = set([leaf])

        while queue:
            current, dist_so_far = queue.popleft()
            
            if current in distances and current != leaf:
                distances[leaf][current] = dist_so_far

            for (neighbor, length) in adj[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist_so_far + length))

    return distances

def print_leaf_distance_table(distances):
    entries = []
    for u in distances:
        for v, d in distances[u].items():
            if u < v:
                entries.append((u, v, d))

    entries.sort(key=lambda x: (x[0], x[1]))

    print("leaf1 leaf2 distance")
    for (u, v, d) in entries:
        print(f"{u} {v} {d:.1f}")

    return [d for (u, v, d) in entries]

def main():
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        newick_str = f.read().strip()

    tree = parse_newick(newick_str)

    existing_names = set()
    def collect_names(n):
        if n.name is not None:
            existing_names.add(n.name)
        for c in n.children:
            collect_names(c)
    collect_names(tree)
    assign_internal_names(tree, existing_names, counter=[1])

    adj = build_adjacency(tree)

    leaf_names = []
    get_leaf_names(tree, leaf_names)
    leaf_names.sort()

    distances = compute_pairwise_leaf_distances(leaf_names, adj)

    print("Leaf‐Pair Distances:")
    dist_list = print_leaf_distance_table(distances)

    min_d = min(dist_list)
    max_d = max(dist_list)
    mean_d = sum(dist_list) / len(dist_list)

    print()
    print(f"min distance: {min_d:.1f}")
    print(f"max distance: {max_d:.1f}")
    print(f"mean distance: {mean_d:.6f}")

if __name__ == "__main__":
    main()
