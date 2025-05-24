
#Assignment 1

#integer mass table
mass_table = {
    'G': 57, 'A': 71, 'S': 87, 'P': 97, 'V': 99,
    'T': 101, 'C': 103, 'I': 113, 'L': 113, 'N': 114,
    'D': 115, 'K': 128, 'Q': 128, 'E': 129, 'M': 131,
    'H': 137, 'F': 147, 'R': 156, 'Y': 163, 'W': 186
}

def cyclo_spectrum(peptide): #Input -> zyklisches Peptid

    fragments = [peptide, ""] #Speichere alle möglichen zyklischen Sub Fragemente -> Peptid selbst und leer sind auch dabei
                              #Ich muss hier das Peptid selbst auch hinzufügen, da es mit den Fenstern nicht hinzugefügt werden kann, da sonst ungültige Fenster mit der Länge des Peptids ebenfalls hinzugefügt werden würden
    peptide_space = peptide + peptide  #Betrachte Peptid als doppelt so lang, um zyklische Sequenzen zu erfassen

    for i in range(len(peptide)): #Für jede AA im Peptid an der Stelle i
        for k in range(1, len(peptide)): #Erzeuge ein Fenster k zwischen 1 und len(peptid) -> Fenster kann len(peptid) - 1 groß sein
            #Füge Fenster k von Peptid als Fragment hinzu
            fragments.append(peptide_space[i:i+k])

    spectrum = []
    mass_spectrum = {}

    for frag in fragments:
      mass = 0
      for aa in frag:
        mass += mass_table[aa]
      spectrum.append(mass)
      mass_spectrum[frag] = mass

    #print(sorted(fragments))
    #print(sorted(spectrum))

    return sorted(spectrum), sorted(fragments), sorted(mass_spectrum.items(), key=lambda item: item[1])

def linear_spectrum(peptide): #Input -> lineares Peptid

    fragments = [""] #Leeres Peptid auch dabei

    for i in range(len(peptide)): #Für jede AA im Peptid an der Stelle i
        for k in range(1, len(peptide)-i+1): #Erzeuge ein Fenster k von k= 1 bis k= len(peptid)
                                             #Jedoch gehe nicht weiter als mögliche Fragmentlänge
                                             # -i ->je weiter Schleife im Peptid, desto kürzer werden mögliche Fragmente
                                             # bei NQEL wäre der Slice peptide[3:5] fehlerhaft, da die 5 zu weit geht! (geht nur bis 4)
            fragments.append(peptide[i:i+k]) #Füge Fenster k von Peptid als Fragment hinzu

    #print(fragments)

    spectrum = []
    mass_spectrum = {}

    for frag in fragments:
      mass = 0
      for aa in frag:
        mass += mass_table[aa]
      spectrum.append(mass)
      mass_spectrum[frag] = mass

    #print(sorted(fragments))
    #print(sorted(spectrum))
    #print(mass_spectrum)

    return sorted(spectrum), sorted(fragments), sorted(mass_spectrum.items(), key=lambda item: item[1])
peptide = "NQEL"
print(cyclo_spectrum(peptide))
print(linear_spectrum(peptide))

name_peptide = "ELIASKARRE"

cyclic_spec, cyclic_frags, cyclic_dict = cyclo_spectrum(name_peptide)
linear_spec, linear_frags, linear_dict = linear_spectrum(name_peptide)

print("Peptide: ", name_peptide)
print("Length: ", len(name_peptide))
print("---------------------------------------------------------")
print("Cyclospectrum: ", cyclic_spec)
print(" Length: ", len(cyclic_spec))
print("Cyclofragments: ", cyclic_frags)
print(" Length: ", len(cyclic_frags))
#print("Number of masses: ", len(cyclic_spec))
print("Fragements+Mass: ", cyclic_dict)
print("---------------------------------------------------------")
print("Linearspectrum: ", linear_spec)
print(" Length: ", len(linear_spec))
print("Linearfragments: ", linear_frags)
print(" Length: ", len(linear_frags))
#print("Number of masses: ", len(linear_spec))
print("Fragements+Mass: ", linear_dict)

"""#Assignment 2"""

