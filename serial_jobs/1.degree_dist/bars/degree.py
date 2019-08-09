from scipy import stats as scipy_stats, random
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as mpatches
import networkx as nx, os, sys, math, numpy as np
from matplotlib import rcParams
sys.path.insert(0, os.getenv('lib'))
import utilv4 as util, init
flip = util.flip
#--------------------------------------------------------------------------------------------------
def update_rcParams():
    rcParams['savefig.pad_inches'] = .2

    rcParams['axes.grid']          = True
    rcParams['axes.titlesize']     = 36
    rcParams['axes.labelsize']     = 28

    rcParams['font.family']        = 'Adobe Caslon Pro'  # cursive, http://matplotlib.org/examples/pylab_examples/fonts_demo.html
    rcParams['font.serif']         = 'Helvetica' #['Bitstream Vera Sans', 'DejaVu Sans', 'Lucida Grande', 'Verdana', 'Geneva', 'Lucid', 'Arial', 'Helvetica', 'Avant Garde', 'sans-serif']

    rcParams['figure.titleweight']    = 'bold'
    rcParams['figure.titlesize']      = 45 
    rcParams['figure.subplot.hspace'] = 0.9
    rcParams['figure.subplot.wspace'] = 0.1
    rcParams['figure.subplot.left']   = 0.1
    rcParams['figure.subplot.right']  = 0.9
    rcParams['figure.subplot.top']    = 0.90 # create a space between title and subplots
    rcParams['figure.subplot.bottom'] = 0.1

    rcParams['grid.alpha']         =  1
    rcParams['grid.color']         =  '#b3cccc' #'#63cae9'
    rcParams['grid.linestyle']     =  'solid' # dashed solid dashdot dotted
    rcParams['grid.linewidth']     =  0.5
    rcParams['axes.grid.axis']     =  'both'
    rcParams['axes.grid.which']    =  'major'


    rcParams['xtick.color']        =  'black'    #  ax.tick_params(axis='x', colors='red'). This will set both the tick and ticklabel to this color. To change labels' color, use: for t in ax.xaxis.get_ticklabels(): t.set_color('red')
    rcParams['xtick.direction']    =  'out'      # ax.get_yaxis().set_tick_params(which='both', direction='out')
    rcParams['xtick.labelsize']    =  22
    rcParams['xtick.major.pad']    =  4.0
    rcParams['xtick.major.size']   =  10.0      # how long the tick is
    rcParams['xtick.major.width']  =  1.0
    rcParams['xtick.minor.pad']    =  4.0
    rcParams['xtick.minor.size']   =  2.0
    rcParams['xtick.minor.width']  =  0.5
    rcParams['xtick.minor.visible']=  False


    rcParams['ytick.color']        =  'black'       # ax.tick_params(axis='x', colors='red')
    rcParams['ytick.direction']    =  'out'         # ax.get_xaxis().set_tick_params(which='both', direction='out')
    rcParams['ytick.labelsize']    =  22
    rcParams['ytick.major.pad']    =  4.0
    rcParams['ytick.major.size']   =  10.0
    rcParams['ytick.major.width']  =  1.0
    rcParams['ytick.minor.pad']    =  4.0
    rcParams['ytick.minor.size']   =  4
    rcParams['ytick.minor.width']  =  0.5
    rcParams['ytick.minor.visible']=  True


    rcParams['legend.borderaxespad']   =  0.5
    rcParams['legend.borderpad']       =  0.4
    rcParams['legend.columnspacing']   =  2.0
    rcParams['legend.edgecolor']       =  'inherit'
    rcParams['legend.facecolor']       =  'inherit'
    rcParams['legend.fancybox']        =  False
    rcParams['legend.fontsize']        =  20
    rcParams['legend.framealpha']      =  1
    rcParams['legend.frameon']         =  False
    rcParams['legend.handleheight']    =  0.7
    rcParams['legend.handlelength']    =  2.0
    rcParams['legend.handletextpad']   =  0.8
    rcParams['legend.isaxes']          =  True
    rcParams['legend.labelspacing']    =  0.5
    rcParams['legend.markerscale']     =  1.0
    rcParams['legend.numpoints']       =  2
    rcParams['legend.scatterpoints']   =  3
    rcParams['legend.shadow']          =  False
