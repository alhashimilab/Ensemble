"""
pdblib, version 1.1, 08-02-2013
Written by Yi Xue
Copyright: Yi Xue and Skrynnikov's group @Purdue University

A simple python package to manipulate pdb files
pdb.base has not dependence of numpy, and thus does not support advanced
operations such as concatenating two chains, rotating a group of atoms, etc

"""

#import pdb  #for debug

import dummy
import os
from copy import deepcopy,copy
from sys import stdout,exit
from operator import add
from math import sqrt
from common.base import cl,pager,divide,partition
from common.bio import aa_abbr,nt_abbr,resabbr


#====== Atom ===================================================================
class Atom:
    atid = 0
    loc = ' '
    r = None
    charge = None
    elem = ''

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def gettype(self):
        return (self.name[1] if self.name[0].isdigit() else self.name[0])

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def show(self, disp=True):
        output = []
        fmtstr = '%-4s %5d %s'
        attrs = [self.name, self.atid, self.loc]
        if self.r:
            fmtstr += ' '+'%8.3f'*3
            attrs += [self.r[0], self.r[1], self.r[2]]
        else:
            fmtstr += ' '+'   *.***'*3
        if self.charge:
            fmtstr += '  %8.3f'
            attrs += [self.charge]
        else:
            fmtstr += '     *.***'
        output.append((fmtstr+'\n')%tuple(attrs))

        if disp:
            stdout.writelines(output)
        else:
            return output

#====== Residue ================================================================
class Residue:
    name = ''
    resi = 0

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def __init__(self):
        self.atoms = []

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # disp=True: display on screen
    def show(self, fmt='S', disp=True):
        output = []
        try:
            uid = self.uid
        except AttributeError:
            uid = ''
        output.append('%s%03d %-4s %-4s%s\n'%(cl.y, self.resi, self.name, uid,
                      cl.n))

        if fmt.upper() == 'S':
            atstrs = [(at.name+(4-len(at.name))*' ' if at.r else
                       cl.lr+at.name+(4-len(at.name))*' '+cl.n)
                      for at in self.atoms]
            output += ' '.join(atstrs) + '\n'
        else:
            for at in self.atoms:
                output += at.show(disp=False)

        if disp:
            stdout.writelines(output)
        else:
            return output

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Given atom name, return atom object; On failure, return None
    def getat(self, name):
        ats = filter(lambda x: x.name==name, self.atoms)
        if ats:
            return ats[0]
        else:
            return None


#====== Segment ================================================================
class Segment:
    sgid = '    '
    chid = ' '
    nter = False
    cter = False

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def __init__(self, reses=None):
        if reses is None:
            self.reses = []
        else:
            self.reses = reses

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def show(self, fmt='S', disp=True):
        output = ['']
        output.append(cl.g + 'Segment ' + self.sgid +
                      ', # of residue: %d'%len(self.reses) + cl.n + '\n')
        output.append(cl.g + '-'*80 + cl.n + '\n')
        if not self.reses:
            output.append('No residue exists!\n')
        else:
            for res in self.reses:
                output += res.show(fmt, disp=False)

        if disp:
            pager(output)
        else:
            return output


#   def stat(self,items='ra',p=None,result=[],dsp=1):

#       if p: fmt=p.fmt
#       else: fmt='plain'

