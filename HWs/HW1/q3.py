dna = input()

# Approach 1
print(dna.replace('T', 'U'))

# Approach 2
seq = []
for nuc in dna:
    seq += [nuc if nuc in ['A', 'C', 'G'] else 'U']

print(''.join(seq))