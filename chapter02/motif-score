def motif_score(motifs, pcount=False):

    #Falls keine Motifs übergeben wurden
    if not motifs:
        return 0

    #Konvertiere alles in Großbuchstaben
    motifs = [m.upper() for m in motifs]

    t = len(motifs)        #Anzahl der Motifs
    n = len(motifs[0])     #Länge
    score = 0

    for j in range(n): #gehe durch jede Spalte

        if pcount:
            #Pseudocounts
            counts = {'A': 1, 'C': 1, 'G': 1, 'T': 1}
        else:
            counts = {'A': 0, 'C': 0, 'G': 0, 'T': 0}

        for motif in motifs: #gehe die einzelnen Motifs durch
            base = motif[j] #selektiere die Base eines Motifs in der Spalte j

            if base in counts: # Nur A, C, G, T zählen
                counts[base] += 1

        #Finde die Häufigste Base in Spalte j
        max_count = max(counts.values())
        #Beitrag zum Score
        score += (t - max_count)

    return score
