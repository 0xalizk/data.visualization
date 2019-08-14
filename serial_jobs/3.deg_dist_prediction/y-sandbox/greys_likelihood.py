slices = {    'interval':10,
                                         'segments':{
                                                 1  :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'100:0', 'range':(100,0)},                               
                                                 2  :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'90:10', 'range':(90,10)},
                                                 3  :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'80:20', 'range':(80,20)},
                                                 4  :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'70:30', 'range':(70,30)},
                                                 5  :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'60:40', 'range':(60,40)},
                                                 6  :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'50:50', 'range':(50,50)},                               
                                                 7  :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'40:60', 'range':(40,60)},
                                                 8  :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'30:70', 'range':(30,70)},
                                                 9  :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'20:80', 'range':(20,80)},
                                                 10 :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'10:90', 'range':(10,90)}, 
                                                 11 :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'0:100', 'range':(0,100)},                             
                                                 12 :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'0:0',   'range':(0,0)}
                                                }
}
#-----------------------------------------------------------------------------------
def assign_range(slices, b, d):
    right_key, b2d_ratio, d2b_ratio = 0,0,0
    if b==0 and d==0:
        right_key =   [key for key in slices['segments'].keys() if slices['segments'][key]['range'][0]==0 and  slices['segments'][key]['range'][1]==0]

    elif b>=d: 
        b2d_ratio, d2b_ratio = round((float(b)/float(b+d))*100, 12), round((float(d)/float(b+d))*100,12)
        right_key = [key for key in slices['segments'].keys() if (b2d_ratio-slices['segments'][key]['range'][0]) >=0 and (b2d_ratio-slices['segments'][key]['range'][0]) <slices['interval']  and (slices['segments'][key]['range'][1]-d2b_ratio)>=0 and (slices['segments'][key]['range'][1]-d2b_ratio)<slices['interval'] ]
    
    else:
        b2d_ratio, d2b_ratio = (float(b)/float(b+d))*100, (float(d)/float(b+d))*100
        right_key = [key for key in slices['segments'].keys() if (slices['segments'][key]['range'][0]-b2d_ratio) >=0 and (slices['segments'][key]['range'][0]-b2d_ratio) <slices['interval']  and (d2b_ratio-slices['segments'][key]['range'][1])>=0 and (d2b_ratio-slices['segments'][key]['range'][1])<slices['interval'] ] 
    assert len(right_key)==1
    return slices['segments'][right_key[0]]['range']
#-----------------------------------------------------------------------------------
def l(n):
    return str(n).ljust(5)
#-----------------------------------------------------------------------------------
def r(n):
    return str(n).rjust(10,' ')
#-----------------------------------------------------------------------------------
def ONES(p):
    return len([s for s in p if s=='1'])
#-----------------------------------------------------------------------------------
def ZEROS(p):
    return len([s for s in p if s=='0'])
#-----------------------------------------------------------------------------------
def sratio(a,b):
    if a == 0 or b == 0:
       return 0
    if a > b:
       return b/a
    return a/b
#-----------------------------------------------------------------------------------
def grey_likelihood(deg):  
    all_possiblities = 2**deg
    num_greys = 0
    for i in range(all_possiblities): # for all permutations 0/1 that edges (=deg) can take
        next_permutation = '{0:0{width}b}'.format(i, width=deg)
        bd_ratio = assign_range(  slices, ONES(next_permutation), ZEROS(next_permutation)   )
        if bd_ratio not in [(100,0),(90,10), (0,100),(10,90)]: 
            num_greys +=1        
    return (num_greys/(2**deg)) 
#-----------------------------------------------------------------------------------
if __name__ == '__main__':
    for deg in range(1,15,1):
        print('degree '+l(deg)+ 'has' + r(round(grey_likelihood(deg)*100,2))+'   % chance of being grey')

    print("\n\tHere a gene is considered 'grey' if its b:d ratio is not in 100-90:0-10 (or 0-10:100-90) slices  \n")
