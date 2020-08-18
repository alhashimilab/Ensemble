
# abbr of amino acid
aa_abbr = {'ALA' :'A', 'ARG' :'R', 'ARG+':'R', 'ASH' :'D', 'ASN' :'N',
           'ASP' :'D', 'CYS' :'C', 'CYX' :'C', 'GLH' :'E', 'GLN' :'Q',
           'GLU' :'E', 'GLY' :'G', 'HID' :'H', 'HIE' :'H', 'HIP' :'H',
           'HIS' :'H', 'HIS+':'H', 'HSD' :'H', 'HSE' :'H', 'HSP' :'H',
           'ILE' :'I', 'LEU' :'L', 'LYS' :'K', 'LYS+':'K', 'MET' :'M',
           'PHE' :'F', 'PRO' :'P', 'SER' :'S', 'THR' :'T', 'TRP' :'W',
           'TYR' :'Y', 'VAL' :'V'}

# abbr of nucleotide
nt_abbr = {'A':'A', 'DA':'A', 'DA5':'A', 'DA3':'A', 'ADE':'A',
                    'RA':'A', 'RA5':'A', 'RA3':'A',
           'G':'G', 'DG':'G', 'DG5':'G', 'DG3':'G', 'GUA':'G',
                    'RG':'G', 'RG5':'G', 'RG3':'G',
           'C':'C', 'DC':'C', 'DC5':'C', 'DC3':'C', 'CYT':'C',
                    'RC':'C', 'RC5':'C', 'RC3':'C',
           'T':'T', 'DT':'T', 'DT5':'T', 'DT3':'T', 'THY':'T',
                    'RT':'T', 'RT5':'T', 'RT3':'T',
           'U':'U', 'DU':'U', 'DU5':'U', 'DU3':'U', 'URA':'U',
                    'RU':'U', 'RU5':'U', 'RU3':'U'}

# merge the two
resabbr = dict(aa_abbr.items() + nt_abbr.items())


atmass={'C'  : 12.011, 'CAL': 40.080, 'CES': 132.900, 'CLA': 35.450,
        'CL-': 35.450, 'H'  :  1.008, 'MG' :  24.305, 'N'  : 14.007,
        'O'  : 15.999, 'POT': 39.102, 'S'  :  32.060, 'SOD': 22.990,
        'NA+': 22.990, 'ZN' : 65.370}


genecode={'UUU':'F','UUC':'F','UUA':'L','UUG':'L',
          'UCU':'S','UCC':'S','UCA':'S','UCG':'S',
          'UAU':'Y','UAC':'Y','UAA':'#','UAG':'#',
          'UGU':'C','UGC':'C','UGA':'#','UGG':'W',
          'CUU':'L','CUC':'L','CUA':'L','CUG':'L',
          'CCU':'P','CCC':'P','CCA':'P','CCG':'P',
          'CAU':'H','CAC':'H','CAA':'Q','CAG':'Q',
          'CGU':'R','CGC':'R','CGA':'R','CGG':'R',
          'AUU':'I','AUC':'I','AUA':'I','AUG':'M',
          'ACU':'T','ACC':'T','ACA':'T','ACG':'T',
          'AAU':'N','AAC':'N','AAA':'K','AAG':'K',
          'AGU':'S','AGC':'S','AGA':'R','AGG':'R',
          'GUU':'V','GUC':'V','GUA':'V','GUG':'V',
          'GCU':'A','GCC':'A','GCA':'A','GCG':'A',
          'GAU':'D','GAC':'D','GAA':'E','GAG':'E',
          'GGU':'G','GGC':'G','GGA':'G','GGG':'G'}

# *: A/U/G/C
# +: A/G
# -: U/C
anticode={'A':('GC*',),      'C':('UG-',),      'D':('GA-',),
          'E':('GA+',),      'F':('UU-',),      'G':('GG*',),
          'H':('CA-',),      'I':('AU-','AUA'), 'K':('AA+',),
          'L':('UU+','CU*'), 'M':('AUG',),      'N':('AA-',),
          'P':('CC*',),      'Q':('CA+',),      'R':('CG*','AG+'),  
          'S':('UC*','AG-'), 'T':('AC*',),      'V':('GU*',),
          'W':('UGG',),      'Y':('UA-',),      '#':('UA+','UGA')}
