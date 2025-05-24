def randomized_motifsearch(dna, k, iterations):
    """Task 2e: Implement RandomizedMotifSearch

    There are no tests for this function, you can use the main function below
    to find motifs for the homework. Execute the file directly using
    ~$ python ./ch02_assignments.py

    """
    best_overall_motifs = None
    best_overall_score = float('inf')

    #iterations = 5
    #ehrfach ausführen, um bessere Ergebnisse zu bekommen
    for _ in range(iterations):
        #Zufällige Initialisierung
        motifs = []
        t = len(dna)  #Anzahl Sequenzen
        for seq in dna:
            start = random.randint(0, len(seq) - k)
            kmer = seq[start:start+k]
            motifs.append(kmer)

        #Kopie als "Bestes" im aktuellen Durchlauf
        best_motifs = motifs[:]

        while True:
            #Erzeuge Profil aus den aktuellen Motifs (mit Pseudocounts)
            profile = motif_profile(best_motifs, pcount=True)

            #Bestimme neue Motifs anhand des Profils
            new_motifs = get_motifs_from_profile(profile, dna)

            #Score vergleichen
            if motif_score(new_motifs) < motif_score(best_motifs):
                best_motifs = new_motifs
            else:
                #Keine Verbesserung -> Abbruch
                break

        #Prüfen, ob das Ergebnis dieses Durchlaufs global besser ist
        current_score = motif_score(best_motifs)
        if current_score < best_overall_score:
            best_overall_score = current_score
            best_overall_motifs = best_motifs

    return best_overall_motifs
