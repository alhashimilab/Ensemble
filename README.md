#
Ensemble

This repository contains all experimental validated ensemble from Al-Hashimi lab


### TAR
#### This is the folder including all the HIV-1-TAR Ensembles
#### The Measured RDCs and PALES predicted RDCs for the TAR ensembles were also supplied as a csv file. The measured RDCs is in "rdc" column, the PALES predicted value (after scaling) is in "rdc_pred" column and the scaling factor used for scaling predicted RDC to measured RDC for each alignment are in "scaling" column
#### For FARFAR-NMR ensemble, we also supply the structure after in silico elongation in order to reproduce the results

##### Anton_TAR_Ens_N20.pdb
###### Selected by NMR RDC
###### Anton-MD-NMR Ensemble (N=20)
###### Citation: Salmon L. et al. 2013 JACS

##### FARFAR_TAR_Ens_N20.pdb (PDBID: 7JU1)
###### Selected by NMR RDC
###### FARFAR-NMR Ensemble (N=20)
###### Citation: Shi H. et al. 2020 Nat Commun

### A6-DNA
#### This is the folder including all the A6-DNA duplex Ensemble

##### A6-DNA_Ens_N10.pdb
###### Selected by NMR RDC
###### Amber MD Ensemble (N=10)
###### Citation: Sathyamoorthy B. et al. 2017 NAR

### A6-DNAm1A16
#### This is the folder including all the A6-DNAm1A16 duplex Ensemble

##### A6-DNAm1A16_Ens_N15.pdb
###### Selected by NMR RDC
###### Amber MD Ensemble (N=15)
###### Citation: Sathyamoorthy B. et al. 2017 NAR

### A2-DNA
#### This is the folder including all the A2-DNA duplex Ensemble

##### A2-DNA_Ens_N6.pdb
###### Selected by NMR RDC
###### Amber MD Ensemble (N=6)
###### Citation: Sathyamoorthy B. et al. 2017 NAR

### A2-DNAm1A16
#### This is the folder including all the A2-DNAm1A16 duplex Ensemble

##### A2-DNAm1A16_Ens_N10.pdb
###### Selected by NMR RDC
###### Amber MD Ensemble (N=10)
###### Citation: Sathyamoorthy B. et al. 2017 NAR

### Elongation
#### This is the folder including all the helices used for TAR in-silico elongation
#### The Python Code for elongate TAR helix was put in the same "Elongation" folder: elongate.py and we supply a dummy test case for HIV-1 TAR and do in silico elongation of EI22, EI3, EII22 

##### tar_stem1_el_v3.pdb
###### For elongate TAR Helix I
###### Citation: Salmon L. et al. 2013 JACS

##### tar_stem2_el_v2.pdb 
###### For elongate TAR Helix II
###### Citation: Salmon L. et al. 2013 JACS

