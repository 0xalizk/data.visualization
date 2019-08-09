import sys
import networkx as nx
import matplotlib
# Force matplotlib to not use any Xwindows backend. this line must be before 'import' of any pyplot or any other matplotlib submodule
matplotlib.use('Agg')

import matplotlib.pyplot as plt


network_file = str(sys.argv[1])
edges_file = open (network_file,'r') #note: with nx.Graph (undirected), there are 2951  edges, with nx.DiGraph (directed), there are 3272 edges
M=nx.DiGraph() 	
next(edges_file) #ignore the first line
for e in edges_file: 
	interaction = e.split()
	assert len(interaction)>=2
	source, target = str(interaction[0]), str(interaction[1])
	M.add_edge(source, target)
	two_way_edges=0
	for n in M.nodes():
		for targeted_by_n in M[n].keys():
			if n in M[targeted_by_n].keys():
				two_way_edges +=1	
print (M.number_of_nodes(), " nodes, ", M.number_of_edges(), " edges, ",len(nx.dominating_set(M))," dominating set, ",two_way_edges/2," bi-directional edges")
#print (list(M.degree().values()))

linewidths	=0 #node border
nodelist	=M.nodes()
node_size	=[M.degree(a_node) for a_node in nodelist]
node_color	=node_size
style		='dotted'
width		=0.1
vmin		=30    #min(list(M.degree().values()))
vmax		=800  #max(list(M.degree().values())) 
with_labels	=False
cmap		=plt.get_cmap('jet')

print ("draw()..")
nx.draw(M,linewidths=linewidths, nodelist=nodelist, node_size=node_size, style=style, width=width, vmin=vmin, vmax=vmax, with_labels=with_labels, node_color=node_color,cmap=cmap)
#nx.draw(M, linewidths=0, node_color='b')
plt.savefig("draw.png")

print ("draw_random()..")
nx.draw_random(M,linewidths=linewidths, nodelist=nodelist, node_size=node_size, style=style, width=width, vmin=vmin, vmax=vmax, with_labels=with_labels, node_color=node_color,cmap=cmap)
plt.savefig("draw_random.png")

print ("draw_circular()..")
nx.draw_circular(M,linewidths=linewidths, nodelist=nodelist, node_size=node_size, style=style, width=width, vmin=vmin, vmax=vmax, with_labels=with_labels, node_color=node_color,cmap=cmap)
plt.savefig("draw_circular.png")

print ("draw_spectral()..")
nx.draw_spectral(M,linewidths=linewidths, nodelist=nodelist, node_size=node_size, style=style, width=width, vmin=vmin, vmax=vmax, with_labels=with_labels, node_color=node_color,cmap=cmap)
plt.savefig("draw_spectral.png")

print ("draw_shell()..")
nx.draw_shell(M,linewidths=linewidths, nodelist=nodelist, node_size=node_size, style=style, width=width, vmin=vmin, vmax=vmax, with_labels=with_labels, node_color=node_color,cmap=cmap)
plt.savefig("draw_shell.png")

print ("Done ..")
