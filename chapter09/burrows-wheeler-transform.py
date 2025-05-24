def burrows_wheeler_transform(text, sentinel='$'):

    text = text + sentinel
    n = len(text)

    rotations = [text[i:] + text[:i] for i in range(n)]

    rotations.sort()

    bwt = ''.join(rot[-1] for rot in rotations)
    return bwt