#--------------------------------------------------------------------------------------------------
def getCommandLineArgs():
    try:
        edge_files = open(str(sys.argv[1]),'r').readlines()
        clean_paths  = []
        clean_titles = []
        for line in edge_files:
            if line[0]=='#':
                continue
            line = line.strip().split()
            t = line[:-1]
            f = line[-1]
            assert os.path.isfile (f)
            clean_titles.append(' '.join(t))
            clean_paths.append(f)
            
        return clean_titles, clean_paths     
    except:
        print ("Usage: python3 deg_dist_histogram_in_pairs.py [/absolute/path/to/input/file.txt (containing abs paths to edge files)]\nExiting..\n")
        sys.exit() 
#--------------------------------------------------------------------------------------------------
def percentages_formatter(x, y):
    if float(x)>=1:
        return str(int(x))+"%"
    else:
        return str(x)+"%" 
#--------------------------------------------------------------------------------------------------
def get_all_degrees(network_files):
    all_degrees = []
    sys.stdout.write("\ndetermining range of degrees for all networks .. please wait")
    sys.stdout.flush()
    for f in network_files:
        M=None
        if f.split('.')[-1]=='txt':
            M     = init.load_network ({'network_file':f,'biased':False}, quite=True)
        else:
            import pickle
            with open(f,'rb') as net:
                M = pickle.load(net)
        d     = list(M.degree().values())
        all_degrees+=d
    sys.stdout.write(" :"+str(min(all_degrees))+' -> '+str(max(all_degrees))+'\n')
    sys.stdout.flush()
    return sorted(list(set(all_degrees)))
#--------------------------------------------------------------------------------------------------    
def deg_dist_combined (degrees, overall_perc, comm_perc, ax, xlims, display_x_label, title="Degree distribution", colors=['forestgreen','#2F67B1'], tick_interval=2.0):

    bar_width   = .35
    ax.set_ylim([.005,100])
    min_x, max_x = xlims[0], xlims[1]
    #ax.set_xlim([min_x-(bar_width*2), max_x+(bar_width*2)])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    #ax.set_title(title)
    ax.text(.5,.8,title, horizontalalignment='center', transform=ax.transAxes, size=30)
    ax.set_xlabel("")
    if display_x_label == True:
        ax.set_xlabel ("degree")
    ax.set_ylabel ("% nodes ")
    ax.tick_params(axis='x', which='major', left='off', right='off', bottom='on', top='off',  labelbottom='on', labeltop='off') # both major and minor ticks
    ax.tick_params(axis='x', which='minor', left='off', right='off', bottom='off', top='off',  labelbottom='off', labeltop='off') # both major and minor ticks
    ax.tick_params(axis='y', which='both', bottom='off', top='off', left='on', right='off',  labelleft='on', labelright='off') # both major and minor ticks             

    labels=[]
    xticks = [x for x in range(min_x, max_x+1,1)]
    for t in xticks:
        if  math.log(t,2)==int(math.log(t,2)):
            labels.append(t)
        else:
            labels.append('')
    ax.set_xticks(xticks)
    ax.set_xticklabels(labels)
    
    locs  = [deg-(bar_width/2.0) for deg in degrees]
    plt.bar(locs, overall_perc, width=bar_width, color=colors[0], align='center', edgecolor='',log=True)
    locs  = [deg+(bar_width/2.0) for deg in degrees]
    plt.bar(locs, comm_perc, width=bar_width, color=colors[1], align='center', edgecolor='',log=True)
    
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(percentages_formatter))
    for t in ax.xaxis.get_ticklabels():
        t.set_color('black')
    
    in_patch =  mpatches.Patch(color='#f5883f', label='% nodes with degree $=d$')
    out_patch = mpatches.Patch(color='#63cae9', label='% nodes with degree $>d$')
    
    plt.legend(handles=[in_patch, out_patch], loc=(.77, 1.05)) # see rcParams above to make changes
    return ax