#       output=[]
#       for item in items:
#           if item=='r':
#               rns=map(lambda x:x.name, self.reses)
#               rcnts={}
#               for rn in rns:
#                   try:
#                       rcnts[rn]+=1
#                   except KeyError:
#                       rcnts[rn]=1
#               if self.type=='peptide' and fmt!='plain':
#                   ks=rcnts.keys()
#                   refns=map(lambda x:x.name, \
#                             filter(lambda x:x.type=='AA',toppar[0][0].values()))
#                   allks=filter(lambda x:x.refname[0] in refns,p.top.values())
#                   msks=set(allks)-set(ks)
#                   for key in msks:
#                       if not rcnts.has_key(key.name):
#                           rcnts[key.name]=0
#               result.append(rcnts)
#               output.append('%s========== Residue Statistics ==========\n'%(cl.g))
#               output.append('%sType: %s\n'%(cl.n,self.type))
#               ks=rcnts.keys()
#               ks.sort()
#               strs=[]
#               total=0
#               for k in ks:
#                   total+=rcnts[k]
#                   if rcnts[k]==0: c=cl.r
#                   else: c=cl.y
#                   strs.append('%s%4s: %s%3d'%(c,k,cl.n,rcnts[k]))
#               N=len(strs)
#               lines=['    '.join(strs[i*4:(i+1)*4])+'\n' for i in range(N/4+int(N%4>0))]
#               output+=lines
#               output.append('%sTotal: %d\n'%(cl.c,total))
#           elif item=='a':
#               atypes=map(lambda x:x.gettype(), self.getats())
#               acnts={}
#               for atype in atypes:
#                   try:
#                       acnts[atype]+=1
#                   except KeyError:
#                       acnts[atype]=1
#               mass=reduce(add,map(lambda x:atmass[x[0]]*x[1],acnts.items()))
#               result+=[acnts,mass]
#               output.append('%s==========  Atom Statistics  ===========\n'%(cl.g))
#               ks=acnts.keys()
#               ks.sort()
#               strs=[]
#               total=0
#               for k in ks:
#                   total+=acnts[k]
#                   strs.append('%s%s: %s%3d'%(cl.y,k,cl.n,acnts[k]))
#               output.append('    '.join(strs)+'\n')
#               output.append('%sTotal: %d    Mass: %f%s\n'%(cl.c,total,mass,cl.n))
#       if dsp:
#           pager(output)
#       else:
#           return output


    def seq(self, fmt='s', dsp=1):    
        #-----------------------------------------------------------------------
        def abbr(resname):
            try:
                name = resabbr[resname]
            except KeyError:
                name = 'X'
            return name
        #-----------------------------------------------------------------------

        resns = map(lambda x: x.name, self.reses)
        if fmt.upper() == 'S':
            return ''.join(map(abbr, resns))
        else:
            return resns

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def getats(self):
        return reduce(add, map(lambda x: x.atoms, self.reses))

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def getindex(self, resi):
        try:
            return map(lambda x: x.resi, self.reses).index(resi)
        except ValueError:
            return None

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def renumber(self, iat=1, ires=None):
        if iat is not None:
            ats = filter(lambda x: x.r, self.getats())
            for i,at in enumerate(ats):
                at.atid = i+iat
        if ires is not None:
            reses = self.reses
            for i,res in enumerate(reses):
                res.resi = i+ires
                for at in res.atoms:
                    at.resi = res.resi


