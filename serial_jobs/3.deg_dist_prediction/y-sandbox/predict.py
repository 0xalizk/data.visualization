import matplotlib.pyplot as plt
from networkx.utils import powerlaw_sequence
import math#powerlaw , math
from ambiguity import amb7 as amb
sys.path.insert(0, os.getenv('lib'))
import fitting_lib 
#import greys_likelihood
#greys = greys_likelihood.grey_likelihood
log10 = math.log10
log2  = math.log2
alpha = 2
################################################################################################################################################
if __name__ == '__main__':
    fig = plt.figure(figsize=(30,30))
    networks = fitting_lib.networks_largestC
    nets  = [n for n in networks_originals().keys() ][0:]
    pos=1
    for key in nets:

        print(key)
        NET = networks()[key]
        deg, freq, e2n_ratio, n2e_ratio = NET['deg'], NET['freq'], NET['edge2node'], NET['node2edge']

        X  =  [x for x in range (1,max(deg)+1, 1)]
        plaw2  =  [ 1.6*(1 / (x**2))     for x in X] # nice straight line
        plaw3  =  [ 1.6*(1 / (x**2))     for x in X]
        
        #amb7
        NEP = [amb(deg,n2e_ratio,e2n_ratio) for deg in X]
        #amb6
        #NEP = [amb(deg,exponent=2.2) for deg in X]
        # amb5
        #NEP  =  [ amb(x)     for x in X  ]

        #NEP = [1-greys(x) for x in X]

        #NEP =  [ 2 / ((x**2)-2) for x in X]

        
        ax = fig.add_subplot(len(nets),1,pos)
        pos+=1
        #ax.loglog(X,plaw3, marker='o', color='blue', linewidth=0,alpha=.75)
        ax.loglog(X,NEP,color='green', marker='o', linewidth=1,alpha=.75)
        ax.loglog(deg,freq,color='red', marker='o', linewidth=0,alpha=.75)
    
        ax.set_ylim([0,100])
        ax.set_xlim([0,300])
        #print (str(powerlaw.Fit(NEP).alpha))
        #print (str(powerlaw.Fit(freq).alpha))
        ax.set_title(key)
        #ax.set_aspect('equal')
    print('saving ..')  
    plt.savefig('../png/plot.png')
    #plt.show()
    