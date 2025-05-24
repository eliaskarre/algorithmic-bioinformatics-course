def profile_entropy(profile):
    """Task 2c: Calculate the entropy of a profile

    Arguments:
        profile (matrix): A matrix where entry ij is the probability of
            nucleotide i being at position j.

    Returns:
        float: The entropy
    """
    if not profile or not profile[0]:
        return 0.0

    k = len(profile[0])
    entropies = []

    for j in range(k):
        col_entropy = 0.0
        for i in range(len(profile)):
            p = profile[i][j]
            if p > 0:
                col_entropy -= p * math.log2(p)
        entropies.append(col_entropy)

    #SUMMIEREN alle Spaltenentropien zu einem Wert
    return sum(entropies)