#====== Molecule (or Model) ====================================================
class Mol:
    fmt = 'plain'
    mdid = 0
    top = None
    
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def __init__(self, inp=None):
        self.segs = []
        if isinstance(inp, str):
            # inp is pdb file name
            self.read(inp)
        elif isinstance(inp, Segment):
            # inp is segment, then build a Mol based on this single seg
            self.segs = [inp]

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def read(self, inp):
        nt_atom = set(['HT3','HN3','H3','3HN','3H'])
        ct_atom = set(['OT2','OXT','OB'])
        if isinstance(inp, str):
            lines = open(inp).readlines()
            kwds=('ATOM','HETATM','TER', 'MODEL','ENDMDL','END')
            ##'Q' is pseudo atoms in molmol format pdb files
            lines = filter(lambda x:x[:6].rstrip() in kwds and x[13:14]!='Q',
                           lines)
            ##lgrps: lines of groups; lmds: text lines of models
            lgrps = partition(lines, lambda x: x[:6].rstrip()=='END')
            lmds = reduce(add, [partition(lgrp, lambda x: x[:5]=='MODEL',
                                include='header') for lgrp in lgrps])
            inp = lmds[0]
            if inp[0][:5]=='MODEL':
                self.mdid = int(inp[0].split()[1])
                inp = inp[1:]
            if inp[-1][:6]=='ENDMDL':
                inp = inp[:-1]

        # reading a prot/model
        self.segs = []
        ##lgrps: lines of groups
        lgrps = partition(inp, lambda x: x[:3]=='TER')
        lsegs = reduce(add,
                       [divide(lgrp, lambda x: x[72:76]) for lgrp in lgrps])
        for lseg in lsegs:
            # Building a segment
            seg = Segment()
            lreses = divide(lseg, lambda x: x[22:27])
            for lres in lreses:
                # Building a residue
                res = Residue()
                res.atoms = [readatom(line) for line in lres]
                res.name = res.atoms[0].resn
                res.resi = res.atoms[0].resi
                seg.reses.append(res)
            atns = set(map(lambda x: x.name,seg.reses[0].atoms))
            # assume nter if is_aa and (no H or containing nt_atom)
            if seg.reses[0].name in aa_abbr and \
               ('H' not in map(Atom.gettype, seg.reses[0].atoms) \
               or (nt_atom & atns)):
                seg.nter = True
            atns = set(map(lambda x: x.name,seg.reses[-1].atoms))
            # assume cter if is_aa and (no H or containing ct_atom)
            if seg.reses[-1].name in aa_abbr and \
               ('H' not in map(Atom.gettype, seg.reses[-1].atoms) \
               or (ct_atom & atns)):
                seg.cter = True
            seg.sgid = seg.reses[0].atoms[0].sgid
            seg.chid = seg.reses[0].atoms[0].chid
            self.segs.append(seg)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # update atom entry for these fields: resn, resi, chid, sgid
    def atsync(self):
        for seg in self.segs:
            for res in seg.reses:
                for at in res.atoms:
                    at.resn = res.name
                    at.resi = res.resi
                    at.chid = seg.chid
                    at.sgid = seg.sgid

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def write(self, out, header=['REMARK CREATED BY PDBLIB\n'], sync=True):
        if isinstance(out, str):
            fout = open(out, 'wt')
        else:
            fout = out

        if header:
            fout.writelines(header)

        if sync:
            self.atsync()

        for seg in self.segs:
            for res in seg.reses:
                for at in res.atoms:
                    if at.r:
                        fout.write(writeatom(at))
            fout.write('TER\n')

        if isinstance(out, str):
            fout.write('END\n')
            fout.close()

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def show(self, fmt='S', disp=True):
        output = []
        output.append(('Model %d,'%self.mdid if self.mdid else 'Mol,') +
                       ' # of segment: %d\n'%len(self.segs))
        output.append('='*80 + '\n')
        for seg in self.segs:
            output += seg.show(fmt, disp=False)

        if disp:
            pager(output)
        else:
            return output

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # format prot to a specific format. 'auto': automatically determine fmt
    def format(self, fmt='auto'):
        #-----------------------------------------------------------------------
        # tpl: dict of template residues (from Top). It returns
        # (cnt_at, cnt_res): unrecognized count for atoms and residue
        def resfit(res, tpl):
            try:
                ##ucs: unrecognized counts; rt: residue template
                ucs = [len(set(map(lambda x: x.name, res.atoms))-
                           set(map(lambda x: x.name, rt.atoms)))
                       for rt in tpl[res.name]]
                return (min(ucs), 0)
            except KeyError:
                return (len(res.atoms), 1)
        #-----------------------------------------------------------------------
        # calculate total # of unrecognized atoms and residues for a fmt
        # sample = (norm, nter, cter)
        def getscore(sample, top):
            tpls = (top.norm, top.nter, top.cter)
            ##ucs: unrecognized counts; tgt: target; tpl: template
            ucs = [map(lambda x: resfit(x,tpl), tgt)
                   for tgt,tpl in zip(sample,tpls)]
            ucs = reduce(add, ucs)
            return reduce(lambda x,y: (x[0]+y[0],x[1]+y[1]), ucs)
        #-----------------------------------------------------------------------

        global topset

        if fmt not in fmts and fmt!='auto':
            print('Undefined fmt string! No formatting occurs.')
            return

        if not topset.preset:
            topset.init()

        # design this way so that pdb.format() only run prot.format() once.
        # please see pdb.format() to get the idea
        if not self.top:
            # get unique residues as sample
            norm = []
            nter = []
            cter = []
            for seg in self.segs:
                beg = 0
                end = len(seg.reses)
                if seg.nter:
                    beg += 1
                    nter.append(seg.reses[0])
                if seg.cter:
                    end -=1
                    cter.append(seg.reses[-1])
                norm += seg.reses[beg:end]

            ##*_rn: resname
            norm_rn = map(lambda x:x.name, norm)
            nter_rn = map(lambda x:x.name, nter)
            cter_rn = map(lambda x:x.name, cter)
            norm = [norm[norm_rn.index(resn)] for resn in set(norm_rn)]
            nter = [nter[nter_rn.index(resn)] for resn in set(nter_rn)]
            cter = [cter[cter_rn.index(resn)] for resn in set(cter_rn)]
            sample = (norm, nter, cter)

            # find the most suitable format for the current prot
            scores = map(lambda x: getscore(sample, topset.preset[x]), fmts)
            s_min = min(scores)
            idx_fmt = scores.index(s_min)
            fmtfit = fmts[idx_fmt]
            if s_min == (0, 0):
                print('The format is recognized as %s'%fmtfit)
            else:
                print('The format looks like %s'%fmtfit)
            self.top = deepcopy(topset.preset[fmtfit])

            # build the refined top. tpls: templates
            if s_min != (0, 0):
                tpls1 = map(lambda x: topset.preset[x].norm, fmts)
                tpls2 = map(lambda x: topset.preset[x].nter, fmts)
                tpls3 = map(lambda x: topset.preset[x].cter, fmts)
                if topset.custom.norm:
                    tpls1.append(topset.custom.norm)
                if topset.custom.nter:
                    tpls1.append(topset.custom.nter)
                if topset.custom.cter:
                    tpls1.append(topset.custom.cter)
                alltpls = (tpls1, tpls2, tpls3)
                items = ('norm', 'nter', 'cter')
                for item,tgt,tpls in zip(items, sample, alltpls):
                    mytpl = getattr(self.top, item)
                    # scan sampled residues in res_list 'norm' 'nter' or 'cter'
                    for res in tgt:
                        ##uc: current unrecognized count (atom count only)
                        ##ucs: unrecognized counts
                        ##idx_fmt: index corresponding to s_min for fmt list
                        ur = resfit(res, tpls[idx_fmt])[0]
                        ucs = map(lambda x: resfit(res,x)[0], tpls)
                        idx = ucs.index(min(ucs))
                        if ucs[idx] < ur:
                            mytpl[res.name] = tpls[idx][res.name]
                            self.top.tuned = True
                s_new = getscore(sample, self.top)
                print('uknown: before tuning --- %3d atoms %2d residues'%s_min)
                print('         after tuning --- %3d atoms %2d residues'%s_new)
            print('-'*40)

        # convert unformated prot into most suitable fmt of prot
        if self.fmt == 'plain':
            for seg in self.segs:
                n = len(seg.reses)
                for i,res in enumerate(seg.reses):
                    try:
                        if i==0 and seg.nter:
                            newreses = self.top.nter[res.name]
                        elif i==n-1 and seg.cter:
                            newreses = self.top.cter[res.name]
                        else:
                            newreses = self.top.norm[res.name]
                    except KeyError:
                        print('RES UNKNOWN: %s %2d in MOL#%2d'
                              %(res.name, res.resi, self.mdid))
                        continue

                    ##ucs: uncrcognized counts; rt: residue template
                    ucs = [len(set(map(lambda x: x.name, res.atoms))-
                               set(map(lambda x: x.name, rt.atoms)))
                           for rt in newreses]
                    newres = newreses[ucs.index(min(ucs))]
                    newatns = map(lambda x: x.name, newres.atoms)
                    atns = map(lambda x: x.name, res.atoms)

                    res.uid = newres.uid
                    res.cat = newres.cat
                    ats = res.atoms
                    newats = deepcopy(newres.atoms)
                    for at in ats:
                        try:
                            idx = newatns.index(at.name)
                            at.charge = newats[idx].charge
                            newats[idx] = at
                        except ValueError:
                            print('ATOM UNKNOWN: %-4s in MOL#%2d  RES %s %d'
                              %(at.name, self.mdid, res.name, res.resi))
                    res.atoms = newats

            if self.top.tuned:
                self.fmt = 'auto'
            else:
                self.fmt = self.top.name

        # convert current format into target format "fmt"
        if fmt!='auto' and fmt!=self.fmt:
            # in a "preset" top, uid is unique; in "custom", it is not
            reses = topset.preset[fmt].getreses()
            tbl = dict([(res.uid, res) for res in reses])

            for seg in self.segs:
                for res in seg.reses:
                    try:
                        newres = tbl[res.uid]
                        res.name = newres.name
                        for at,newat in zip(res.atoms, newres.atoms):
                            at.name = newat.name
                    except (AttributeError, KeyError):
                        print('NO CONVERSION: %s %2d in MOL#%2d'
                              %(res.name, res.resi, self.mdid))
            self.fmt = fmt
            self.top = topset.preset[fmt]

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def renumber(self, iat=1, ires=None):
        if iat is not None:
            ats = filter(lambda x: x.r, self.getats())
            for i,at in enumerate(ats):
                at.atid = i+iat
        if ires is not None:
            reses = self.getreses()
            for i,res in enumerate(reses):
                res.resi = i+ires
                for at in res.atoms:
                    at.resi = res.resi

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def getats(self):
        return reduce (add, map(Segment.getats, self.segs))

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def getreses(self):
        return reduce (add, map(lambda x: x.reses, self.segs))

