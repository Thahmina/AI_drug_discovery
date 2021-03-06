# Classify the functional group from SMILES notation.
# This code uses the rdkit package.


from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Draw
from rdkit.Chem import FunctionalGroups

from time import time
import csv

start = time()
csvfile = open("fg_smils.csv", 'a')
header = ["pubchemId","functionalGroup", "SMILES"]
writer = csv.writer(csvfile)
writer.writerow(header)

smilesfile = "CID-SMILES"

fgs = FunctionalGroups.BuildFuncGroupHierarchy()


#for filename in filenames:
    
suppl = Chem.SmilesMolSupplier(smilesfile, delimiter=",",
                               smilesColumn=1, nameColumn=0, titleLine=False )

mols = [x for x in suppl if x is not None]
del suppl

print("processing %s with %d valid compounds" % (filename, (len(mols))))

zbbAllFGs = {}

def getFGs(fgs, res):
    if not fgs:
        return
    for x in fgs:
        patt = x.pattern
        tmp = [m for m in mols if m.HasSubstructMatch(patt)]
        # if there are functional groups then check its children also
        if len(tmp):
            res[x.label] = {'mols': tmp, 'pattern': patt}
            #print(x.label, Chem.MolToSmarts(patt))
            getFGs(x.children, res)
        # end if
    # end for

    return


getFGs(fgs, zbbAllFGs)
len(zbbAllFGs)
totalFGs = 0
for fgName in sorted(zbbAllFGs.keys()):
    totalFGs += len(zbbAllFGs[fgName]['mols'])
    #print("%s: Found %d" %(fgName, len(zbbAllFGs[fgName]['mols'])))
    for ml in zbbAllFGs[fgName]['mols']:
        id = ml.GetProp('_Name')
        smiles = Chem.MolToSmiles(ml)
        row = [id, fgName, smiles]
        writer.writerow(row)
    csvfile.flush()


del mols
del zbbAllFGs
print("Total number of functional groups: %d" % (totalFGs))

csvfile.close()
end = time() - start
print(" TOtal time taken: ", end)
