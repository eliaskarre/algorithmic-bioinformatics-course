def motif_profile(motifs, pcount = True):
    """Task 2b: Make a motif profile.

    Note: it is recommended to use numpy for working with matrices.

    Arguments:
        motifs (list): A list of DNA sequences.
        pcount (bool, optional): Add pseudocounts if True.

    Returns:
        profile (matrix): A matrix where entry ij is the probability of
            nucleotide i being at position j.
    """
    if not motifs:
        return []

    k = len(motifs[0])
    n = len(motifs)

    profile = { 'A': [0]*k, 'C': [0]*k, 'G': [0]*k, 'T': [0]*k }

    #Für jede Spalte: Zähle die Basen, beginnend mit Pseudocount 1 für jede Base.
    for j in range(k):

        if pcount:
            #Pseudocounts
            counts = {'A': 1, 'C': 1, 'G': 1, 'T': 1}
        else:
            counts = {'A': 0, 'C': 0, 'G': 0, 'T': 0}

        for motif in motifs:
            base = motif[j].upper()  #immer Großbuchstaben
            if base in counts:
                counts[base] += 1
        #Gesamtsumme in der Spalte
        total = n + 4
        #Berechne relative Häufigkeiten
        for nucleotide in "ACGT":
            profile[nucleotide][j] = counts[nucleotide] / total

    return [profile['A'], profile['C'], profile['G'], profile['T']]
