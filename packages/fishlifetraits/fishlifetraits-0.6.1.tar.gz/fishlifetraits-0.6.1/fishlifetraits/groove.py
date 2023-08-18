

import os
import copy
import itertools


import dendropy
import numpy as np
import networkx as nx

import glob
gene_tree = glob.glob("/Users/ulises/Desktop/GOL/data/r1_gt_prota/*.txt_rank1.tree")



def create_edge_list():
    pass


metadata = {}
for gt in gene_tree:

    # taxa list
    _gt_tree = dendropy.Tree.get(
                    path   = gt, 
                    schema = 'newick',
                    preserve_underscores = True
                )

    gt_taxa = [i.taxon.label for i in  _gt_tree.leaf_node_iter()]

    
    # temporal code
    code = os.path.basename(gt).split('.')[1]
    metadata[code] = gt_taxa


G = nx.Graph()

for gt1,gt2 in itertools.combinations(metadata.keys(), 2):
    
    shared_taxa = len(set(metadata[gt1]) & set(metadata[gt2]))
    G.add_edge(gt1,gt2, weight=shared_taxa)


components = nx.connected_components(G)
for component in components:
    print(f'{len(component)}: {component}')



A = nx.adjacency_matrix(G)
maA = A.todense()


G_copy = copy.deepcopy(G)

threshold = 4
to_rm = []
for u,v in G.edges:
    if G[u][v]['weight'] < threshold:
        G_copy.remove_edge(u,v)
        to_rm.append((u,v))
    

nx.draw(G_copy)

components = nx.connected_components(G_copy)
for component in components:
    print(f'{len(component)}')

    

## really well connected
centrality = nx.pagerank(G)

# centrality = nx.katz_centrality_numpy(G, alpha = 0.2, beta = 1, normalized = True, weight = None)
sort_list  = sorted(centrality.items(), key = lambda x: x[1], reverse = True )




first_quartile = sort_list[:int((len(sort_list) + 1)/4)]
fq_nodes = [c for c,v in first_quartile]


lq_nodes = [ c for c,v in list(reversed(sort_list))[:int((len(sort_list) + 1)/4)]]


color_map = []
for node in G:
    # node
    if node in fq_nodes:
        color_map.append('red')
        
    else: 
        color_map.append('green')      

nx.draw(G, node_color=color_map, with_labels=False)
import re

with open('/Users/ulises/Desktop/GOL/data/r1_gt_prota/pageRank_fq_prota.txt', 'w') as f:
    for i in fq_nodes:
        for gt in gene_tree:
            base_gt = os.path.basename(gt)
            if re.findall( i, base_gt ):
                f.write(base_gt + "\n")

lq_nodes = [ c for c,v in list(reversed(sort_list))[:int((len(sort_list) + 1)/4)]]


color_map = []
for node in G:
    # node
    if node in lq_nodes:
        color_map.append('red')
        
    else: 
        color_map.append('green')      

nx.draw(G, node_color=color_map, with_labels=False)
import re



with open('/Users/ulises/Desktop/GOL/data/r1_gt_prota/pageRank_lq_prota.txt', 'w') as f:
    for i in lq_nodes:
        for gt in gene_tree:
            base_gt = os.path.basename(gt)
            if re.findall( i, base_gt ):
                f.write(base_gt + "\n") 