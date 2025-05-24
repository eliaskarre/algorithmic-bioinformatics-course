def build_suffix_array(text, sentinel='$'):
    if sentinel not in text:
        text = text + sentinel

    suffixes = [(text[i:], i) for i in range(len(text))]

    suffixes.sort(key=lambda x: x[0])

    sa = [pos for (_, pos) in suffixes]

    return sa
