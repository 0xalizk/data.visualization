import networkx as nx, sys
from ambiguity import amb7 as amb
import operator

def myprint(s):
    sys.stdout.write(s)
    sys.stdout.flush()

N = 10
E = 2

n2e = .4
e2n = 1.7

    
for i in range(N):
	i_cost_before = amb(i, n2e, e2n) #1-amb(i, n2e, e2n)
	#i_cost_after  = amb(i+1, n2e, e2n) #1-amb(i+1, n2e, e2n) # if 1 more edge is added
	#delta_i       = i_cost_after - i_cost_before
	print(str(i)+': '+str(amb(i, n2e, e2n) ))
	#print(str(i)+'->'+str(i+1)+':\t'+str(delta_i))
myprint('\nDone\n')

#next_pair = sorted(SCORES.items(), key=operator.itemgetter(1))[0]


