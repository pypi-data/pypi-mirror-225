# residuecontact - A utility package to generate 3D residue distance graph

The residue-contact package provides a set of utilities for generating 3D residue distance graph from PDB files. 

## Quick Run

```python
from residuecontact import get_sifts_pdbresidue_to_uniprot_map, build_PDB_residues_connection_graph
import os
spmap = get_sifts_pdbresidue_to_uniprot_map("pdbresiduemapping.txt")
build_PDB_residues_connection_graph(
    ["1HIP.pdb"], # A list of files, or PDB structures, or structure from PDB bundles
    spmap, # A dictionary of PDB residue ID to Uniprot residue ID
    10, # The maximum distance between two residues to be put in the graph. Note that generating a full distance matrix is very memory intensive.
    "CA", # CA or all. When measuring distance between two residues res-A and res-B, whether to use the distance between the two c-alpha atoms from res-A and res-B, or the shortest distance of all pairs of atoms between res-A and res-B.
    "intra", # intra or inter or all.
    lambda i: os.path.basename(i).split(".")[0],
    output="1HIP_graph.graphml"
)

```


## Detailed usage

To generate a graph, we need (1) a dictionary of PDB residue ID to uniprot residue ID; and (2) the 3D structure files (in PDB format)

### Preparation of PDB residue map

Users could generate their own dictionary, with keys as PDBID_CHAINID_RESSEQ; and value as UNIPROTID_SEQ.

Here we provide two methods to process the map from sifts and alphafold.

```python
from residuecontact import get_sifts_pdbresidue_to_uniprot_map, get_alphafold_pdbresidue_to_uniprot_map
spmap_sifts = get_sifts_pdbresidue_to_uniprot_map("pdbresiduemapping.txt")
spmap_alphafold = get_alphafold_pdbresidue_to_uniprot_map("alphafold2residuemapping.txt")
```

Example of `pdbresiduemapping` file:

```
PDB	Chain	UniProt	MappableResInPDBChainOnUniprotBasis	MappableResInPDBChainOnPDBBasis
1HIP	A	P00260	[38-47,49-81,83-122]	[1-10,12-44,46-85]
5UFW	A	P03372	[309-380,382-416,418-461,465-529,531-535,537-548]	[309-380,382-416,418-461,465-529,531-535,537-548]
5UFW	B	P03372	[306-337,341-380,382-416,418-460,470-529,531-535,537-546]	[306-337,341-380,382-416,418-460,470-529,531-535,537-546]
2LQ8	A	P29397	[1-41,230-353]	[3-43,54-177]
```

Example of `alphafold2residuemapping` file:

```
UniProt	Species	Gene	Structure	Fragment_Num	Total_Fragments	Avg_pLDDT	Avg_Confidence	PDB_Resi	UniProt_Resi	Total_Resi	N_Very_High	Very_High_Resi	N_High	High_Resi	N_Low	Low_Resi	N_Very_Low	Very_Low_Resi
A0A0A7EPL0	ARATH	PIAL1	AF-A0A0A7EPL0-F1-model_v1.pdb.gz	1	1	56.94	Low	[1-847]	[1-847]	847	239	[22,24-40,47-48,51,71-94,117-144,150-156,166-174,177-202,209-247,254-258,277-347,351-356,362-364]	89	[16-21,23,41-46,49-50,52-70,95-101,115-116,145-149,157-162,164-165,175-176,203-208,248-253,259-261,271-276,348-350,357-361,365-366]	31	[1-15,102-107,113-114,163,262-263,268-270,367,382]	488	[108-112,264-267,368-381,383-847]
A0A140JWM8	ARATH	C7162	AF-A0A140JWM8-F1-model_v1.pdb.gz	1	1	92.29	Very High	[1-473]	[1-473]	473	350	[28-39,44-69,73-78,81-104,106,138-189,194-195,197-205,216-217,219-249,258-259,277-278,281-320,324-416,419-448,452-455,458-471]	115	[1-27,40-43,70-72,79-80,105,107-116,125-137,190-193,196,206-215,218,250-257,260-276,279-280,321-323,417-418,449-451,456-457,472-473]	6	[117-119,122-124]	2	[120-121]
```

### Preparation of input structures

For legacy PDB files, one could directly use the files as input.

```python
input_structures = ["1HIP.pdb"]
```

Larger structures are not supported by legacy PDB format, and they were packed in bundle. To read a bundle file, use the following:

```python
structure = PDB_bundle_structure(*(extract_PDB_bundle("7a01-pdb-bundle.tar.gz"))) 
input_structures = [structure]

```

One could input multiple structures at the same time, and only the shortest distance is reported:

```python
input_structures = ["1HIP.pdb", "4MZI.pdb"]
```

### Graph generation

```python
from residuecontact import build_PDB_residues_connection_graph
build_PDB_residues_connection_graph(
    pdbfiles=["1HIP.pdb"], # A list of files, or PDB structures, or structure from PDB bundles
    spmap, # A dictionary of PDB residue ID to Uniprot residue ID
    10,
    "CA", 
    "all",
    pdb_id_func=lambda i: os.path.basename(i).split(".")[0],
    residue_subset=None,
    extra_residue_filter=None,
    output="1HIP_graph.graphml"
)

```

```
pdbfiles: A list of PDB files (or Structures)

spmap: A dictionary to map pdb residue into uniprot residue, with key as PDBID_CHAINID_RESSEQ, value as UNIPROTID_SEQ 

max_distance: Maximum distance between any two residues as connected. One can set a large maximum distance to capture a full distance matrix, but generating a full matrix is very memory intensive.

atommode: calpha/ca or all. When measuring distance between two residues res-A and res-B, whether to use the distance between the two c-alpha atoms from res-A and res-B, or the shortest distance of all pairs of available atoms between res-A and res-B. Distance calculated based on all atoms are always smaller than or equal to that based on only calpha atoms.

chainmode: all or inter or intra. When set to Intra, only pairs of residues from the same chain are analyzed. When set to Inter, only pairs of residues from different chains are analyzed. When set to All, all pairs of residues are analyzed.

pdb_id_func: Convert pdbfile to pdb_id. Not required if a list of structures is provided in pdbfiles

residue_subset: A subset of residues to include.

extra_residue_filter: A filter to remove certain residues that meet the criteria. For example, residue with a high uncertainty in its position in the structure could be removed from the analysis to avoid noise.

output: The output graph file in graphml format


```

### Output

The output graph is in graphml format. 

Each node has an attribute of ID which correspond to the uniprot residues.

```xml
<node id="P36217_204"/>
```

Each edge has the source and target nodes, and has two additional fields (d1) source field refers to the PDB residue pairs with the shortest distance, and the (d0) distance field refers to the distance between the residue pairs. 

```xml
<edge source="P36217_204" target="P36217_80">
  <data key="d0">7.443631014932368</data>
  <data key="d1">P36217_204:5ZIW_A_171;P36217_80:5ZIW_A_47</data>
</edge>
```

### Graph merging

When multiple structures are used to determine the closest distance between two uniprot residues, the graph generated previously can be merged as one by using the following:

```python
from residuecontact import merge_PDB_residues_connection_graphs
merged_graph = merge_PDB_residues_connection_graphs([graph1, graph2])
```

### Validation

When you want to quickly find out the shortest distances of selected pairs of PDB residues, one could use the following:

```python
from residuecontact import find_PDB_residues_distances_separated_by_models
find_PDB_residues_distances_separated_by_models("1HIP", "1HIP.pdb", pairs, "CA")
```
