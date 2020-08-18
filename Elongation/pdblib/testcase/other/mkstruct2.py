#!/usr/bin/python

from pdblib.base import *

a = Mol('./charmm.pdb')
a.format()

b = deepcopy(a)
b.format('molmol')

for r1,r2 in zip(getreses(a), getreses(b)):
    if r1.name in ('GLY', 'ARG'):
        r1.atoms = r2.atoms
        r1.name = r2.name

a.write('at_mix.pdb')
