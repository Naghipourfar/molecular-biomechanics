dna = input()

# Approach 1
my_list = [str(dna.count('A')), str(dna.count('C')), str(dna.count('G')), str(dna.count('T'))]
print(' '.join(my_list))

# # Approach 2
counts = {'A': 0, 'C': 0, 'G': 0, 'T': 0}
for nuc in dna:
    counts[nuc] += 1

print(' '.join(list(counts.values())))


