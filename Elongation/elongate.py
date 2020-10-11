
#!/usr/bin/python

import os
import sys
from supimp import *
from copy import deepcopy

# EI22
print("Make EI22")

inpdir = './test/E0'
oupdir = './test/EI22'
ei22 = Mol("tar_stem1_el_v3.pdb")

for idx, pdbf in enumerate(os.listdir(inpdir)):
    
    print ("--- Working on [%s] (%d of %d) ---"%(pdbf,idx+1,len(os.listdir(inpdir))))
    mol = Mol(os.path.join(inpdir,pdbf))
    ref = deepcopy(ei22)
    supimpose(mol,ref,'2-5,25-28','24-31')
    
    newmol = Mol()
    newmol.segs = [Segment()]
    newmol.segs[0].reses = mol.segs[0].reses[1:-1]+ref.segs[0].reses[0:23]+ref.segs[0].reses[31:]
    
    newmol.renumber(1,2)
    newmol.write(os.path.join(oupdir,pdbf.replace("E0","EI22")))

# EI3
print("Make EI3")

inpdir = './test/EI22'
oupdir = './test/EI3'

for idx, pdbf in enumerate(os.listdir(inpdir)):
    
    print ("--- Working on [%s] (%d of %d) ---"%(pdbf,idx+1,len(os.listdir(inpdir))))

    mol = Mol(os.path.join(inpdir,pdbf))
    newmol = Mol()
    newmol.segs = [Segment()]
    newmol.segs[0].reses = mol.segs[0].reses[46:50]+mol.segs[0].reses[0:27]+mol.segs[0].reses[50:54]
    
    newmol.renumber(1,-2)
    newmol.write(os.path.join(oupdir,pdbf.replace("EI22","EI3")))

# EII22
print("Make EII22")

inpdir = './test/E0'
oupdir = './test/EII22'

for idx, pdbf in enumerate(os.listdir(inpdir)):

    print ("--- Working on [%s] (%d of %d) ---"%(pdbf,idx+1,len(os.listdir(inpdir))))

    mol1 = Mol(os.path.join(inpdir,pdbf))
    mol2 = deepcopy(mol1)
    eii22 = Mol("tar_stem2_el_v2.pdb")
    ref = deepcopy(eii22)

    supimpose(mol1,ref,'10-12,21-23','107-109,156-158')
    supimpose(mol2,ref,'10-12,21-23','129-131,134-136')
    
    
    newmol = Mol()
    newmol.segs = [Segment()]
    newmol.segs[0].reses = mol1.segs[0].reses[0:12]+mol2.segs[0].reses[12:20]+mol1.segs[0].reses[20:29]+ref.segs[0].reses[9:31]+ref.segs[0].reses[33:55]
    
    newmol.renumber(1,1)
    newmol.write(os.path.join(oupdir,pdbf.replace("E0","EII22")))
