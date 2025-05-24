# Mapping der Basen zu Ziffern und umgekehrt
base_to_num = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
num_to_base = {0: 'A', 1: 'C', 2: 'G', 3: 'T'}

def kmer_to_int(kmer):
    if kmer == "":
        return 0
    last = kmer[-1]   # Nimm das letzte Zeichen
    rest = kmer[:-1]   # Nimm den Rest (alles vor dem letzten Zeichen -> Präfix)
    return 4 * kmer_to_int(rest) + base_to_num[last] #Formel aus den Folien


def int_to_kmer(num, k):
    #Wandelt eine ganze Zahl num zurück in einen k-mer der Länge k.
    #Dabei wird num als Zahl im Basis-4-System interpretiert.

    if k == 0:
        return ""  # kein k-mer mehr zu erzeugen -> alle Stellen abgearbeitet

    # Letzte Ziffer in Basis 4 ist num % 4
    #Teilt man z.b 57 durch 4, ergibt das einen Rest von 1
    #-> 1 ist also die letzte Ziffer der Zahl 57, wenn man sie in Basis 4 schreibt.
    last_digit = num % 4

    # Die letzte Base des kmers bestimmt sich aus last_digit
    last_symbol = num_to_base[last_digit]

    #Berechnet den 'Prefix', also die Zahl ohne der Last Digit in der 4er Basis, mit der es dann weitergeht.
    rest_num = num // 4  #Macht eine Ganzzahlige Division -> Ergebnis wird abgerundet. E.g. 15÷4 = 3.75 -> ergibt 3


    # Rekursiver Aufruf: Bei jedem Aufruf wird eine Stelle bearbeitet, also wird k jedes mal um 1 verringert.
    #Sobald k 0 ist, sind alle stellen abgearbeitet.
    prefix = int_to_kmer(rest_num, k - 1)


    return prefix + last_symbol

print("12-mer Represented by 1234561:")
print(int_to_kmer(1234561, 12))

print("13-mer Represented by 1234561:")
print(int_to_kmer(1234561, 13))

print("Integer for AAACTGCTTTAA:")
print(kmer_to_int("AAACTGCTTTAA"))

print("2-mer Represented by 16")
print(int_to_kmer(16, 2))