#--------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    update_rcParams()
    titles, network_files = getCommandLineArgs()
    output_file_name = []
    clean_titles =[]
    for t,f in zip(titles, network_files):
        output_file_name.append(f.split('/')[-1].split('.')[0])
        clean_titles.append(t.replace('_',' '))
    output_file_name = '_'.join(output_file_name)

    all_degrees = get_all_degrees(network_files)
    #with open('all_degrees','wb') as f:
    #    import pickle
    #    pickle.dump(all_degrees,f)
    #all_degrees = None
    #with open('dumps/all_degrees','rb') as f:
    #    import pickle
    #    all_degrees  = pickle.load(f)
    xlims       = [min(all_degrees), max(all_degrees)]
    # use this if you're plotting in rows: fig = plt.figure(figsize=(20*len(network_files), 10))
    fig = plt.figure(figsize=(20, 6*len(network_files))) # width x height
    fig.subplots_adjust(hspace = 1, wspace=.1) #wspace: horizental space between subplots on the same row
    fig.suptitle ("degree distribution")
    
    cols = 1
    rows = len(network_files)
    pos  = 0
    
    for f,title, display_x_label in zip(network_files, clean_titles, [True]*len(network_files)):
        pos += 1
        M = init.load_network ({'network_file':f,'biased':False})
        with open (f.split('/')[-1].split('.')[0]+'.dump','wb') as file:
            import pickle
            pickle.dump(M,file)
        #M=None
        #with open(f,'rb') as file:
        #    import pickle
        #    M = pickle.load(file)
        sys.stdout.write('done loading net '+str(f.split('/')[-1])+'\n')
        sys.stdout.flush()
        degrees         = list(M.degree().values())
        deg_count       = {}
        for deg in set(degrees):
            deg_count[deg]  = degrees.count(deg)
       
        divider             = sum(deg_count.values()) # aka number of nodes
        so_far              = 0
                
        commula_perc, overall_perc = [], []

        for deg in sorted(all_degrees): # we want all networks to have the same ticks
            if deg in deg_count.keys():
                #print(str(deg).ljust(5,' ')+str(deg_count[deg]))
                perc = (float(deg_count[deg])/divider)*100
                overall_perc.append(perc)
                so_far += perc
                commula_perc.append(100-so_far)
            else:
                overall_perc.append(0)
                commula_perc.append(0)

        '''
        print('mind '+str(min(M.degree().values())))
        print('maxd '+str(max(M.degree().values())))
        print('mind-in '+str(min(M.in_degree().values())))
        print('mind-ou '+str(min(M.out_degree().values())))        
        
        print ("(ou_deg, frequency):\n"        +str(ou_d_count)       +  "\navg ou_degrees\n"+str(np.average(list(set(ou_d)))))  
        print ("\n(in_degree, frequency):\n"   +str(in_d_count)  +  "\navg in_degree\n"+str(np.average(list(set(in_d)))))   
        print ('\n')
        print ("M.in_degrees\n" +str(sorted(set(ou_d))))
        print ("avg "+str(np.average(list(set(in_d)))))
        print ('\n')
        print ("M.out_degrees (log):\n"+str(sorted([float("{0:.2f}".format(round(math.log2(int(d)),2)))  for d in set(ou_d) if d!=0])))
        print ('\n')
        print ("M.in_degrees (log):\n" +str(sorted([float("{0:.2f}".format(round(math.log2(int(d)),2))) for d in set(in_d) if d!=0])))
        '''
    
        ax = fig.add_subplot(rows,cols,pos)
        ax = deg_dist_combined(all_degrees, overall_perc, commula_perc, ax, xlims, display_x_label, title, ['#f5883f','#63cae9'], tick_interval=2.0) 
    
    print ("\n\nsaving: "+output_file_name+"_histogram.png")
    plt.savefig(output_file_name+"_histogram.png", dpi=300, bbox_inches="tight")    
#--------------------------------------------------------------------------------------------------
