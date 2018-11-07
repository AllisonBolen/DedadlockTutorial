
import time
import random
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import pylab
import networkx as nx

processes = [(lambda x: x)(x) for x in range(0,6)]
resources = [(lambda x: x)(x) for x in range(len(processes), 2+len(processes))]

print(processes)
print(resources)
labels = {0: 'P0', 1: 'P1', 2: 'P2', 3: 'P3', 4: 'P4', 5: 'P5', 6: 'R1', 7: 'R2'}
# G = nx.DiGraph()
# #G = G.to_directed()
#
B = nx.DiGraph()
# B.add_nodes_from(processes, bipartite=0) # Add the node attribute "bipartite"
# B.add_nodes_from(resources, bipartite=1)
B.add_nodes_from(processes+resources)
# B.add_nodes_from(resources)
pos = {}

countP = 1
countR = 1
for node in processes+resources:
    if node in processes:
        B.node[node]['pos'] = (countP*10,10)
        pos[node]=(countP*10,10)
        countP = countP + 1
    if node in resources:
        B.node[node]['pos'] = (countR*10,80)
        pos[node]=(countR*10,80)
        countR = countR + 1


count = 1

nx.draw_networkx_nodes(B, pos,
                           nodelist=processes,
                           node_color='r',
                           node_size=500,
                           alpha=0.8,
                           label="Processes")

nx.draw_networkx_nodes(B, pos,
                           nodelist=resources,
                           node_color='b',
                           node_size=500,
                           alpha=0.8,
                           label="Resources")

nx.draw_networkx_edges(B, pos,
                           edgelist=[(0,6)],
                           width=1, alpha=1, arrows=True, arrowstyle='->', arrowsize=20)


nx.draw_networkx_labels(B, pos, labels, font_size=16)

plt.axis('off')

plt.show()
