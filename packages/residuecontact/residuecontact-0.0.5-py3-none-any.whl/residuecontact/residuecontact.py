import tarfile
import codecs
import itertools
from collections import defaultdict
from collections import namedtuple
import re

from scipy.spatial import cKDTree
import scipy.spatial.distance

import networkx as nx

from Bio.PDB import PDBParser
import Bio.PDB.Structure

from biodata.delimited import DelimitedReader
from biodata.baseio import create_text_stream

def extract_PDB_bundle(file):
	'''
	Extract PDB bundle
	
	* The bundle file is assumed to be .tar.gz
	* In tar file, there should be
	** a file PDBID-chain-id-mapping.txt for chain mapping.
	** other sub-pdb files with a suffix .pdb that contains the structure information
	
	Returns two variables: the structures (keys: sub-pdb file name, values: PDB structure), chain_id_map (keys: sub-pdb file name, values: dict to convert new chain ID to original chain ID)
	'''
	
	with tarfile.open(file, 'r:gz',) as t:
		filenames = t.getnames()
		chain_id_mapping_files = [filename for filename in filenames if filename.endswith("-chain-id-mapping.txt")]
		if len(chain_id_mapping_files) != 1:
			raise Exception()
		chain_id_mapping_file = chain_id_mapping_files[0]
		pdb_id = chain_id_mapping_file.split("-chain-id-mapping.txt")[0].upper()
		pdb_files = [filename for filename in filenames if filename.endswith(".pdb")]
		chain_id_map = defaultdict(dict)
		with codecs.getreader("utf-8")(t.extractfile(chain_id_mapping_file)) as cf:
			status = None
			for line in cf.readlines():
				line = line.rstrip()
				if status is None:
					for pdb_file in pdb_files:
						if line.startswith(pdb_file):
							status = pdb_file
				else:
					if len(line.strip()) == 0:

						status = None
					else:
						new_chain_id, original_chain_id = line.strip().split()
						chain_id_map[status][new_chain_id] = original_chain_id
		structures = {pdb_file:PDBParser(QUIET=True).get_structure(pdb_id, codecs.getreader("utf-8")(t.extractfile(pdb_file))) for pdb_file in pdb_files}
		return structures, chain_id_map
def _PDB_bundle_structure_chains_generator(models):
	'''
	'''
	for key, model in models.items():
		for chain in model.get_chains():
			yield chain

def PDB_bundle_structure(structures, chain_id_map):
	'''
	'''
	def get_models():
		for modellist in zip(*[structure.get_models() for structure in structures.values()]):
			if len(modellist) != len(structures):
				raise Exception() # Just in case the model number is different in different bundled PDB
			models = dict(zip(structures.keys(), modellist))
			def get_chains():
				return _PDB_bundle_structure_chains_generator(models)
			WrappedModelBundle = namedtuple("WrappedModelBundle", ["get_chains"])
			yield WrappedModelBundle(get_chains)
	
	for modellist in zip(*[structure.get_models() for structure in structures.values()]):
		models = dict(zip(structures.keys(), modellist))
		for key, model in models.items():
			for chain in model.get_chains():
				chain.id = "dummy" + chain_id_map[key][chain.id]
		
	for modellist in zip(*[structure.get_models() for structure in structures.values()]):
		models = dict(zip(structures.keys(), modellist))
		for key, model in models.items():
			for chain in model.get_chains():
				chain.id = chain.id[5:]
	WrappedStructureBundle = namedtuple("WrappedStructureBundle", ["id", "get_models"])
	return WrappedStructureBundle(next(iter(structures.values())).id, get_models)
	
def parse_sifts_range(s):
	'''
	Parse sift ranges. It can be:
	[-1, -1A, 0-100, 100A, 101, 101b]
	'''
	pattern = re.compile("^[0-9]+-[0-9]+$") #1-100
	pattern2 = re.compile("^-[0-9]+$") #-5
	pattern3 = re.compile("^-?[0-9]+[A-Za-z]$") #124A, -4A
	pattern4 = re.compile("^[0-9]+$") #15
	if pattern.match(s):
		start, stop = s.split("-")
		return range(int(start), int(stop) + 1)
	elif pattern2.match(s):
		return [int(s)]
	elif pattern3.match(s):
		return [s]
	elif pattern4.match(s):
		return [int(s)]
	else:
		raise Exception(s)

