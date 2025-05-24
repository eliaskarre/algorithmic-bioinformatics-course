def cycle_to_chromosome(nodes):
    chromosome = []
    for j in range(0, len(nodes), 2):
        if nodes[j] < nodes[j + 1]:
            chromosome.append(nodes[j + 1] // 2)
        else:
            chromosome.append(-nodes[j] // 2)
    return chromosome

def is_black_edge(u, v):
    return abs(u - v) == 1 and (min(abs(u), abs(v)) % 2 == 1)

def graph_to_genome(adj):

    visited = set()
    genome = []
    for start in adj:
        if start in visited:
            continue

        #Zyklus finden
        cycle = []
        curr = start
        prev = None
        while True:
            cycle.append(curr)
            visited.add(curr)

            nbrs = adj[curr]
            #wähle nächsten Nachbarn, der nicht prev ist
            nxt = nbrs[0] if nbrs[0] != prev else nbrs[1]

            prev, curr = curr, nxt
            if curr == start:
                break

        #Zyklus so rotieren
        
        L = len(cycle)
        for _ in range(L):
            if is_black_edge(cycle[0], cycle[1]):
                break
            cycle = cycle[1:] + cycle[:1]
        
        #In Chromosom umwandeln
        chrom = cycle_to_chromosome(cycle)
        genome.append(chrom)

    return genome

def black_edges(genome):
    edges = []
    for chrom in genome:
        nodes = chromosome_to_cycle(chrom)
      
        for i in range(0, len(nodes), 2):
            head = nodes[i]
            tail = nodes[i+1]
            edges.append((head, tail))
    return edges

def remove_edge(adj, a, b):
    if b in adj.get(a, []):
        adj[a].remove(b)
    if a in adj.get(b, []):
        adj[b].remove(a)

def add_edge(adj, a, b):
    adj.setdefault(a, []).append(b)
    adj.setdefault(b, []).append(a)


def two_break_on_genome_graph(GenomeGraph, i, j, k, l):
  remove_edge(GenomeGraph, i, j)
  remove_edge(GenomeGraph, k, l)

  add_edge(GenomeGraph, i, k)
  add_edge(GenomeGraph, j, l)

  return GenomeGraph

def two_break_on_genome(P, i, j, k, l):
  
  colored = colored_edges(P)
  #print(colored)
  black = black_edges(P)
  #print(black)

  adj = {}
  for x,y in colored + black:
      adj.setdefault(x, []).append(y)
      adj.setdefault(y, []).append(x)

  #print("Vorher:", dict(adj))
  new = two_break_on_genome_graph(adj, i, j, k, l)
  #print("Nachher:", dict(new))
  
  genome = graph_to_genome(new)

  return genome
  #return adj

if __name__ == "__main__":
    P = [[
        +1,+2,+3,-4,-5,-6,+7,-8,+9,-10,-11,-12,-13,-14,
        +15,+16,+17,-18,+19,+20,-21,-22,-23,-24,+25,-26,
        -27,+28,-29,+30,+31,-32,+33,-34,+35,-36,-37,+38,
        -39,+40,-41,-42,+43,-44,+45,+46,+47,-48,+49,+50,
        -51,-52,-53,+54,+55,+56,+57,+58,-59,-60,+61,+62,
        +63,-64,+65,-66,-67,+68
    ]]

    i, j = 104, 101
    k, l = 102, 100

    print(two_break_on_genome(P, i, j, k, l))
