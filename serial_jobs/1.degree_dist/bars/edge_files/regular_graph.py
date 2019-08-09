import random,sys,os
import networkx as nx
sys.path.insert(0, os.getenv('lib'))
import init
M = nx.random_regular_graph(2,3352)
'''
out = open ('regular_graph.txt','w')
out.write ('source target sign')
for e in G.edges():
    out.write ('\nN'+str(e[0])+' N'+str(e[1])+' '+str(random.SystemRandom().choice(['+','-'])))
#for n in G.nodes():
#    print (str(G.degree(n))+' ',end='')
#print ("\n\nno. nodes "+str(len(G.nodes())))
#print ("\n\nno. edges "+str(len(G.edges())))
'''

#M = init.load_network({'network_file':'/Users/mohammedalshamrani/Downloads/School/Waldispul/Publishing/Paper_01/v2/fig/02.degree-dist/edge_files/Vinayagam.txt', 'biased':False})

#print (str(sum(list(M.out_degree().values()))))
#print (str(sum(list(M.in_degree().values()))))
print (str(sum(list(M.degree().values()))))
print (str(len(M.edges())))
print (str(len(M.nodes())))
