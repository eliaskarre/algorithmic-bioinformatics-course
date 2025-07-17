import numpy as np
from collections import Counter, defaultdict
from itertools import product

mass_to_aa = {57: "G", 71: "A", 87: "S", 97: "P", 
              99: "V", 101: "T", 103: "C", 113: "LI", 
              114: "N", 115: "D", 128: "QK", 129: "E", 
              131: "M", 137: "H", 147: "F", 156: "R", 
              163: "Y", 186: "W"}

aa_to_mass = {"G": 57, "A": 71, "S": 87, "P": 97, 
              "V": 99, "T": 101, "C": 103, "L": 113, 
              "I": 113, "N": 114, "D": 115, "Q": 128, 
              "K": 128, "E": 129, "M": 131, "H": 137,
              "F": 147, "R": 156, "Y": 163, "W": 186}

aa_list = ["G", "A", "S", "P", "V", "T", 
           "C", "L", "N", "D", "Q", "E",
           "M", "H", "F", "R", "Y", "W"]

def ideal_spectrum(peptide):
    """
        Args: 
            peptide: string
        Returns:
            list: [0, 71, 156, 174, 285, 289, 400, 418, 503, 574]

    """
    prefix = [0]
    for aa in peptide:
        prefix.append(prefix[-1] + aa_to_mass[aa])
    total = prefix[-1]
    
    suffix = [total - m for m in prefix[1:-1]]
    
    spectrum = sorted(prefix + suffix)
    return spectrum
 
def decode_spectrum(ispec):
    """
        Args:
            ispec: list
        Returns:
            list: proteins explaining spectrum
    """
    S = sorted(ispec)
    if not S or S[0] != 0:
        S = [0] + S
    source, sink = S[0], S[-1]
    G = defaultdict(list)
    S_set = set(S)
    for i in S:
        for m, aas in mass_to_aa.items():
            j = i + m
            if j in S_set:
                for aa in aas:
                    G[i].append((j, aa))

    count_paths = {node: 0 for node in S}
    count_paths[source] = 1
    for u in S:
        for v, _ in G[u]:
            count_paths[v] += count_paths[u]
    total_paths = count_paths[sink]
    print(f"Total number of paths through the DAG: {total_paths}")

    peptides = []
    path = []
    def dfs(u):
        if u == sink:
            pep = "".join(path)
            if ideal_spectrum(pep) == S:
                peptides.append(pep)
            return
        for v, aa in G[u]:
            path.append(aa)
            dfs(v)
            path.pop()

    dfs(source)
    return sorted(peptides)


def peptide_identification(specvec, proteome, aa_masses = None):
    """
    Args:
     specvec (list): the spectral vector
     protemoe (string): the proteome
     aa_masses (dict): all amino acids with their masses

     specvec = [0,0,0,4,-2,-3,-1,-7,6,5,3,2,1,9,3,-8,0,3,1,2,1,8]
     proteome = "XZZXZXXXZXZZXZXXZ"
     aa_masses = {"X": 4, "Z": 5}


    Returns:
        (string, int): The best peptide and it's score.

    """
    best_score = float('-inf')
    best_peptide = ''
    n = len(proteome)

    for i in range(n):
        pm = 0
        score = 0
        for j in range(i, n):
            aa = proteome[j]
            if aa not in aa_masses:
                break
            pm += aa_masses[aa]
            if pm < 1 or pm > len(specvec):
                break
            score += specvec[pm-1]
            if pm == len(specvec):
                if score > best_score:
                    best_score = score
                    best_peptide = proteome[i:j+1]
                break

    return best_peptide, best_score

def get_spectral_dict_size(specvec, threshold, mass_to_aa, max_score):
    """
        specvec = [4,-3,-2,3,3,-4,5,-3,-1,-1,3,4,1,3]
        threshold = 1
        masses_aa = {4:"X", 5: "Z"}
        max_score = 8


        Returns:
            int: size
    """
    m = len(specvec)
    dp = [[0]*(max_score+1) for _ in range(m+1)]
    dp[0][0] = 1

    # fill DP
    for i in range(1, m+1):
        si = specvec[i-1]
        for t in range(max_score+1):
            cnt = 0
            for mass, aas in mass_to_aa.items():
                j = i - mass
                u = t - si
                if j >= 0 and 0 <= u <= max_score:
                    cnt += len(aas) * dp[j][u]
            dp[i][t] = cnt

    return sum(dp[m][t] for t in range(threshold, max_score+1))


def get_spectral_dict_prob(specvec, threshold, mass_to_aa, max_score):
    m = len(specvec)
    A = sum(len(aas) for aas in mass_to_aa.values())

    dp = [[0.0]*(max_score+1) for _ in range(m+1)]
    dp[0][0] = 1.0

    for i in range(1, m+1):
        si = specvec[i-1]
        for t in range(max_score+1):
            total = 0.0
            for mass, aas in mass_to_aa.items():
                prev_i = i - mass
                prev_t = t - si
                if prev_i >= 0 and 0 <= prev_t <= max_score:
                    total += dp[prev_i][prev_t] * (len(aas)/A)
            dp[i][t] = total

    return sum(dp[m][t] for t in range(threshold, max_score+1))
