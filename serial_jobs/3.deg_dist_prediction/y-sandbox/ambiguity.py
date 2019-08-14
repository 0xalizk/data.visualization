import numpy as np, math,sys
import matplotlib.pyplot as plt
import itertools
from scipy.special import comb as nchoosek
fact = math.factorial
log10  = math.log10
log2   = math.log2
def log8(d):
    return math.log(d,10)
####################################################################################
def ONES(p):
    return len([s for s in p if s=='1'])
#-----------------------------------------------------------------------------------
def ZEROS(p):
    return len([s for s in p if s=='0'])
#-----------------------------------------------------------------------------------
def bs(n):
    #print (str(math.ceil(math.log(max(1,n),2))))
    #return bin(n).replace('0b','')#.ljust(math.ceil(math.log(max(1,n),2)),'0')
    yield itertools.product("01", repeat=n)
#-----------------------------------------------------------------------------------
def sdiv(a,b):
    if b==0:
       return a
    return a/b
#-----------------------------------------------------------------------------------
def sratio(a,b):
    return abs(a-b)/max(1,a+b)
#-----------------------------------------------------------------------------------
def l(n):
    return str(n).ljust(20,' ')
#-----------------------------------------------------------------------------------
def r(n):
    return str(n).rjust(20,' ')
#-----------------------------------------------------------------------------------
def BDpairs(deg):
    return [(b,deg-b) for b in range(0,deg+1,1)]
#-----------------------------------------------------------------------------------
def verify(unity):
    try:
        assert unity >=.99999
    except:
        print(" WARNING: unity != 1; unity = "+l(unity))
        pass
####################################################################################
def ReAvg(previous_avg, previous_count, new_value):
    new_count = previous_count+1.0
    new_avg = ((previous_avg*previous_count) + new_value) / new_count
    return new_avg, new_count
####################################################################################
def amb1(deg):
    amb = []
    for b,d in BDpairs(deg):
       if b>d:
          amb.append( sdiv(b,d)*deg  )
       else:
          amb.append( sdiv(d,b)*deg  )
    return np.average(amb)#-math.log2(deg)
####################################################################################
####################################################################################
def amb2(deg):  
    perm   = ["".join(seq) for seq in itertools.product("01", repeat=deg)]   
    #amb    = len([p for p in perm if ONES(p) <= .1*len(p)]) 
    amb    = len([p for p in perm if abs(ONES(p) - ZEROS(p)) <= .01*len(p)])
    print(l(deg)+r(amb))
    #print(str(perm))
    return amb / len(perm) #/(2**deg)
####################################################################################
####################################################################################
def amb3(deg):   # see if you can use amb5 to speed amb3 up
    AsF, CsF = 0,0
    greys = 0
    for i in range(2**deg): # for all permutations 0/1 that edges (=deg) can take
       p = '{0:0{width}b}'.format(i, width=deg)
       #AsF, CsF = ReAvg(AsF,CsF, sratio(ONES(p), ZEROS(p)))
       #print(l(i)+r(p) + r(AsF)+r(CsF)+r(sratio(ONES(p), ZEROS(p))))
       #print('')
       #ratio = sratio(ONES(p), ZEROS(p))
       greys +=  ((sratio(ONES(p), ZEROS(p)))**4)/2
    return greys/(2**deg)      #return AsF
#################################################################################### 
def amb4(deg):
    return 1/2**deg
    return 1/2**(math.log(deg,2))
#################################################################################### 
def amb5(d): # Bernoulli Trials
    prob_beneficial  = .5 #+ math.log(d,2)/d
    prob_detrimental = 1 - prob_beneficial
    
    # d             => node's degree
    # 1<= k <=d      => how many edges must be ONES or ZEROS for the node to be considered ambiguous. The smaller k the stricter the criteria of ambiguity
    
    k1 = math.ceil(math.log2(d))#d-math.ceil(d*.5)
    #k2 = d-math.floor(d*.5)    

    dCk1 = nchoosek(d,k1,exact=True) # equivelantly, dCk = fact(d) / ( fact(k1)*fact(d-k1)  )    
    amb1 = dCk1   *   prob_beneficial**k1   *   prob_detrimental**(d-k1)
    #dCk2 = nchoosek(d,k2,exact=True) 
    #amb2 = dCk2   *   prob_beneficial**k2   *   prob_detrimental**(d-k2)
    
    #amb = (amb1+amb2) / 2
    print('d:'+l(d)+'k:'+l(k1)+'amb1:'+r(amb1))
    return amb1**3 