def _zip_two_ranges(r1, r2):
	r1 = list(r1)
	r2 = list(r2)
	rsum1 = sum(map(len, r1))
	rsum2 = sum(map(len, r2))
	if rsum1 != rsum2:
		raise Exception("Range has a problem!")
	i1 = 0
	i2 = 0
	while i1 < len(r1) and i2 < len(r2):
		if len(r1[i1]) == len(r2[i2]):
			yield (r1[i1], r2[i2])
			i1 += 1
			i2 += 1
		elif len(r1[i1]) > len(r2[i2]):
			assert isinstance(r1[i1], range)
			yield (range(r1[i1].start, r1[i1].start + len(r2[i2])), r2[i2])
			r1[i1] = range(r1[i1].start + len(r2[i2]), r1[i1].stop)
			i2 += 1
		elif len(r1[i1]) < len(r2[i2]):
			assert isinstance(r2[i2], range)
			yield (r1[i1], range(r2[i2].start, r2[i2].start + len(r1[i1])))
			r2[i2] = range(r2[i2].start + len(r1[i1]), r2[i2].stop)
			i1 += 1
		else:
			assert False
	assert i1 == len(r1) and i2 == len(r2)

def get_sifts_pdbresidue_to_uniprot_map(file):
	class PDB_Uniprot_Map_Item():
		def __init__(self, pdb, chain, uniprot, pdb_uniprot_ranges):
			self.pdb = pdb
			self.chain = chain
			self.uniprot = uniprot
			self.pdb_uniprot_ranges = pdb_uniprot_ranges
			
	class PDB_Uniprot_Map():
		def __init__(self, db):
			self.db = db
		def __contains__(self, key):
			pdb, chain, res = key.split("_")
			if pdb not in self.db:
				return False
			if chain not in self.db[pdb]:
				return False
			for pdb_range, uniprot_range in self.db[pdb][chain].pdb_uniprot_ranges:
				resi = None
				try:
					resi = int(res)
				except:
					pass
				if res in pdb_range or (resi is not None and resi in pdb_range):
					return True
			return False
		def __getitem__(self, key):
			pdb, chain, res = key.split("_")
			for pdb_range, uniprot_range in self.db[pdb][chain].pdb_uniprot_ranges:
				resi = None
				try:
					resi = int(res)
				except:
					pass
				if res in pdb_range or (resi is not None and resi in pdb_range):
					if isinstance(uniprot_range, range) and isinstance(pdb_range, range):
						return self.db[pdb][chain].uniprot + "_" + str(resi - pdb_range.start + uniprot_range.start)
					else:
						return f"{self.db[pdb][chain].uniprot}_{uniprot_range[0]}"
	
	
	db = defaultdict(dict)
	with DelimitedReader(file, header=True) as dr:
		for d in dr:
			if any(v == "nan" for v in d.values()):
				continue
			pdb_ranges = list(map(parse_sifts_range, d["MappableResInPDBChainOnPDBBasis"][1:-1].split(",")))
			uniprot_ranges = list(map(parse_sifts_range, d["MappableResInPDBChainOnUniprotBasis"][1:-1].split(",")))
			pdb_uniprot_ranges = list(_zip_two_ranges(pdb_ranges, uniprot_ranges))
			db[d["PDB"]][d["Chain"]] = PDB_Uniprot_Map_Item(d["PDB"],d["Chain"], d["UniProt"], pdb_uniprot_ranges)
			
	return PDB_Uniprot_Map(db)

