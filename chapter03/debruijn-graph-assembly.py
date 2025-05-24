def get_deBruijn_graph(kmers):
    #https://www.youtube.com/watch?v=TNYZZKrjCSk
    """ Assignment 2a.

    Arguments:
        kmers (list): A sorted list of k-mers.

    Returns:
        nodes ({nodes}): a set of nodes
        edges ([(node_from, node_to), ...]): a list of edges connecting nodes

    """
    nodes = set()      # Hier speichern wir alle Knoten
    edges = []         # Hier speichern wir alle Kanten

    for kmer in kmers:

        prefix = kmer[:-1]
        suffix = kmer[1:]

        nodes.add(prefix)
        nodes.add(suffix)

        #Jede k-mer erzeugt eine Kante vom Prefix zum Suffix
        edges.append((prefix, suffix))

    return nodes, edges

def get_genome_deBruijn(kmers):
    """ Assignment 2b:

    arguments:
        kmers (list): a sorted list of k-mers.

    returns:
        str: a valid genomes that can be reconstructed from input k-mers.
    """
    nodes = set()      #Knoten
    edges = []         #Kanten
    #Gleich wie vorhin
    for kmer in kmers:

        prefix = kmer[:-1]
        suffix = kmer[1:]

        nodes.add(prefix)
        nodes.add(suffix)

        edges.append((prefix, suffix))


    #Erstelle Adjazenzliste
    #Für jeden Knoten wird eine Liste seiner Nachbarknoten erstellt
    graph = {}
    for u, v in edges:
        if u in graph:
            graph[u].append(v)
        else:
            graph[u] = [v]

    #print(graph)

    #Wahl des Startknoten anhand der Knotengrade

    indegree = {node: 0 for node in nodes}
    outdegree = {node: 0 for node in nodes}
    for u in graph: #Outdegree: Anzahl der Nachbarn eines Knotens
        outdegree[u] = len(graph[u])
        for v in graph[u]: #Indegree: Häufigkeit, wie oft dieser Knoten in den Nachbarslisten der anderen Knoten insgesamt vorkommt.
            indegree[v] += 1
    #print(indegree)
    #print(outdegree)

    start = None
    for node in nodes:
        #Für einen Eulerpfad sollte genau ein Knoten existieren, bei dem (out_degree - in_degree == 1).
        if outdegree.get(node, 0) - indegree.get(node, 0) == 1:
            start = node
            break
    if start is None:
        # Wenn kein spezieller Start gefunden wird, wähle irgendeinen Knoten, der ausgehende Kanten hat.
        for node in nodes:
            if node in graph and graph[node]:
                start = node
                break
    if start is None:
        return ""  # Falls gar keine Kanten existieren.

    #Finde einen Eulerpfad mittels einem Stack
    #Dabei werden die Kanten "verbraucht", sobald sie benutzt werden.
    path = []    # Hier wird der Eulerpfad gesammelt (in umgekehrter Reihenfolge)
    stack = [start]

    while stack:
        #print(stack)
        current_point = stack[-1]
        # Falls es von curr noch ausgehende Kanten gibt, gehe zur nächsten Station.
        if current_point in graph and graph[current_point]:
            # Nimm die erste Kante aus der Liste und "verbrauche" sie.
            next_node = graph[current_point].pop(0)
            stack.append(next_node)
        else:
            # Keine Kante mehr vom akutellen Punkt -> Eulerpfad erfolgreich erstellt.
            break

    #Genomstring aus Eulerpfad
    #Der erste Knoten liefert alle ersten Positionen des Genoms
    #Jeder weiterer Knoten trägt nur das jeweils letzte Zeichen zum Genom bei -> Overlap
    genome = stack[0]
    for node in stack[1:]: #nur das jeweils letzte Zeichen
        genome += node[-1]

    return genome