def spectral_convolution(spectrum):

    convolutions = {}

    for x in spectrum:
      for y in spectrum:
        if x > y:
          convolution = x - y
          if convolution in convolutions:
            convolutions[convolution] += 1
          else:
            convolutions[convolution] = 1 #Hier beim nöchsten mal einen Counter verwenden

    sorted_convolutions = {k: v for k, v in sorted(convolutions.items(), key=lambda item: item[1], reverse=True)}

    mapped_convolutions = {}

    for convolution, count in sorted_convolutions.items():
            for aminoacid, mass in mass_table.items():
                if convolution == mass:
                    mapped_convolutions[aminoacid] = mapped_convolutions.get(aminoacid, 0) + count




    return sorted_convolutions, mapped_convolutions


theoretical_spectrum = [0, 71, 87, 114, 129, 156, 158, 216, 227, 243, 270, 287, 314, 330, 341, 399, 401, 428, 443, 470, 486, 557,]
experimental_spectrum = [0, 57, 71, 87, 129, 156, 158, 216, 227, 243, 270, 287, 314, 330, 341, 374, 399, 401, 428, 443, 470, 486, 557]

print(spectral_convolution(theoretical_spectrum)[0])
print(spectral_convolution(experimental_spectrum)[1])

#print(spectral_convolution(cyclo_spectrum("KARRE")[0])[1])

"""#Assignment 3"""

from collections import Counter

mass_table = {
    'G': 57, 'A': 71, 'S': 87, 'P': 97, 'V': 99,
    'T': 101, 'C': 103, 'I': 113, 'L': 113, 'N': 114,
    'D': 115, 'K': 128, 'Q': 128, 'E': 129, 'M': 131,
    'H': 137, 'F': 147, 'R': 156, 'Y': 163, 'W': 186
}

aminoacids = sorted(set(mass_table.values()))

def peptide_to_mass_list(peptide_str):
    #Wandelt einen Peptid strin in eine Liste von Massen um
    return [mass_table[aa] for aa in peptide_str]

def mass_list_to_peptide_string(peptide_list):
    #Wandelt eine Liste von Massen in einen Peptidstring um
    mass_to_amino = {
        57: 'G',
        71: 'A',
        87: 'S',
        97: 'P',
        99: 'V',
        101: 'T',
        103: 'C',
        113: 'I',  #Für I und L wähle immer L -> wir können nicht zwischen I und L unterscheiden
        114: 'N',
        115: 'D',
        128: 'K',  #Für K und Q wähle immer K
        129: 'E',
        131: 'M',
        137: 'H',
        147: 'F',
        156: 'R',
        163: 'Y',
        186: 'W'
    }
    return ''.join(mass_to_amino[m] for m in peptide_list)

def score(peptide, spectrum):
    #zyklisches Peptidspektrum
    peptide_spectrum = cyclo_spectrum(mass_list_to_peptide_string(peptide))[0]

    #Zähle Häufigkeiten beider Spektre.
    counter_theoretical = Counter(peptide_spectrum)
    counter_experimental = Counter(spectrum)

    #berechnet die Schnittmenge+
    intersection = counter_theoretical & counter_experimental

    #Summe aller Werte in der Schnittmenge entspricht dem Score
    return sum(intersection.values())

def peptide_mass(peptide):
    #Berrechnet die Summe aller Massen eines Peptids -> Gesamtmasse
    return sum(peptide)

def expand(leaderboard):
    expanded = []
    for peptide in leaderboard:
        for mass in aminoacids:
            expanded.append(peptide + [mass]) #Um ein einzelnes Element (hier den Wert von mass) an diese Liste anzuhängen, wird [mass] (eine Liste mit einem einzigen Element) verwendet
    return expanded

def trim_leaderboard(leaderboard, spectrum, N):

    #Kürzt das Leaderboard unbehält nur die Top N peptide anhand der Score
    if len(leaderboard) <= N:
        return leaderboard
    scored = [(peptide, score(peptide, spectrum)) for peptide in leaderboard]
    scored.sort(key=lambda x: x[1], reverse=True)
    cutoff = scored[N-1][1]
    trimmed = [peptide for peptide, s in scored if s >= cutoff]
    return trimmed