#   def disulf(self):
#       ret=[]
#       assulf=self.atsel('SG','CYS',all=0)
#       while True:
#           N=len(assulf.items)
#           if N<2: break
#           d0=10.0
#           for i1 in range(N):
#               for i2 in range(i1+1,N):
#                   at1=assulf.items[i1][0]
#                   at2=assulf.items[i2][0]
#                   d=atdist(at1,at2)
#                   if d<=3.0 and d<d0:
#                       d0=d
#                       idx=(i1,i2)
#           if d0<=3.0:
#               ret.append((assulf.items[idx[0]][1],assulf.items[idx[1]][1]))
#           i1,i2=idx
#           assulf.items[i2:i2+1]=[]
#           assulf.items[i1:i1+1]=[]
#       return ret



#====== Pdb ====================================================================
class Pdb:
    "A simple PDB python lib written by Yi Xue @ PULSe, Purdue Unversity"
    pass

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def __init__(self, fn=None):
        self.mds = []
        if fn:
            self.read(fn)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def read(self, fn):
        lines = open(fn).readlines()
        kwds=('ATOM','HETATM','TER','MODEL','ENDMDL','END')
        ##'Q' is pseudo atoms in molmol format pdb files
        lines = filter(lambda x:x[:6].rstrip() in kwds and x[13:14]!='Q', lines)

        self.mds = []
        ##lgrps: lines of groups; lmds: text lines of models
        lgrps = partition(lines, lambda x: x[:6].rstrip()=='END')
        lmds = reduce(add, [partition(lgrp, lambda x: x[:5]=='MODEL',
                            include='header') for lgrp in lgrps])
