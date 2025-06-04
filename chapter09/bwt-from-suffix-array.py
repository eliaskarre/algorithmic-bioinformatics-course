def build_suffix_array(text, sentinel='$'):

    if sentinel not in text:
        text = text + sentinel

    suffixes = [(text[i:], i) for i in range(len(text))]

    suffixes.sort(key=lambda x: x[0])

    sa = [pos for (_, pos) in suffixes]

    return sa


def bwt_from_sa(text, sentinel='$'):
    """Build the Burrows-Wheeler transform using the suffix array.

    If the sentinel character already occurs in ``text`` we must not append it
    again as this would shift all indices compared to the suffix array that is
    built from ``text``.  Only append the sentinel when it is absent, mirroring
    the logic used in :func:`build_suffix_array`.
    """

    if sentinel in text:
        t = text
    else:
        t = text + sentinel

    sa = build_suffix_array(text, sentinel)
    
    bwt = []
    for pos in sa:
        if pos == 0:
            bwt.append(sentinel)
        else:
            bwt.append(t[pos-1])
    return ''.join(bwt)
