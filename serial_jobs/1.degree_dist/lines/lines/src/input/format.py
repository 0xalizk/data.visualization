import os,sys

for d in ['Regulatory']:#['PPI','Regulator','DB_sourced']:
    for root,dirs,files in os.walk(d):
        for F in files:
            Ls = (open(os.path.join(root,F),'r')).readlines()
            for f in Ls:
            #f=os.path.join(root,f)
                f=f.strip()
                
                
                #print(name)
                name=f.split('/')[-1]
                #print(name)
                name=name.split('.')[0]
                #print(name)
                name=name.replace('-PPI','')
                #print(name)
                name=name.replace('NH_','')
                #print(name)
                name=name.replace('NL_','')
                #print(name)
                name=name.replace('RN_','')
                #print(name)
                name=name.replace('-Iso',' Iso')
                print(name.replace('\r','')+' '+f)
                #sys.exit(1)
