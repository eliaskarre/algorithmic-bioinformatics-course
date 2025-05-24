def random_genome(length):
  alphabet = {"A", "T", "G", "C"}
  string = []
  for i in range(length):
    string.append(random.choice(list(alphabet)))

  return "".join(string)
