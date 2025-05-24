def chromosome_to_cycle(chromosome):
    nodes = []
    for i in chromosome:
        if i > 0:
            nodes.extend([2*i - 1, 2*i]) #+i -> (2i-1, 2i)
                                         # 2i -> Head, 2i-1 -> Tail
            #print([2*i - 1, 2*i])
        else:
            j = abs(i)
            nodes.extend([2*j, 2*j - 1]) #-i -> (2i,   2i-1)
                                         # 2i-1 -> Head, 2i -> Tail
            #print([2*j, 2*j - 1])
    return nodes

if __name__ == "__main__":
  chrom = [+5, -1, +3, +11, +13, +14, -15, +8, +12, +7, +9, +4, +6, -10, +2, +16]
  cycle = chromosome_to_cycle(chrom)
  print(cycle)