#       pdb.set_trace() #<============ for debug
        for lmd in lmds:
            md = Mol()
            if lmd[0][:5]=='MODEL':
                md.mdid = int(lmd[0].split()[1])
                lmd = lmd[1:]
            if lmd[-1][:6]=='ENDMDL':
                lmd = lmd[:-1]
            md.read(lmd)
            self.mds.append(md)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # update atom entry for these fields: resn, resi, chid, sgid
    def atsync(self):
        for md in self.mds:
            md.atsync()

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # header=1: Print a header line
    def write(self, fn, header=['REMARK CREATED BY PDBLIB\n'], sync=True):
        fout = open(fn, 'wt')

        if header:
            fout.writelines(header)

        if sync:
            self.atsync()

        for md in self.mds:
            if len(self.mds) > 1:
                fout.write('MODEL%9d\n'%md.mdid)
            md.write(fout, header=[], sync=False)
            if len(self.mds) > 1:
                fout.write('ENDMDL\n')

        fout.write('END   \n')
        fout.close()

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def show(self, fmt='S'):
        output = []
        output.append(cl.y + 'PDB file, # of model: %d'%len(self.mds) +
                      cl.n + '\n')
        output.append(cl.y + '+'*80 + cl.n + '\n')
        for md in self.mds:
            output += md.show(fmt, disp=False)
        pager(output)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def format(self, fmt='auto'):
        if self.mds:
            self.mds[0].format(fmt)
        for md in self.mds[1:]:
            md.top = self.mds[0].top
            md.format(fmt)