def get_alphafold_pdbresidue_to_uniprot_map(file):
	'''
	Create an ID-map (dictionary) of alphafold PDB residues to uniprot residues 
	'''
	class PDB_Uniprot_Map_Item():
		def __init__(self, pdb, chain, uniprot, pdb_uniprot_ranges):
			self.pdb = pdb
			self.chain = chain
			self.uniprot = uniprot
			self.pdb_uniprot_ranges = pdb_uniprot_ranges
			
	class PDB_Uniprot_Map():
		def __init__(self, db):
			self.db = db
		def __contains__(self, key):
			pdb, chain, res = re.compile("^(.+)_([^_]+)_([^_]+)$").match(key).groups()
			if pdb not in self.db:
				return False
			if chain not in self.db[pdb]:
				return False
			for pdb_range, uniprot_range in self.db[pdb][chain].pdb_uniprot_ranges:
				resi = None
				try:
					resi = int(res)
				except:
					pass
				if res in pdb_range or (resi is not None and resi in pdb_range):
					return True
			return False
		def __getitem__(self, key):
			pdb, chain, res = re.compile("^(.+)_([^_]+)_([^_]+)$").match(key).groups()
			for pdb_range, uniprot_range in self.db[pdb][chain].pdb_uniprot_ranges:
				resi = None
				try:
					resi = int(res)
				except:
					pass
				if res in pdb_range or (resi is not None and resi in pdb_range):
					if isinstance(uniprot_range, range) and isinstance(pdb_range, range):
						return self.db[pdb][chain].uniprot + "_" + str(resi - pdb_range.start + uniprot_range.start)
					else:
						return f"{self.db[pdb][chain].uniprot}_{uniprot_range[0]}"
	
	
	db = defaultdict(dict)
	with DelimitedReader(file, header=True) as dr:
		for d in dr:
			if any(v == "nan" for v in d.values()):
				continue
			pdb_ranges = list(map(parse_sifts_range, d["PDB_Resi"][1:-1].split(",")))
			uniprot_ranges = list(map(parse_sifts_range, d["UniProt_Resi"][1:-1].split(",")))
			pdb_uniprot_ranges = list(_zip_two_ranges(pdb_ranges, uniprot_ranges))
			chain = 'A'
			db[d["Structure"]][chain] = PDB_Uniprot_Map_Item(d["Structure"],chain, d["UniProt"], pdb_uniprot_ranges)
			
	return PDB_Uniprot_Map(db)

def get_PDB_structure_residue_distance_matrices(structure, max_distance=5, atommode="all", chainmode="all", residue_filter = lambda residue:True):
	'''
	Returns all sparse distance matrices between all pairs of residues in a structure if they are within the maximum distance 
	
	:param structure: PDB structure 
	:param max_distance: Maximum distance between any two atoms as connected
	:param atommode: calpha or all
	:param chainmode: all or inter or intra
	:param residue_filter: A filter for residue
	:return: A tuple of three variables. The first is a set of residue info, the second is a list of atom information, the third is the matrix
	'''
	atommode = atommode.lower()
	chainmode = chainmode.lower()
	
	all_residue_info = set()
	tree_matrice = []
	atom_residue_infos = []	
	for model in structure.get_models():
		atom_coords_dict = {};
		atom_residue_info_dict = {};
		for chain in model.get_chains():
			atom_coords = []
			atom_residue_info = []		
			for residue in chain.get_residues():
				if not residue_filter(residue):
					continue
				residue_id = residue.get_full_id()			
				if atommode == "calpha" or atommode == "ca":
					atoms = [residue["CA"]]
				elif atommode == "all":
					atoms = residue.get_atoms()
				else:
					raise Exception("Unknown mode")
				
				for atom in atoms:
					atom_coords.append(atom.coord)
					atom_residue_info.append(residue_id)
			atom_coords_dict[chain.get_id()] = atom_coords
			atom_residue_info_dict[chain.get_id()] = atom_residue_info
		
		chain_ids = list(atom_coords_dict.keys())
		if chainmode == "all":
			atom_coords = list(itertools.chain.from_iterable(atom_coords_dict[chain_id] for chain_id in chain_ids))
			atom_residue_info = list(itertools.chain.from_iterable(atom_residue_info_dict[chain_id] for chain_id in chain_ids))
			if len(atom_coords) > 0:
				tree = cKDTree(atom_coords)
				tree_matrice.append(tree.sparse_distance_matrix(tree, max_distance, output_type="ndarray"))
				atom_residue_infos.append((atom_residue_info, atom_residue_info))
		elif chainmode == "intra":
			for chain_id in chain_ids:
				atom_coords = atom_coords_dict[chain_id]
				atom_residue_info = atom_residue_info_dict[chain_id]
				if len(atom_coords) > 0:
					tree = cKDTree(atom_coords)
					tree_matrice.append(tree.sparse_distance_matrix(tree, max_distance, output_type="ndarray"))
					atom_residue_infos.append((atom_residue_info, atom_residue_info))
		elif chainmode == "inter":
			tree_dict = {chain_id:(cKDTree(atom_coords_dict[chain_id]) if len(atom_coords_dict[chain_id]) > 0 else None) for chain_id in chain_ids}
			for chain_id1, chain_id2 in itertools.combinations(chain_ids, 2):
				tree1 = tree_dict[chain_id1]
				tree2 = tree_dict[chain_id2]
				atom_residue_info1 = atom_residue_info_dict[chain_id1]
				atom_residue_info2 = atom_residue_info_dict[chain_id2]
				if tree1 is not None and tree2 is not None:
					tree_matrice.append(tree1.sparse_distance_matrix(tree2, max_distance, output_type="ndarray"))
					atom_residue_infos.append((atom_residue_info1, atom_residue_info2))
		else:
			raise Exception("Unknown chain mode")
		all_residue_info.update(itertools.chain.from_iterable(atom_residue_info_dict[chain_id] for chain_id in chain_ids))
	return all_residue_info, atom_residue_infos, tree_matrice

