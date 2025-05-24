def overlap_graph_assembly(kmers):
    """Assignment 1b.

    arguments:
        kmers (list): a sorted list of k-mers.

    returns:
        [str, ...]: a list/set/generator of all genomes that can be reconstructed from input k-mers.
    """
    n = len(kmers)
    np.set_printoptions(threshold=np.inf)
    ad_matrix = np.zeros((n, n), dtype=int)

    for i in range(len(kmers)):
      suffix = kmers[i][1:]
      #prefix = kmers[i][:-1]

      for j in range(len(kmers)):
        if i != j and suffix == kmers[j][:-1]:
          ad_matrix[i,j] = 1

    #print(ad_matrix)

    results = []
    paths = [[i] for i in range(n)]  #Erstelle alle möglichen Startpunkte für Pfade.
                                     #Jedes Element ist ein Pfad, besteht am Anfang jeodch nur aus einem Startpunkt
                                     #[[0], [1], [2], ...]


    while paths: #Wenn paths leer ist, wird die Schleife beendet

        new_paths = [] #Liste für die neuen Pfade, die in dieser Runde entstehen. Der Rest wird verworfen

        for path in paths:

          #Anfangsprüfung: Wenn der Pfad alle kmers verwendet hat dann ist er vollständig
            if len(path) == n:
                # Vollständiger Pfad → Genome zusammenbauen
                genome = kmers[path[0]] #Starte den rekonstruierten String mit dem ersten kmer im Pfad

                #Für jedes weitere k-mer im Pfad
                for idx in path[1:]:
                    genome += kmers[idx][-1] #Hänge nur den letzten Buchstaben an -> Anfang schon durch vorheriges kmer abgedeckt
                results.append(genome)
                continue #Springe zum nächsten Pfad, da dieser hier schon abgeschlossen ist

          #Neuen Punkt im akutellen Pfad Finden
            last = path[-1] #Hole den Endpunkt des akutellen unvollständigen Pfades (Index des letzten kmers)

            for candidate_point in range(n): #Überprüfe alle möglichen nächsten kmers, ob es der Nächste Punkt im Pfad werden könnte
                if ad_matrix[last, candidate_point] == 1 and candidate_point not in path: #Wenn last eine Kante mit einem kmer hat und diese im akutellen Pfad noch nicht vorgekommen ist
                    new_paths.append(path + [candidate_point]) #Pfad verlängern um candidate_point
                                                               #Pfad kommt in die nächste Runde -> new_paths
        #print(new_paths)
        paths = new_paths #ersetzt alle bisherigen Pfade nur durch jene die erfolgreich verlängert werden konntne -> nächste Runde kann bgeinnen

    return results