#################################################################################### 
def amb6(d,exponent=2.2): # weighted Bernoulli Trials
    if d<=0:
        return 0
    if d>250:
        return  amb6(250,exponent)
        
    universe = d**2
    prob_beneficial  = .5 #+ math.log(d,2)/d
    prob_detrimental = 1 - prob_beneficial
    
    p = prob_beneficial
    q = prob_detrimental
    # d             => node's degree
    # 1<= k <=d      => how many edges must be ONES or ZEROS for the node to be considered ambiguous. The smaller k the stricter the criteria of ambiguity
    ambiguity  = []
    unity      = 0
    for k in range(0,d+1,1):
        dCk          = nchoosek(d,k,exact=True) 
        count        = dCk   *   p**k   *   q**(d-k)
        
        ###################################################################
        ambiguity.append(count**exponent) # winner
        ###################################################################
        
        #print('d:'+l(d)+'k:'+l(k)+'count:'+l(count)+'\timpact:'+l(impact)+'(count*impact)**4:  '+l((count*impact)))#+'\tambiguity:'+l(ambiguity))
        unity += count
    #print('\td:'+l(d)+' ambiguity: '+r(np.average(ambiguity))+'\t 1/d**2: '+str(1/(d**2)))
    verify(unity)
    return np.average(ambiguity)
#################################################################################### 
def amb7(d,n2e,e2n): # weighted Bernoulli Trials
    if d<=0:
        return 0
    if d>250:
        return  amb7(250,n2e,e2n)
    prob_beneficial  = .5 #+ math.log(d,2)/d
    prob_detrimental = 1 - prob_beneficial
    
    p = prob_beneficial
    q = prob_detrimental
    ambiguity = []
    unity      = 0
    for k in range(0,d+1,1):

        dCk          = nchoosek(d,k,exact=True) 
        count        = dCk   *   p**k   *   q**(d-k)

        ###################################################################
        ambiguity.append(n2e*(count**(e2n*log10(d)))) # winner
        ###################################################################
  
        #print('d:'+l(d)+'k:'+l(k)+'count:'+l(count)+'\timpact:'+l(impact)+'(count*impact)**4:  '+l((count*impact)))#+'\tambiguity:'+l(ambiguity))
        unity += count

    #print('\td:'+l(d)+' ambiguity: '+r(np.average(ambiguity))+'\t 1/d**2: '+str(1/(d**2)))
    verify(unity)
    return np.average(ambiguity)
#################################################################################### 
def amb8(d,exponent): # weighted Bernoulli Trials
    universe = d**2
    prob_beneficial  = .5 #+ math.log(d,2)/d
    prob_detrimental = 1 - prob_beneficial
    
    p = prob_beneficial
    q = prob_detrimental

    ambiguity = []
    unity      = 0
    for k in range(0,d+1,1):
        dCk          = nchoosek(d,k,exact=True) 
        count        = dCk   *   p**k   *   q**(d-k)
        
        ###################################################################        
        impact       = k/d 
        if k>d/2:
            impact = 1-impact
        #ambiguity +=    impact*count*universe
        ambiguity.append(    1/((count**impact)*universe)    )
        #ambiguity.append((impact*count)**(log10(d)))
        ###################################################################
        
        #pprint('d:'+l(d)+'k:'+l(k)+'count:'+l(count)+'\timpact:'+l(impact)+'(count**impact)*universe:  '+l(1/((count**impact)*universe)))#+'\tambiguity:'+l(ambiguity))
        unity += count
    print('\td:'+l(d)+' ambiguity: '+r(np.average(ambiguity))+'\t 1/d**2: '+str(1/(d**2)))
    verify(unity)
    return np.average(ambiguity)#sdiv(1,ambiguity)
####################################################################################   
def plaw(d,exp):
    return exp*(1/(d**3))
if __name__ == '__main__':
    #--------------------------------------------
    '''
    for deg,color in zip([10,20,300,400,500], ['grey','black','red','green','blue']):
       X,Y=[],[]
       for i in range(deg+1):
          X.append(i)
          Y.append(sratio(i,deg-i))
          print (l(i)+r(deg-i)+r(sratio(i,deg-i)))
       plt.plot(X,Y)
       print('===')
    plt.show()
    '''
    #--------------------------------------------
    #for i in range(1,100,1):
    amb8 (10,2.2)
    #---------------------------------------------
    '''
    for deg in range(1,20):
       perm  = ["".join(seq) for seq in itertools.product("01", repeat=deg)]
       all   = len(perm)
       grey  = 0
       for p in perm:
          #ratio = sratio(ONES(p) , ZEROS(p))
          #if ratio <= .5 and ratio >=.4:
          diff = abs(ONES(p) - ZEROS(p)) / len(p)         
          grey += diff
       print (str(deg).ljust(4,' ')+':'+l(grey/all)+'  vs   '+str(1/deg**2))
    '''
    #---------------------------------------------
    
    #for i in range(10):
       #print(l(i)+r(bs(i))+r(len(BDpairs(i))))
       #print(str('\n'.join(["".join(seq) for seq in itertools.product("01", repeat=i)])))
       #print("="*15+str(i)+"="*15)
    #for deg in range(1,100,1):
       #print (l(deg)+l(int(amb1(deg)))+r(deg**2))
       #print (l(deg)+r(amb2(deg)))
    
    
    #for i in range(1,101,1):
    #    print(l(i)+r(len(BDpairs(i))))
    
    
    #print(str(BDpairs(10)))

    