#   def check(self):
#       output=[]
#       for md in self.mds:
#           for ch in md.chs:
#               output.append('==> Checking model #%d chain %s...\n'%
#                             (md.mdid,ch.chid))
#               result={}
#               for res in ch.reses:
#                   hydrg=[]
#                   heavy=[]
#                   for at in res.getats():
#                       if not at.r:
#                           if at.gettype()=='H': hydrg.append(at.name)
#                           else: heavy.append(at.name)
#                   if hydrg or heavy:
#                       key=(res.name,tuple(hydrg),tuple(heavy))
#                       try: result[key].append(res.resid)
#                       except KeyError: result[key]=[res.resid]
#               if result:
#                   ks=result.keys()
#                   ks.sort()
#                   for key in ks:
#                       strs=(cl.c,key[0],': ',cl.y,' '.join(key[1]), \
#                             cl.r,' '.join(key[2]), \
#                             cl.p,'@',','.join(map(str,result[key])),cl.n)
#                       output.append(''.join(strs)+'\n')
#               else:
#                   strs=(cl.g,'all atoms are present :)',cl.n)
#                   output.append(''.join(strs)+'\n')
#       pager(output)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def renumber(self, iat=1, ires=None):
        for md in self.mds:
            md.renumber(iat, ires)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def getats(self):
        return reduce (add, map(Mol.getats, self.mds))

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def getreses(self):
        return reduce (add, map(Mol.getreses, self.mds))

#   def stat(self):
#       output=[]
#       for i,ch in enumerate(self.mds[0].chs):
#           output.append('')
#           output.append('%s>>>>>>>>>>>> CH%02d <<<<<<<<<<<<\n'%(cl.g,i))
#           output+=ch.stat(p=self,dsp=0)
#           output.append('\n')
#       pager(output)


#====== Topology ===============================================================
class Top:
    name = ''
    tuned = False  # has been tuned during formatting?

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def __init__(self, fn=None):
        self.norm = {}
        self.nter = {}
        self.cter = {}
        if fn:
            self.read(fn)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def read(self, fn):
        #-----------------------------------------------------------------------
        # Note: a single res.name may corresponds to multiple res
        # (e.g. in charmm22.lib, HIS => uid: hip/hie/hid)
        def resapp(res, resdict):
            try:
                resdict[res.name].append(res)
            except KeyError:
                resdict[res.name] = [res]
        #-----------------------------------------------------------------------
        def nterize(res, pres):
            if res.uid != 'pro':
                res.atoms[1:2] = pres[:3]
            else:
                res.atoms[1:1] = pres[3:5]
        #-----------------------------------------------------------------------
        def cterize(res, pres):
            res.atoms[-1:] = pres[5:]
        #-----------------------------------------------------------------------

        lines = open(fn).readlines()
        ##Note: '' also in '#', which excludes empty line
        lines = filter(lambda x: x.lstrip()[:1] not in '#', lines)
        lreses = partition(lines, lambda x: x[:4] in ('RESI','PRES'),
                           include='header')
        lpres = filter(lambda x: x[0].split()[0]=='PRES' ,lreses)
        lresi = filter(lambda x: x[0].split()[0]=='RESI' ,lreses)

        # build self.norm{} and partially build self.nter/cter{}
        # and prepare list of residues to be patched
        self.norm.clear()
        self.nter.clear()
        self.cter.clear()
        ##ters: residues to be patched by nter and cter
        ters = []
        for lres in lresi:
            res = Residue()
            fds = lres[0].split()
            res.name = fds[1]
            res.uid = fds[2]
            res.cat = fds[3]
            for line in lres[1:]:
                at = Atom()
                at.name = line.strip()
                res.atoms.append(at)
            # Note: type 'nt'/'ct' does not appear in regular lib file,
            # but might appear in custom.lib
            if res.cat == 'nt':
                resapp(res, self.nter)
            elif res.cat == 'ct':
                resapp(res, self.cter)
            else:
                resapp(res, self.norm)
                ##in amberFF, ash/glh do not have nter/cter
                if res.cat == 'aa' and res.uid not in ('ash','glh'):
                    ters.append(res)

        # build self.nter/cter{} by patching normal aa in "ters"
        if lpres:
            pres = []
            for line in lpres[0][1:]:
                at = Atom()
                at.name = line.strip()
                pres.append(at)
            for res in ters:
                nter = deepcopy(res)
                nterize(nter, pres)
                nter.uid = 'n' + nter.uid
                nter.cat = 'nt'
                resapp(nter, self.nter)

                cter = deepcopy(res)
                cterize(cter, pres)
                cter.uid = 'c' + cter.uid
                cter.cat = 'ct'
                resapp(cter, self.cter)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # return a residue list for a top
    def getreses(self):
        # "[]" serve as the default return when seq is empty
        reses = reduce(add, self.norm.values() +
                            self.nter.values() +
                            self.cter.values(), [])
        return reses

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def show(self, fmt='S'):
        output = []
        output.append(cl.g + 'Topology, # of residue: %d'%(len(self.getreses()))
                      + cl.n + '\n')
        output.append(cl.g + '-'*80 + cl.n + '\n')

        if self.norm:
            reses = reduce(add, self.norm.values())
            reses.sort(key=lambda x: (x.cat,x.name))
            output.append('>>> Normal residues, %d in total\n'%len(reses))
            for res in reses:
                output += res.show(fmt, disp=False)

        if self.nter:
            reses = reduce(add, self.nter.values())
            reses.sort(key=lambda x: x.name)
            output.append('>>> N-terminal residues, %d in total\n'%len(reses))
            for res in reses:
                output += res.show(fmt, disp=False)

        if self.cter:
            reses = reduce(add, self.cter.values())
            reses.sort(key=lambda x: x.name)
            output.append('>>> C-terminal residues, %d in total\n'%len(reses))
            for res in reses:
                output += res.show(fmt, disp=False)

        pager(output)


