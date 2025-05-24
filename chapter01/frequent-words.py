import numpy as np
import time
import matplotlib.pyplot as plt

def frequentwords(seq, k):

  frequency_array = np.zeros(4**k) #Array initialisierung: Alle möglichen Kombinationen von 4 Basen bei k Positionen

  #Algorithmus geht jede Genomposition durch und erstellt ein kmer, indem es k Positionen upstream liest
  for index in range(len(seq) - k + 1): #minus k + 1 verhindert short reads am Ende des Genoms
                                        #Eintrag kann nur erfolgen wenn sich sich das kmer noch ausgeht
                                        # minus 1, weil Array bei 0 anfängt
      kmer = seq[index:index+k]
      if 'N' in kmer: # Checking if kmer contains 'N', skip if found.
          continue
      kmer_number = kmer_to_int(kmer) #kmer wird in Zahl bzw. Index umgewandelt
      frequency_array[kmer_number] += 1 #Der Count für die Nummer des kmers wird im Array erhöht

  sorted_indices = np.argsort(frequency_array) # gibt die Indizes in der Reihenfolge zurück, in der die Werte des Arrays von klein nach groß angeordnet sind.

  #Kehre die Reihenfolge um (absteigend) mit -1 und nehme die ersten 5
  top10_indices = sorted_indices[::-1][:5]

  result = dict()

  for index in top10_indices:
   kmer_str = int_to_kmer(index, k)           #Schlüssel: wandelt Index in Sequenz-String um
   result[kmer_str] = frequency_array[index]  #Wert: kmer count

  return result

def genome_percent(file_path, k):
  seq = read_fasta(file_path)

  #Runtime Achsen
  fractions = [] #X-Achse
  runtimes = [] #Y-Achse

  for i in range(10, 101, 10): #Iteriert von 10 bis 100 in 10er Schritten
    to = int(len(seq)*(i/100)) #legt die obere Grenze der Fraktion im Gesamten genom fest (e.g 10% -> Zahl der Genompositionen * 0.1)

    seq_percent = seq[0:to]
    print(i,"% of the genome:")

    start_time = time.time() #Starte Zeitmessung

    print(frequentwords(seq_percent, k)) #Zählt kmere

    end_time = time.time() #Beende Zeitmessung

    #Zeit in Listen Speichern
    elapsed = end_time - start_time #berechent die runtime, durch die Zeitdifferenz
    fractions.append(i)
    runtimes.append(elapsed)

  #Plot um die Runtime über die Genomfraktionen darzustellen

  plt.figure(figsize=(7,4))
  plt.plot(fractions, runtimes, marker='o', linestyle='--')
  plt.xlabel("Genome fraction (%)")
  plt.ylabel("Runtime (seconds)")
  plt.title(f"Runtime vs. fraction of genome (k={k})")
  plt.grid(True)
  plt.show()

print("Counts for Halomonas")
halo_seq = read_fasta("halomonas.fna")
print(frequentwords(halo_seq, 9))

print("Counts for Staphylococcus")
staphylo_seq = read_fasta("staphylo.fna")
print(frequentwords(staphylo_seq, 9))

print("Counts for Streptococcus")
strepto_seq = read_fasta("strepto.fna")
print(frequentwords(strepto_seq, 9))

print("Percental Counts for Halomonas")
genome_percent("halomonas.fna", 8)
