'''
Most heatmap tutorials I found online use pyplot.pcolormesh with random sets of
data from Numpy; I just needed to plot x, y, z values stored in lists--without
all the Numpy mumbo jumbo. Here I have code to plot intensity on a 2D array, and
I only use Numpy where I need to (pcolormesh expects Numpy arrays as inputs).
'''
import matplotlib.pyplot as plt
import numpy as np, pickle

likely_interactors, colors, sizes, degrees=None,None,None,None
i=1
with open('data'+str(i)+'.dump','rb') as f:
    binary_interactions_count, interaction_likelihood, target_likelihood, degrees = pickle.load(f)

x=list(set(degrees))
y=list(set(degrees))
#print (str(x))
#print(str(y))
z=[]
for d1 in x:
    z.append([])
    for d2 in y:
        if (d1,d2) in target_likelihood.keys():
            z[-1].append(target_likelihood[(d1,d2)])
        else:
            z[-1].append(0)
print(str(z[0]))
#print (str(x)+'\n'+str(y))
#for i in z:
#    print ('\n'+str(str(i)))

#setup the 2D grid with Numpy
x, y = np.meshgrid(x, y)

#convert intensity (list of lists) to a numpy array for plotting
intensity = np.array(z)

#now just plug the data into pcolormesh, it's that easy!
plt.pcolormesh(x, y, intensity,cmap=plt.cm.viridis)
plt.colorbar() #need a colorbar to show the intensity scale
plt.show() #boom