#====== Topology Set ===========================================================
class Topset:
    preset = {}
    custom = None

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def init(self):
        #-----------------------------------------------------------------------
        def fillparm(top, parm):
            for res in top.getreses():
                try:
                    for atom,chg in zip(res.atoms,parm[res.uid]):
                        atom.charge = chg
                except KeyError:
                    print('Cannot find %s in parm.dat: '
                          'charges of this residue are not filled in!'%res.uid)
        #-----------------------------------------------------------------------

        libpath = os.path.dirname(dummy.__file__)
        if not libpath:
            libpath=os.path.abspath('.')

        # read in parameter file (parm.dat, only charge dat included)
        fn_parm = libpath+'/toppar/parm.dat'
        parm = {}
        lines = open(fn_parm).readlines()
        ##Note: '' also in '#', which excludes empty line
        lines = filter(lambda x: x.lstrip()[:1] not in '#', lines)
        lreses = partition(lines, lambda x: x[:4]=='RESI', include='header')
        for lres in lreses:
            fds = lres[0].split()
            parm[fds[1]]=map(lambda x: float(x.split()[1]), lres[1:])

        # read in topology files (*.lib)
        self.preset.clear()
        for fmt in fmts:
            fn_lib = libpath+'/toppar/'+fmt+'.lib'
            top = Top(fn_lib)
            top.name = fmt
            fillparm(top, parm)
            self.preset[fmt] = top
        top = Top(libpath+'/toppar/custom.lib')
        top.name = 'custom'
        fillparm(top, parm)
        self.custom = top

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def genabbr(self):
        restab = {}
        for fmt in self.preset:
            restab.update(self.preset[fmt].norm)
            restab.update(self.preset[fmt].nter)
            restab.update(self.preset[fmt].cter)
        reses = reduce(add, restab.values())
        reses = filter(lambda x: x.cat in ('aa','nt','ct'), reses)
        resns = list(set(map(lambda x: x.name, reses)))
        resns.sort()
        out = ["%-6s:'%s'"%("'"+resn+"'",
                            (resabbr[resn] if resabbr.has_key(resn) else '?'))
                            for resn in resns]
        stdout.write(', '.join(out))
        
