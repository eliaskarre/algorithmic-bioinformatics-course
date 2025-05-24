import math
import numpy
import random
import itertools # To execise your mind, try not to use itertools.

#TASK 1a ------------------------------------------------------------------------------------------------------------------------------------------------------------
def hamming_distance(a, b):
  assert len(a) == len(b) #a und b müssen gleich lang sein!!
  dist = 0
  for x, y in zip(a, b): #zip nimmt mehrere Iterable und zippt sie zusammen -> Verschachtelte Schleife
                         #Sie bilden Paare von Elementen die an denselben Positionen in den einzelnen Iterables stehen
      if x != y: #wenn sich zwei Elemente unterscheiden, wird die Distanz erhöht
          dist += 1
  return dist

def kd_neighbors_exp_k(kmer, d):

    alphabet = ['A', 'C', 'G', 'T']
    k = len(kmer)
    neighbors = []

    #itertools.product erzeugt alle möglichen Kombinationen des Alphabets (4^k kmere) -> das Ergebnis wird als Tupel zurückgegeben.
    """
    Alternative unflexible Methode zu itertools.product:
    candidates=[]
    for pos1 in alphabet:
      for pos2 in alphabet:
        for pos3 in alphabet:
          for pos4 in alphabet:
            candidates.append(pos1+pos2+pos3+pos4)
    """

    for candidate_tuple in itertools.product(alphabet, repeat=k):
        candidate = ''.join(candidate_tuple)  #Tupel in String umwandeln
        # Überprüfe die Hamming-Distanz (Laufzeit O(k))
        if hamming_distance(kmer, candidate) <= d:
            neighbors.append(candidate) #Wenn in der Distanz, dann zu Neighbors hinzufügen
    return neighbors

  def motif_enumeration(dna, k, d):
    """Task 1c: Return all motifs (or kmer) found with brute force.

    Arguments:
        dna (list): A list of DNA sequences.
        k (int): The k-mer length.
        d (int): The maximum k-mer distance.

    Returns:
        [str, ...]: A list of k-mers.
    """
    result = set()

    seq_neighbors = dict()

    for sequence in dna:
        seq_neighbors[sequence] = []
        for i in range(len(sequence) - k + 1):
          kmer = sequence[i:i+k]
          kmer_neighbors = kd_neighbors_exp_k(kmer, d)
          seq_neighbors[sequence].extend(kmer_neighbors)

    #return seq_neighbors

    common = set.intersection(*(set(liste) for liste in seq_neighbors.values()))
    return set(common)

  if __name__ == '__main__':
    
    implanted_15mers = [
    "ATGACCGGGATACTGATAGAAGAAAGGTTGGGGGCGTACACATTAGATAAACGTATGAAGTACGTTAGACTCGGCGCCGCCG",
    "ACCCCTATTTTTTGAGCAGATTTAGTGACCTGGAAAAAAAATTTGAGTACAAAACTTTTCCGAATACAATAAAACGGCGGGA",
    "TGAGTATCCCTGGGATGACTTAAAATAATGGAGTGGTGCTCTCCCGATTTTTGAATATGTAGGATCATTCGCCAGGGTCCGA",
    "GCTGAGAATTGGATGCAAAAAAAGGGATTGTCCACGCAATCGCGAACCAACGCGGACCCAAAGGCAAGACCGATAAAGGAGA",
    "TCCCTTTTGCGGTAATGTGCCGGGAGGCTGGTTACGTAGGGAAGCCCTAACGGACTTAATATAATAAAGGAAGGGCTTATAG",
    "GTCAATCATGTTCTTGTGAATGGATTTAACAATAAGGGCTGGGACCGCTTGGCGCACCCAAATTCAGTGTGGGCGAGCGCAA",
    "CGGTTTTGGCCCTTGTTAGAGGCCCCCGTATAAACAAGGAGGGCCAATTATGAGAGAGCTAATCTATCGCGTGCGTGTTCAT",
    "AACTTGAGTTAAAAAATAGGGAGCCCTGGGGCACATACAAGAGGAGTCTTCCTTATCAGTTAATGCTGTATGACACTATGTA",
    "TTGGCCCATTGGCTAAAAGCCCAACTTGACAAATGGAAGATAGAATCCTTGCATACTAAAAAGGAGCGGACCGAAAGGGAAG",
    "CTGGTGAGCAACGACAGATTCTTACGTGCATTAGCTCGCTTCCGGGGATCTAATAGCACGAAGCTTACTAAAAAGGAGCGGA"]

    print(motif_enumeration(implanted_15mers, 15, 1))