def leaderboard_cyclopeptide_sequencing(spectrum, N, use_convolution):

    parent_mass = max(spectrum)
    leaderboard = [[]]  #Starte mit leerem Peptid
    leader_peptide = []
    leader_score = 0

    if use_convolution:
      convolutions = spectral_convolution(spectrum)[0]
      for mass, count in convolutions.items():
        if count > 6 and mass in aminoacids:
          leaderboard.append([mass])
      #print(convolutions)
      #print(leaderboard)

    while leaderboard:
        #print(leaderboard)
        #Expande jedes Peptid im Leaderboard
        print("Size of leaderboard before expand: ", len(leaderboard))
        leaderboard = expand(leaderboard)
        print("Size of leaderboard after expand: ", len(leaderboard))

        #print(leaderboard)
        candidates = []

        for peptide in leaderboard:
            m = peptide_mass(peptide)
            if m == parent_mass:
                current_score = score(peptide, spectrum)
                if current_score > leader_score:
                    leader_peptide = peptide
                    leader_score = current_score
                candidates.append(peptide)
            elif m < parent_mass:
                candidates.append(peptide)
            #Verwerfe Peptide mit mass > parent_mass.
        leaderboard = candidates
        print("Size of leaderboard before trimming: ", len(leaderboard))
        leaderboard = trim_leaderboard(leaderboard, spectrum, N)
        print("Size of leaderboard after trimming: ", len(leaderboard))
    print("finished")
    return leader_peptide

#peptide_str = "ELIASKARRE"
#experimental_spectrum = cyclo_spectrum(peptide_str)[0]

nqel_book_spectrum = [0, 113, 114, 128, 129, 242, 242, 257, 370, 371, 484]
best_peptide = leaderboard_cyclopeptide_sequencing(nqel_book_spectrum, 10, True)
print("NQEL Spectrum Best Peptide: ", mass_list_to_peptide_string(best_peptide))


theoretical_spectrum = [0, 71, 87, 114, 129, 156, 158, 216, 227, 243, 270, 287, 314, 330, 341, 399, 401, 428, 443, 470, 486, 557,]
experimental_spectrum = [0, 57, 71, 87, 129, 156, 158, 216, 227, 243, 270, 287, 314, 330, 341, 374, 399, 401, 428, 443, 470, 486, 557]


print("------------------------------------------------")
print("Theoretical Spectrum:")
print("")
print("full aminoacid set:")
theoretical_best_peptide_full = leaderboard_cyclopeptide_sequencing(theoretical_spectrum, 10, False)
print("Best peptide: ", mass_list_to_peptide_string(theoretical_best_peptide_full))
print("Best peptide spectrum:", theoretical_best_peptide_full)
print("Score:", score(theoretical_best_peptide_full, theoretical_spectrum))
print("")
print("reduced aminoacid set:")
theoretical_best_peptide_reduced = leaderboard_cyclopeptide_sequencing(theoretical_spectrum, 10, True)
print("Best peptide: ", mass_list_to_peptide_string(theoretical_best_peptide_reduced))
print("Best peptide spectrum:", theoretical_best_peptide_reduced)
print("Score:", score(theoretical_best_peptide_reduced, theoretical_spectrum))
print("------------------------------------------------")
print("Experimental Spectrum:")
print("")
print("full aminoacid set:")
experimental_best_peptide_full = leaderboard_cyclopeptide_sequencing(experimental_spectrum, 10, False)
print("Best peptide: ", mass_list_to_peptide_string(experimental_best_peptide_full))
print("Best peptide spectrum:", experimental_best_peptide_full)
print("Score:", score(experimental_best_peptide_full, experimental_spectrum))
print("")
print("reduced aminoacid set:")
experimental_best_peptide_reduced = leaderboard_cyclopeptide_sequencing(experimental_spectrum, 10, True)
print("Best peptide: ", mass_list_to_peptide_string(experimental_best_peptide_reduced))
print("Best peptide spectrum:", experimental_best_peptide_reduced)
print("Score:", score(experimental_best_peptide_reduced, experimental_spectrum))
