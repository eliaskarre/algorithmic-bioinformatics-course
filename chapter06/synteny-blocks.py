def reverse_complement(kmer):
    comp = {'A':'T','T':'A','C':'G','G':'C'}
    return ''.join(comp[base] for base in kmer[::-1])

#print(reverse_complement("ATGC"))

def synteny_blocks(k, genome1, genome2):
  #blocks = set()
  pairs = set()

  for i in range(len(genome1)-k+1):
    for j in range(len(genome2)-k+1):
      kmer1 = genome1[i:i+k]
      kmer2 = genome2[j:j+k]

      if kmer1 == kmer2 or kmer1 == reverse_complement(kmer2):
        #blocks.add(kmer1)
        pairs.add((i+1,j+1))

        print(kmer1, kmer2, reverse_complement(kmer2), (i+1,j+1))
  return pairs

if __name__ == "__main__":
  #synteny_blocks(4, "GCATCGTAATGCATTT", "ATGCATATT")

  with open("Assignment_1.txt", "r") as f:
      lines = [line.strip() for line in f if line.strip()]

  seq1, seq2 = lines

  synteny_blocks(13, seq1, seq2)
