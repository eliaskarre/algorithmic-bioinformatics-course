import sys

def last_to_first(bwt):

    first_col = sorted(bwt)

    occ_last = []
    count_last = {}

    for ch in bwt:
        count_last[ch] = count_last.get(ch, 0) + 1
        occ_last.append(count_last[ch])

    occ_first = []
    count_first = {}
    for ch in first_col:
        count_first[ch] = count_first.get(ch, 0) + 1
        occ_first.append(count_first[ch])

    #Build a mapping
    first_index = {}
    for idx, ch in enumerate(first_col):
        first_index[(ch, occ_first[idx])] = idx

    #print("Hash-Table ", first_index)

    lf = [first_index[(bwt[i], occ_last[i])] for i in range(len(bwt))]
       
    return lf


def inverse_bwt(bwt):
    lf = last_to_first(bwt)
    row = bwt.index('$')
    original = []
    for _ in range(len(bwt) - 1):
        row = lf[row]
        original.append(bwt[row])

    return ''.join(reversed(original)) + '$'


def main():
    if len(sys.argv) < 2:
        print("Usage: python bwt_decoder.py <bwt_string>")
        sys.exit(1)

    bwt = sys.argv[1]
    
    print("BWT:\t", bwt)

    lf = last_to_first(bwt)
    print("LAST-to-FIRST mapping:")
    print(lf)

    original = inverse_bwt(bwt)
    print("Reconstructed text:\t", original)

if __name__ == '__main__':
    main()
