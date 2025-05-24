import matplotlib.pyplot as plt

def read_fasta(file_path):
    #Read a FASTA file and return the concatenated sequence as a string."
    sequence = []
    with open(file_path, "r") as f:
        for line in f:
            if line.startswith(">"):
                continue  # Header beginnen mit einem ">", diese werden nicht einglesen
            sequence.append(line.strip().upper())
    return "".join(sequence)

#line.strip(): Entfernt führende und abschließende Leerzeichen sowie Zeilenumbrüche aus der aktuellen Zeile.
#upper(): Wandelt alle Buchstaben der bereinigten Zeile in Großbuchstaben um.
#sequence.append(...): Fügt den so bereinigten und in Großbuchstaben umgewandelten String der Liste sequence hinzu.

def count_nucleotides(seq):
    #Count occurrences of A, C, G, T in the sequence.
    counts = {"A":0, "C":0, "G":0, "T":0}
    for nucleotide in seq:
        if nucleotide in counts:
            counts[nucleotide] += 1
    return counts

#erstellt ein Dictionary für alle Basen der DNA und durchläuft die Genomsequenz
#jedes mal wenn die Schleife auf eine bestimmte Base trifft, wird deren Wert im Dictionary um 1 erhöht und somit gezählt

def plot_bar_chart(counts, title="Nucleotide Counts"):

#Plot a bar chart of nucleotide counts

    nucleotides = list(counts.keys())  #Erstellt eine Liste aller Nukleotide: A,T,G,C -> X-Achse

    #print(nucleotides)

    values = [counts[nuc] for nuc in nucleotides] #Erstellt eine Liste der Häufigkeiten der Nukleotide -> Y-Achse

    plt.figure(figsize=(6,4))
    plt.bar(nucleotides, values) # x und y achse definieren
    plt.xlabel("Nucleotide")
    plt.ylabel("Count")
    plt.title(title)
    plt.show()

def compute_skew(seq, positive_base, negative_base):
    skew = [0]                            #erstellt eine leere Liste
    for nucleotide in seq:                #das genom wird iteriert
        if nucleotide == positive_base:   #wenn das Nukleotid den Skew positiv beeinflusst, wird er erhöht, wenn negativ dann verringert

            skew.append(skew[-1] + 1)     #„Nimm das letzte Element in der Liste“, addiere 1 und füge das Ergbnis der Liste ganz vorne hinzu.
        elif nucleotide == negative_base:
            skew.append(skew[-1] - 1)    #„Nimm das letzte Element in der Liste“, subbtrahiere 1 und füge das Ergbnis der Liste ganz vorne hinzu.
        else:
            skew.append(skew[-1])   #„Nimm das letzte Element in der Liste“ und füge es vorne an die Liste hinzu
    return skew

def plot_skews(seq, genome_label="Genome"):
    #Plottet GC-skew und GT-skew für ein Genom

    gc_skew = compute_skew(seq, 'G', 'C')  #G als positive Base, C als negative -> Y-Achse
    gt_skew = compute_skew(seq, 'G', 'T')  # G als positive Base, T als negative -> y-Achse

    positions = range(len(gc_skew)) #Erstellt eine Liste mit allen Positionen des Genoms -> X-Achse

    plt.figure(figsize=(10, 5))

    plt.plot(positions, gc_skew, label="GC-skew", color="blue")
    plt.plot(positions, gt_skew, label="GT-skew", color="green", linestyle="--")

    plt.xlabel("Genome Position")
    plt.ylabel("Skews")
    plt.title(f"Skew Plots for {genome_label}")
    plt.legend()
    plt.show()

    # Identifiziert das Minimum des Skews für einen Wahscheinlichen Origin of replication

    min_index = gc_skew.index(min(gc_skew)) #Enthält die Position, an der der größte GC-Skew-Wert in der Liste zu finden ist.
    print(f"For {genome_label}:")
    print(f"Minimum GC-skew at position: {min_index}")
    print(f"GC-skew value at minimum: {min(gc_skew)}")

    return min_index

def process_genome(file_path, genome_label="Genome"):
    seq = read_fasta(file_path)
    counts = count_nucleotides(seq)
    print("Nucleotide Counts:", counts)

    plot_bar_chart(counts, title=f"{genome_label} Nucleotide Counts")
    origin = plot_skews(seq, genome_label)
    return counts, origin


process_genome("halomonas.fna", "Halomonas Genome")
process_genome("staphylo.fna", "Stahpylococcus Genome")
process_genome("strepto.fna", "Streptococcus Genome")