def build_PDB_residues_connection_graph(pdbfiles, spmap, max_distance, atommode, chainmode, pdb_id_func=None, residue_subset=None, extra_residue_filter=None, output=None):
	'''
	Builds a residue connection graph, with edges representing the distance. 
	Given a list of pdb files, generate the output graphml
	
	:param pdbfiles: A list of PDB files (or Structure) as value 
	:param spmap: A dictionary to map pdb residue into uniprot residue, with key as PDBID_CHAINID_RESSEQ, value as UNIPROTID_SEQ 
	:param max_distance: Maximum distance between any two atoms as connected
	:param atommode: calpha or all
	:param chainmode: all or inter or intra
	:param pdb_id_func: Convert pdbfile to pdb_id. Not required if a list of structure is provided in pdbfiles
	:param residue_subset: A subset of uniprot to include.
	:param extra_residue_filter: Other residue filter
	:param output: The output graph file in graphml format
	:return: Connection graph
	
	'''
	def convert_pdb_residue_id(residue_full_id):
		structure_id, model_id, chain_id, (het, resseq, icode) = residue_full_id
		return f"{structure_id}_{chain_id}_{resseq}{icode.strip()}"

	g = nx.Graph()
	for f in pdbfiles:
		if hasattr(f, "id"):
			structure = f
			pdb_id = structure.id
		else:
			pdb_id = pdb_id_func(f)
			pdb_file_handle = create_text_stream(f, "r")
			try:
				structure = PDBParser(QUIET=True).get_structure(pdb_id, pdb_file_handle)
			except:
				print(f"Error occurs in {pdb_id}. Skip.")
				continue
		if residue_subset is None:
			if extra_residue_filter is None:
				residue_filter = lambda residue: convert_pdb_residue_id(residue.get_full_id()) in spmap and "CA" in residue
			else:
				residue_filter = lambda residue: convert_pdb_residue_id(residue.get_full_id()) in spmap and "CA" in residue and extra_residue_filter(residue) 
		else:
			if extra_residue_filter is None:
				residue_filter = lambda residue: convert_pdb_residue_id(residue.get_full_id()) in spmap and "CA" in residue and spmap[convert_pdb_residue_id(residue.get_full_id())] in residue_subset
			else:
				residue_filter = lambda residue: convert_pdb_residue_id(residue.get_full_id()) in spmap and "CA" in residue and spmap[convert_pdb_residue_id(residue.get_full_id())] in residue_subset and extra_residue_filter(residue) 
		all_residue_info, atom_residue_infos, matrice = get_PDB_structure_residue_distance_matrices(structure, max_distance=max_distance, atommode=atommode, chainmode=chainmode, residue_filter=residue_filter)
		g.add_nodes_from(map(lambda rid: spmap[convert_pdb_residue_id(rid)], all_residue_info))
		for (atom_residue_info1, atom_residue_info2), tree_matrix in zip(atom_residue_infos, matrice):
			for i,j, distance in tree_matrix:
				pdb_r1 = convert_pdb_residue_id(atom_residue_info1[i])
				pdb_r2 = convert_pdb_residue_id(atom_residue_info2[j])
				r1 = spmap[pdb_r1]
				r2 = spmap[pdb_r2]
				if pdb_r1 == pdb_r2:
					continue
				if not g.has_edge(r1, r2) or distance < g.get_edge_data(r1, r2)["distance"]:
					g.add_edge(r1, r2, distance=distance, source=f"{r1}:{pdb_r1};{r2}:{pdb_r2}")
	if output is not None:
		nx.write_graphml(g, output)
	return g


