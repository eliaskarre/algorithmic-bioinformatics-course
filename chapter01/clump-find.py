from collections import defaultdict

def clump_find(seq, k, window_length, t):
  # k the length of the k-mers.
  # L the length of the window along the genome.
  # t the number of least occurrences of the each k-mers in the windows.
  clumps = set()

  for i in range(len(seq) - window_length + 1):
    window = seq[i:i+window_length]
    print(i)
    #window_kmers = frequentwords(window, k)

    #Frequent Words umgeschrieben
    counts = defaultdict(int)  #dictionary statt Array
    for i in range(len(window) - k + 1):  #jedes Fenster wird komplett durchlaufen
        kmer = window[i:i+k]   #ein kmer ist genau k lang
        if 'N' in kmer:   #N am Ende ignorieren
            continue
        counts[kmer] += 1

    window_kmers = {kmer: count for kmer, count in counts.items() if count > t} #Threshold wird berücksichtigt beim Filtern

    for i in window_kmers:
      if window_kmers[i] >= t:
        clumps.add(i)

  return clumps

  #return #All distinct k-mers forming (L,t)-clumps in Genome

halo_seq = read_fasta("halomonas.fna")

#cut_index = int(len(halo_seq) * 0.8)  # ab 80 % der Länge
#halo_seq = halo_seq[cut_index:]  # letzter Abschnitt

print(clump_find(halo_seq, 9, 300, 6))

clumps ={'CCTGCTCCT', 'ACCACGACC', 'GAAGAAGGA', 'GCTGCTCTT', 'AAGGAAGAA', 'CTTACCTCT', 'GGCCTCGGC', 'GAGCCAGAG', 'CTCTGGCTC', 'AGTGCTTCA', 'GCCTCTTCC', 'TACCTCTTA', 'TCGGCCTCG', 'CAGAGCCAG', 'AGCCAGAGC', 'GCTCTGGCT', 'AGAAGGAAG', 'CCAGAGCCA', 'GACCACGAC', 'GCTTCAGTG', 'GGCTCTGGC', 'TTCAGTGCT', 'TGGTCGTGG', 'CTCGGCTTC', 'GTGGTCGTG', 'CCACGACCA', 'CTGCTCCTG', 'ACCTCTTAC', 'GCCAGAGCC', 'GTCGTGGTC', 'TCGTGGTCG', 'TTACCTCTT', 'TCAGTGCTT', 'AGAGCCAGA', 'GCTCCTGCT', 'CTGCTCTTC', 'TGCTTCAGT', 'CTGGCTCTG', 'TCTTACCTC', 'TGGCTCTGG', 'TCCTGCTCC', 'CCTCTTCCT', 'CAAATCAAA', 'AGGAAGAAG', 'AAGAAGGAA', 'CGCTGCTCT', 'CTCTTACCT', 'CCTCGGCTT', 'CTCCTGCTC', 'GTGCTTCAG', 'CGACCACGA', 'GGTCGTGGT', 'CTTCAGTGC', 'CGGCCTCGG', 'TCTGGCTCT', 'CACGACCAC', 'GAAGGAAGA', 'CCTCTTACC', 'GGAAGAAGG', 'CGTGGTCGT', 'ACGACCACG', 'GCCTCGGCT', 'TGCTCCTGC'}

def reverse_complement(kmer):
    #Berechnet das Reverse Complement eines k-mer.
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    # Erzeugt das komplementäre Zeichen für jedes Zeichen im umgekehrten kmer
    return "".join(complement[base] for base in reversed(kmer))


def clumps_with_rc(clumps):
    #Überprüft, ob eines der k-mer (Clumps) auch ein Reverse Complement hat, das ebenfalls als Clump gefunden wurde.
    #Gibt ein Dictionary zurück, in dem der Schlüssel das k-mer ist und der Wert angibt, ob das Reverse Complement ebenfalls ein Clump ist. (true, false)

    result = {}
    for kmer in clumps:
        rc = reverse_complement(kmer)
        result[kmer] = rc in clumps #erzegut true/false Wert mit dem kmer als Schlüssel
    return result

print("Gefundene Clumps:")
print(clumps)

rc_results = clumps_with_rc(clumps)
print("\nÜberprüfung, ob das Reverse Complement auch ein Clump bildet:")
for kmer, has_rc in rc_results.items():
    print(f"{kmer} (Reverse Complement: {reverse_complement(kmer)}) -> {has_rc}")
