def reverse_complement(kmer):
    #Berechnet das Reverse Complement eines k-mer.
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    # Erzeugt das komplementäre Zeichen für jedes Zeichen im umgekehrten kmer
    return "".join(complement[base] for base in reversed(kmer))