#====== Public Functions =======================================================
# ==============================================================================
def readatom(line):
    """
    Pdb format:
    1-6:   "ATOM  ";     7-11: ATOM ID
    13-16: Atom Name;    17: Location indicator
    18-20: resname;      22: chain identifier
    23-26: resnum;       27: icode
    31-38: X,real(8.3)   39-46: Y,real(8.3)
    47-54: Z,real(8.3)   55-60: Occupancy
    61-66: TempFactor    73-76: segID
    77-78: element       79-80: Charge
    """
    try:
        atom = Atom()
        atom.atid = int(line[6:11])
        atom.name = line[12:16].strip()
        atom.loc = line[16:17]
        atom.resn = line[17:21].strip()
        if line[26:27].isdigit():
            atom.resi = int(line[22:27])  # charmm pdb reserves icode for resi
        else:
            atom.resi = int(line[22:26])
        atom.chid = line[21:22]
        atom.r = (float(line[30:38]),float(line[38:46]),float(line[46:54]))
        #-------------------------------
        try:
            atom.oc = float(line[54:60])
        except ValueError:
            atom.oc = 1.0
        #-------------------------------
        try:
            atom.bf = float(line[60:66])
        except ValueError:
            atom.bf = 0.0
        #-------------------------------
        atom.sgid = line[72:76]
        atom.elem = line[76:78].strip()
    except ValueError:
        print('ATOM line does not conform to pdb standard!\n')
        exit(1)
    return atom

# ==============================================================================
def writeatom(at):
    fmt = 'ATOM  %5d %4s%1s%-4s%1s%4d    %8.3f%8.3f%8.3f%6.2f%6.2f      ' \
          '%-4s%2s  \n'
    name = (' '+at.name+' '*(3-len(at.name)) if len(at.name)<4 else at.name)
    return fmt%(at.atid, name, at.loc, at.resn, at.chid, at.resi,
                at.r[0], at.r[1], at.r[2], at.oc, at.bf, at.sgid, at.elem)

# ==============================================================================
def atdist(at1, at2):
    r1 = at1.r
    r2 = at2.r
    return sqrt((r1[0]-r2[0])**2+(r1[1]-r2[1])**2+(r1[2]-r2[2])**2)

# ==============================================================================
def getats(obj):
    """
    Generate an atom list from Pdb, Mol, Segment, or Residue.
    If obj is an atom list, the obj itself will be returned.
    """
    if isinstance(obj, (Segment,Mol,Pdb)):
        return obj.getats()
    elif isinstance(obj, Residue):
        return obj.atoms
    elif isinstance(obj, (tuple,list)):
        return obj
    else:
        return None

# ==============================================================================
def getat(obj, resi, name):
    atoms = getats(obj)
    ats = filter(lambda x: x.resi==resi and x.name==name, atoms)
    if len(ats) == 1:
        return ats[0]
    elif len(ats) == 0:
        return None
    else:
        print('ERROR (getat): more than 1 atom are found!')
        exit(1)

# ==============================================================================
def sortat(obj):
    """
    Sort atoms in each residue according to atid
    obj: Pdb, Mol, Segment, or res list
    """
    reses = getreses(obj)
    for res in reses:
        res.atoms.sort(key=lambda at: at.atid)

# ==============================================================================
def getreses(obj):
    """
    Generate an res list from Pdb, Mol, Segment.
    If obj is an res list, the obj itself will be returned.
    """
    if isinstance(obj, (Mol,Pdb)):
        return obj.getreses()
    elif isinstance(obj, Segment):
        return obj.reses
    elif isinstance(obj, (tuple,list)):
        return obj
    else:
        return None

# ==============================================================================
def getres(obj, resi):
    reses = getreses(obj)
    reses = filter(lambda x: x.resi==resi, reses)
    if len(reses) == 1:
        return reses[0]
    elif len(reses) == 0:
        return None
    else:
        print('ERROR (getres): more than 1 residues are found!')
        exit(1)

# ==============================================================================
def gettopset():
    return topset

####### global variable and init code ##########################################
fmts = ['rcsb','charmm22','charmm22_xplor','amber94','ent','molmol']
topset = Topset()
