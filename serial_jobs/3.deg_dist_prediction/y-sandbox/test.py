from scipy.special import comb as nchoosek

#-----------------------------------------------------------------------------------
def l(n):
    return str(n).ljust(20,' ')
#-----------------------------------------------------------------------------------
def r(n):
    return str(n).rjust(20,' ')

d=20
p=.5
q=.5
for k in range(0,d+1,1):

    dCk          = nchoosek(d,k,exact=True) 
    count        = dCk   *   p**k   *   q**(d-k)
    print (l(k)+r(count*2**d))
    
