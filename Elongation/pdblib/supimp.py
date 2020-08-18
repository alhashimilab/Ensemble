from pdblib.num import *
from common.base import range2list
import pdb

#===============================================================================
def supimpose(m1, m0, rg1, rg0):
    '''superimpose m1 on m0
    '''

    # handel rg1, rg0
    if isinstance(rg1, str):
        rg1 = range2list(rg1)
    if isinstance(rg0, str):
        rg0 = range2list(rg0)

    ats_m1 = []
    for res in getreses(m1):
        if res.resi in rg1:
            ats_m1.append(res.getat("C4'"))
            ats_m1.append(res.getat("O3'"))
    ats_m0 = []
    for res in getreses(m0):
        if res.resi in rg0:
            ats_m0.append(res.getat("C4'"))
            ats_m0.append(res.getat("O3'"))
    if len(ats_m1) != len(ats_m0):
        #pdb.set_trace()
        print('supimpose: The overlaid regions have different size!')
        print('  source: ' + ' '.join(map(lambda x: '%d-%s'%(x.resi,x.name),
              ats_m1)))
        print('  target: ' + ' '.join(map(lambda x: '%d-%s'%(x.resi,x.name),
              ats_m0)))
        exit(1)
    # align
    if (isinstance(m1, list) and isinstance(m1[0], Residue)):
        m1 = reduce(add, map(lambda x: x.atoms, m1), [])
    M = getmat(m1)
    A = getmat(ats_m1)
    B = getmat(ats_m0)
    mc_A = mean(A, 0)
    A -= mc_A
    mc_B = mean(B, 0)
    B -= mc_B
    rot,rmsd = matvec.lsqfit(A, B)
    if rot is not None:
        M -= mc_A
        M = dot(M,rot) + mc_B
        putmat(m1, M)
        return rmsd
    else:
        raise Exception, 'The alignment failed!'

#===============================================================================
def res_del(mol, rg):
    ri = range2list(rg)
    for seg in mol.segs:
        seg.reses = [res for res in seg.reses if res.resi not in ri]

#===============================================================================
def res_ins(sg, reses, resi):
    idx = sg.getindex(resi)
    sg.reses[idx+1:idx+1] = reses

#===============================================================================
def getreslist(sg, rg):
    rg = range2list(rg)
    return [res for res in sg.reses if res.resi in rg]

#===============================================================================
def glue(mol1, mol2):
    '''Glue mol2 to mol1
    '''
    nsg1 = len(mol1.segs)
    nsg2 = len(mol2.segs)
    if nsg1==1 and nsg2==1:
        mol1.segs[0].reses = mol1.segs[0].reses + mol2.segs[0].reses
    elif nsg1==1 and nsg2==2:
        mol1.segs[0].reses = mol2.segs[0].reses + mol1.segs[0].reses \
                           + mol2.segs[1].reses
    elif nsg1==2 and nsg2==1:
        mol1.segs[0].reses = mol1.segs[0].reses + mol2.segs[0].reses \
                           + mol1.segs[1].reses
        mol1.segs[1:] = []
    elif nsg1==2 and nsg2==2:
        mol1.segs[0].reses = mol1.segs[0].reses + mol2.sges[0].reses
        mol1.segs[1].reses = mol2.segs[1].reses + mol1.sges[1].reses
    else:
        print('Error: mol1 has %d nt, mol2 has %d nt!'%(nsg1,nsg2))
        exit(1)
    #mol1.renumber(1, 1)
