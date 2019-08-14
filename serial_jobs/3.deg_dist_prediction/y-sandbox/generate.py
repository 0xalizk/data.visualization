import networkx as nx, sys
from ambiguity import amb7 as amb
import operator

def myprint(s):
    sys.stdout.write(s)
    sys.stdout.flush()

N = 100
E = 90

n2e = N/E
e2n = E/N


M = nx.Graph()
#start with an empty graph of N nodes
for n in range(N):
    M.add_node(n)

assigned_edges = 0

#AMBscores = {}
#for i in range(500):
#    print(str(i))
#    AMBscores[i] = amb(i, n2e, e2n)
#with open ('AMBscores.dump','wb') as f:
#    import pickle
#    pickle.dump(AMBscores,f)
#    f.close()
AMBscores = None
with  open ('AMBscores.dump','rb') as f: 
    import pickle
    AMBscores = pickle.load(f)


while assigned_edges < E :
    
    least_costly=None
    
    for i in range(N):
        #myprint('\n'+'='*50+' '+str(i)+' '+'='*50)
        i_cost_before = 1-AMBscores[M.degree(i)]   #1-amb(M.degree(i), n2e, e2n)
        i_cost_after  = 1-AMBscores[M.degree(i)+1] #1-amb(M.degree(i)+1, n2e, e2n) # if 1 more edge is added
        delta_i       =  i_cost_after - i_cost_before 
        for j in range(N):
            
            if i == j or (i,j) in M.edges() or (j,i) in M.edges():
                continue
            #print(str(M.degree(j+1)))
            j_cost_before = 1-AMBscores[M.degree(j)]   #1-amb(M.degree(j), n2e, e2n)
            j_cost_after  = 1-AMBscores[M.degree(j)+1] #1-amb(M.degree(j)+1, n2e, e2n)

            
            delta_j       =  j_cost_after - j_cost_before 
            
            DELTA = delta_i +  delta_j
            #print(str(j).ljust(4,' ')+str(DELTA).ljust(30,' ')+'vs\t'+str(least_costly))
            
            if least_costly != None:
                if DELTA < least_costly[2]:
                    least_costly=(i,j,DELTA)
            else:
                
                least_costly=(i,j,DELTA)
                #print(str(least_costly)+'\t'+str(i)+'-'+str(j))

    M.add_edge(least_costly[0],least_costly[1])
    

    assigned_edges+=1
    non_zeros = [d for d in M.degree().values() if d!=0]
    myprint('\n'+str(assigned_edges)+'/'+str(E)+': '+str(least_costly))
    myprint(', deg_dist ('+str(len(non_zeros))+'): '+str(sorted(non_zeros))  )

with open ('deterministically_grown.dump','wb') as f:
    import pickle
    pickle.dump(M,f)
myprint('\n'+str(sorted(M.degree().values()) )  )
myprint('\nDone\n')

#next_pair = sorted(SCORES.items(), key=operator.itemgetter(1))[0]


