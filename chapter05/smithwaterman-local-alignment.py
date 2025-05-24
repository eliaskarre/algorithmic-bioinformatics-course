import numpy as np
import pandas as pd
np.set_printoptions(threshold=np.inf)
np.set_printoptions(linewidth=1000)

scoring_matrix = {
    'A': {'A': 4, 'C': -2, 'G': -1, 'T': -2, '-': -4},
    'C': {'A': -2, 'C': 4, 'G': -2, 'T': -1, '-': -4},
    'G': {'A': -1, 'C': -2, 'G': 4, 'T': -2, '-': -4},
    'T': {'A': -2, 'C': -1, 'G': -2, 'T': 4, '-': -4},
    '-': {'A': -4, 'C': -4, 'G': -4, 'T': -4, '-': -4}
}

def local_alignment(seqx, seqy, scoring_matrix):
    m = len(seqx)
    n = len(seqy)

    matrix = np.zeros((m+1, n+1), dtype=int)

    # Matrix füllen
    for x in range(1, m+1):
        for y in range(1, n+1):
            left_score = matrix[x][y-1] + scoring_matrix['-'][seqy[y-1]]    # Gap in seqx
            upper_score = matrix[x-1][y] + scoring_matrix[seqx[x-1]]['-']    # Gap in seqy
            diagonal_score = matrix[x-1][y-1] + scoring_matrix[seqx[x-1]][seqy[y-1]]

            score = max(diagonal_score, left_score, upper_score)
            if score < 0:
                score = 0
            matrix[x][y] = score

    # Maximale Score finden
    max_score = np.max(matrix)
    positions = np.argwhere(matrix == max_score)

    all_alignments = []

    # Für jede Startposition ein vollständiges Stack-basiertes Traceback
    for x, y in positions:

        stack = [(x, y, [], [])]  # (x, y, aligned_seqx, aligned_seqy)

        while stack: #TO-DO Liste = Stack
            #print(stack)
            x, y, aligned_seqx, aligned_seqy = stack.pop() #streiche momentane position von der TO-DO Liste = Stack

            # Alignment abgeschlossen -> wenn 0 dann Alignment fertig
            if matrix[x][y] == 0:
                #Baue Alignment auf -> Reihenfolge umdrehen
                aligned_seqx = ''.join(aligned_seqx[::-1])
                aligned_seqy = ''.join(aligned_seqy[::-1])

                #Speichere Alignment
                all_alignments.append((aligned_seqx, aligned_seqy, len(aligned_seqx), int(max_score))) #Speichere Alignment, Länge und Score
                continue #Gehe nun weiter die TO-DO Liste ab

            current_box = matrix[x][y]

            #Für jede zulässige Richtung ein neuer Eintrag auf der TO-DO Liste:

            # Diagonalbewegung

            if current_box == matrix[x-1][y-1] + scoring_matrix[seqx[x-1]][seqy[y-1]]:
                    stack.append((x-1, y-1, aligned_seqx + [seqx[x-1]], aligned_seqy + [seqy[y-1]]))

            # Bewegung nach oben

            if current_box == matrix[x-1][y] + scoring_matrix[seqx[x-1]]['-']:
                    stack.append((x-1, y, aligned_seqx + [seqx[x-1]], aligned_seqy + ['-']))

            # Bewegung nach links

            if current_box == matrix[x][y-1] + scoring_matrix['-'][seqy[y-1]]:
                    stack.append((x, y-1, aligned_seqx + ['-'], aligned_seqy + [seqy[y-1]]))
    print(matrix)
    df = pd.DataFrame(matrix)
    csv_path = 'matrix.csv'
    df.to_csv(csv_path, index=False, header=False)
    return all_alignments

print(local_alignment('TAGCAAGAGTTGACGGTGTGGAGCCCTTTATGT', 'GGGCTTTATGCGCAAAGAGTCGAGGGATCCGCATG', scoring_matrix))
