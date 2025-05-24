def genome_to_kmers(genome, k):
    """Assignment 1a.

    Arguments:
        genome (str): A nucleotide sequence.
        k (int): The k-mer length.

    Returns:
        [str, ...]: A sorted list of k-mers.
    """
    results = []
    for i in range(len(genome)-k+1):
        results.append(genome[i:i+k])

    return sorted(results)
