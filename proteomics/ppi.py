import networkx as nx
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm



def get_interaction(proteins: list, output_format: str = 'tsv', species: str = '9606'):
    if proteins in [None, []]:
        proteins = ['TPH1','COMT','SLC18A2','HTR1B','HTR2C','HTR2A',
                    'MAOA', 'TPH2','HTR1A','HTR7','SLC6A4','GABBR2','POMC','GNAI3',
                    'NPY','ADCY1','PDYN','GRM2','GRM3','GABBR1']

    protein_separator = "%0d"
    proteins_str = protein_separator.join(proteins)
    url = f"https://string-db.org/api/{output_format}/network?identifiers={proteins_str}&species={species}"

    response = requests.get(url)

    lines = response.text.split('\n')
    data = [line.split('\t') for line in lines]

    df = pd.DataFrame(data[1:-1], columns=data[0])

    interactions = df[['preferredName_A', 'preferredName_B', 'score']]

    return interactions

def build_graph(interactions: pd.DataFrame):
    graph = nx.Graph(name='Protein Interaction Graph')
    interactions = np.array(interactions)
    for i in range(len(interactions)):
        interaction = interactions[i]
        a = interaction[0] # protein a node
        b = interaction[1] # protein b node
        w = float(interaction[2]) # score as weighted edge where high scores = low weight
        graph.add_weighted_edges_from([(a, b, w)]) # add weighted edge to graph

    print(nx.info(graph))

    return graph

def visualize_graph(graph: nx.Graph, mode: str = 'simple', cmap: str = 'plasma'):
    if mode == 'simple':
        pos = nx.spring_layout(graph) # position the nodes using the spring layout
        plt.figure(figsize=(11,11), facecolor=[1, 1, 1, 1])
        nx.draw_networkx(graph)
        plt.axis('off')
        plt.show()
    elif mode == 'advanced': 
        # function to rescale list of values to range [newmin,newmax]
        def rescale(l, newmin, newmax):
            arr = list(l)
            return [(x - min(arr))/(max(arr) - min(arr))*(newmax - newmin) + newmin for x in arr]
        # use the matplotlib plasma colormap
        graph_colormap = cm.get_cmap(cmap, 12)
        # node color varies with Degree
        c = rescale([graph.degree(v) for v in graph], 0.0, 0.9) 
        c = [graph_colormap(i) for i in c]
        # node size varies with betweeness centrality - map to range [10,100] 
        # bc = nx.betweenness_centrality(G) # betweeness centrality
        # s =  rescale([v for v in bc.values()],1500,7000)
        # edge width shows 1-weight to convert cost back to strength of interaction 
        ew = rescale([float(graph[u][v]['weight']) for u, v in graph.edges], 0.1, 4)
        # edge color also shows weight
        ec = rescale([float(graph[u][v]['weight']) for u, v in graph.edges], 0.1, 1)
        ec = [graph_colormap(i) for i in ec]

        pos = nx.spring_layout(graph)
        plt.figure(figsize=(19,9),facecolor=[1, 1, 1, 1])
        nx.draw_networkx(graph, pos=pos, with_labels=True, edge_color= ec,width=ew, node_color="#FFA500",
                        font_color='black', font_weight='normal', font_size='11')
        plt.axis('off')
        plt.legend()
        plt.show()
    else: 
        raise Exception("Invalid mode!")
    

