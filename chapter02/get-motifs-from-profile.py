def get_motifs_from_profile(profile, dna):
    """Task 2d: Get best scoring motif in each line.

    Returns:
        motifs: A list of motifs.
    """
        #Länge der Motifs aus dem Profil -> Anzahl der Spalten
    k = len(profile[0])

    best_motifs = []
    best_probs = []

    # Mapping von Nukleotiden zu Zeilenindex im Profil
    nucleotide_index = {'A': 0, 'C': 1, 'G': 2, 'T': 3}

    for seq in dna:
        best_prob = -1.0
        best_motif = None
        # fr jedes mögliche kmer in der Sequenz:
        for i in range(len(seq) - k + 1):
            kmer = seq[i:i+k]
            prob = 1.0
            for j, nucleotide in enumerate(kmer.upper()):
                #falls das Nukleotid nicht in unserem Profil vorkommt, wird die Wahrscheinlichkeit 0
                if nucleotide not in nucleotide_index:
                    prob = 0
                    break
                # Multipliziere die Wahrscheinlichkeit der Base an Position j
                prob *= profile[nucleotide_index[nucleotide]][j]
           
            if prob > best_prob:
                best_prob = prob
                best_motif = kmer
        best_motifs.append(best_motif)
        best_probs.append(best_prob)

    #return best_motifs, best_probs
    return best_motifs
