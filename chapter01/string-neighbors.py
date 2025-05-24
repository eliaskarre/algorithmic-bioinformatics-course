alphabet = ['A', 'C', 'G', 'T']

a = "ACGTTA"
b = "GAGTCA"

def neighbors_d1(pattern):
  #Sucht alle Nachbarn eines Strings, mit einem Abstand von 1
  result = set() #initialisiert Ergebnis Set

  #für alle Positionen eines Strings wird geschaut, ob es Buchstaben im Alphabet gibt
  #Diese nicht mit der jeweligen String-Position matchen.
  #Sobald dies erkannt wurde, wird der Buchstabe ausgetauscht und somit ein neuer d=1 Nachbar erstellt
  for i in range(len(pattern)):
    for nucleotide in alphabet: #Vergleicht String-Position mit kompletten Alphabet
      if nucleotide != pattern[i]: #Wenn Abweichung gefunden
        neighbor = pattern[:i] + nucleotide + pattern[i+1:] #Füge Abweichenden Buchstaben ein um Neihbor zu erzeugen
        result.add(neighbor) #Füge neuen neighbor den Ergebnissen hinzu
  return result

def neighbors(pattern, d):
    #Für d == 0 wird einfach das Pattern zurückgegeben.
    #Für d == 1 wird die Funktion neighbors_d1 verwendet.
    #Für d >= 2 wird das Ergebnis als Vereinigung der 1‑Nachbarn von allen Nachbarn mit Hamming-Distanz d-1 berechnet.

    if d == 0:
        return {pattern}
    if d == 1:
        return neighbors_d1(pattern)

    result = set()

    first_neighbors = neighbors_d1(pattern) # Hole zunächst alle 1‑Nachbarn

    for p in first_neighbors: #Führe neighbors_d1 nochmal aus und Vereinige die Mengen
        result = result.union(neighbors(p, d - 1)) #d minus 1, da first_neugbors bereits d1 Nachbarn erstellt
    return result

#print(hamming_distance(a,b))

#print(neighbors_d1(q1))

q1 = "ACGTTA"

print("Sorted 1 neighbors of q1: ", sorted(neighbors(q1,1)))
print("Sorted 2 neighbors of q1: ", sorted(neighbors(q2,1)))

print("3 neighbor count of q1:", len(neighbors(q1,3)))
print("4 neighbor count of q1:", len(neighbors(q1,4)))

q2 = "AAAAAAAGGGGGG"

print("3 neighbor count of q2:", len(neighbors(q2,3)))
print("4 neighbor count of q2:", len(neighbors(q2,4)))
