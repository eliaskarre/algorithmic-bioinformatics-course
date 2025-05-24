def colored_edges(genome):
    edges = []
    for chrom in genome:
        nodes = chromosome_to_cycle(chrom)

        for i in range(1, len(nodes), 2): #0 bis 1 wäre eine Black Edge, 1 bis 2 eine Red (Colored) -> also starten wir bei 1
            head = nodes[i]
            if i+1 < len(nodes):
                tail = nodes[i+1]
            else: #Wenn Ende erreicht, nimm die Erste Node als letzten Tail, da das Genom Zyklisch ist
                tail = nodes[0]
            edges.append((head, tail))

    return edges

def two_break_distance(P, Q):

    b = sum(len(chrom) for chrom in P) #Anzahl Synteny-Blöcke in P
    red = colored_edges(P)
    blue   = colored_edges(Q)

    #Adjazenzliste Breakpoint-Graph
    adj = {}
    for x,y in red + blue:
        adj.setdefault(x, []).append(y)
        adj.setdefault(y, []).append(x) #Ungeri­chteter Graph -> Adjazenzliste muss symmetrisch sein.
                                        # also in beide Richtungen
    #print(adj)


    #Zähle zyklen
    visited_nodes = set()
    cycle_count   = 0

    for start_node in adj:
        if start_node not in visited_nodes:
            #Starte eine neue Zyklussuche
            nodes_to_visit = [start_node] #Stack
            while nodes_to_visit:
                current_node = nodes_to_visit.pop()
                if current_node not in visited_nodes:
                    visited_nodes.add(current_node)
                    for neighbor in adj[current_node]:
                        nodes_to_visit.append(neighbor)
            cycle_count += 1

    return b - cycle_count

if __name__ == "__main__":
  P1 = [[+4, +8, +1, -2, -3, +5, +6, -7]]
  
  Q1 = [[+1, +2, +3, +4, +5, +6, +7, +8]]

  print(two_break_distance(P1, Q1))

  P2 = [[+1, -3, -2, +4, +5, +6]]

  Q2 = [[+1, +2, +3, +4, +5, +6]]

  print(two_break_distance(P2, Q2))

  P3 = [[+1, -3, -2, -4, +5, +6, -7, -8, +9, +10, -12, -11, +13, -15, -14, +16, +17, -20, -19, -18]]

  Q3 = [[+1, +2, +3, +4, +5, +6, +7, +8, +9, +10, +11, +12, +13, +14, +15, +16, +17, +18, +19, +20]]

  print(two_break_distance(P3, Q3))

  P4 = [[+1, -3, -2, +4], [+5, -7, -6, +8]]
  Q4 = [sorted(abs(b) for b in chrom) for chrom in P4] #Sort Each Chromosome

  print(two_break_distance(P4, Q4))