def merge_PDB_residues_connection_graphs(graphs):
	'''
	Merge a list of graphs generated from build_PDB_residues_connection_graph into a single graph.
	
	
	'''
	final_graph = nx.Graph()
	for g in graphs:
		final_graph.add_nodes_from(g)
		for node1, node2, v in g.edges(data=True):
			if final_graph.has_edge(node1, node2) and final_graph.edges[node1, node2]["distance"] < v["distance"]:
				continue
			final_graph.add_edge(node1, node2, **v)
	return final_graph

def find_PDB_residues_distances_separated_by_models(pdb_id, f, pdb_residue_pairs, atommode):
	'''
	
	Given a list of PDB residue pairs, extract the distance between residues in each pair. 
	The distance calculation is repeated for each model in the PDB file. 
	
	:param pdb_id: The PDB ID
	:param f: Input PDB file
	:param pdb_residue_pairs: a list of pdb residue pairs. PDB residue is in a format of PDBID_CHAINID_RESSEQ 
	:param atommode: calpha or all

	:return: A list (for each model) of list (for each pdb residue pair) of distances
	
	'''
	def convert_pdb_residue_id(residue_full_id):
		structure_id, model_id, chain_id, (het, resseq, icode) = residue_full_id
		return f"{structure_id}_{chain_id}_{resseq}{icode.strip()}"
	if isinstance(f, Bio.PDB.Structure.Structure):
		structure = f
	else:
		pdb_file_handle = create_text_stream(f, "r")
		try:
			structure = PDBParser(QUIET=True).get_structure(pdb_id, pdb_file_handle)
		except:
			raise Exception(f"Error occurs in {pdb_id}. Skip.")
		
	atommode = atommode.lower()
	
	residue_subset = set(itertools.chain.from_iterable(pdb_residue_pairs))
	residue_filter = lambda residue: "CA" in residue and convert_pdb_residue_id(residue.get_full_id()) in residue_subset

	dists_list = [list() for _ in range(len(pdb_residue_pairs))]
	for model in structure.get_models():
		atom_residue_info = defaultdict(list)
		for chain in model.get_chains():
			
			for residue in chain.get_residues():
				if not residue_filter(residue):
					continue
				residue_id = convert_pdb_residue_id(residue.get_full_id())			
				if atommode == "calpha" or atommode == "ca":
					atoms = [residue["CA"]]
				elif atommode == "all":
					atoms = residue.get_atoms()
				else:
					raise Exception("Unknown mode")
				
				for atom in atoms:
					atom_residue_info[residue_id].append(atom.coord)
		for dists, (p1, p2) in zip(dists_list, pdb_residue_pairs):
			if p1 in atom_residue_info and p2 in atom_residue_info:
				dists.append(min(scipy.spatial.distance.euclidean(p1_coord, p2_coord) for p1_coord, p2_coord in itertools.product(atom_residue_info[p1], atom_residue_info[p2])))
			else:
				dists.append(None)
	return dists_list