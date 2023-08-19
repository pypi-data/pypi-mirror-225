# reproduce error

def reproduce(smiles, num_conf=3, rdkit_ff='MMFF94'):

    import os
    from rdkit import Chem, Geometry
    from rdkit.Chem import AllChem

    # get threads
    n_threads = os.cpu_count() - 1

    # initialize rdmol
    rdmol = Chem.AddHs(Chem.MolFromSmiles(smiles))

    params = AllChem.EmbedParameters()
    params.useSymmetryForPruning = True
    params.useSmallRingTorsions = True
    params.useMacrocycleTorsions = True
    params.ETversion = 2
    params.pruneRmsThresh = 0.35
    params.numThreads = n_threads
    params.useRandomCoords = True

    # embed and optimized conformers
    AllChem.EmbedMultipleConfs(rdmol, num_conf, params)
    if rdkit_ff == "MMFF94":
        AllChem.MMFFOptimizeMoleculeConfs(rdmol, mmffVariant="MMFF94", numThreads=n_threads)
    elif rdkit_ff == "MMFF94s":
        AllChem.MMFFOptimizeMoleculeConfs(rdmol, mmffVariant="MMFF94s", numThreads=n_threads)
    elif rdkit_ff == "UFF":
        AllChem.UFFOptimizeMoleculeConfs(rdmol, numThreads=n_threads)


    # elements, conformer_coordinates, connectivity_matrix, charges = extract_from_rdmol(rdmol)
    #
    # return elements, conformer_coordinates, connectivity_matrix, charges

if __name__ == '__main__':
    reproduce('CCCCCCCCC1=CC=C2C(C=C(C3=C(C(C)C)C=C(C(C)C)C=C3C(C)C)C4=C2C5=C(C(C6=C(C(C)C)C=C(C(C)C)C=C6C(C)C)=CC7=CC(CCCCCCCC)=CC=C57)OP(O)(O4)=O)=C1')