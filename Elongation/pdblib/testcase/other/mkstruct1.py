#!/usr/bin/python

from pdblib.base import *

a = Mol('../amber/ubq-wt.pdb')

for res in getreses(a):
    if res.name in ('GLY','VAL'):
        res.getat('H').name = 'HN'

a.write('at_unk.pdb')

a.format()
