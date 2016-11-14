from __future__ import print_function
import os


# Build workflow here:
structures = []
for filename in os.listdir('./'):
    if filename.endswith(".done"):
	structures.append(filename)

#structures = [ 'GaN.cif', 'CdS_mp-672_conventional_standard.cif', 'SrO_mp-2472_conventional_standard.cif']

for structure in structures:
    print('{}'.format(structure))
