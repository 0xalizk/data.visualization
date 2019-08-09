import os, sys, time, pickle
sys.path.insert(0, os.getenv('lib'))
import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx, math, numpy as np
import matplotlib.colors as mpl_colors
from matplotlib import rcParams
import pylab
import matplotlib.ticker as ticker
from scipy.stats import itemfreq
from scipy import stats as scipy_stats, random
import pickle
#from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
#from mpl_toolkits.axes_grid1.inset_locator import mark_inset

import utilv4 as util, init
flip = util.flip
####################################################################
def update_rcParams():
    rcParams['savefig.pad_inches'] = .2

    rcParams['axes.grid']          = True
    rcParams['axes.titlesize']     = 36
    rcParams['axes.labelsize']     = 20

    rcParams['font.family']        = 'Adobe Caslon Pro'  # cursive, http://matplotlib.org/examples/pylab_examples/fonts_demo.html
    rcParams['font.serif']         = 'Helvetica' #['Bitstream Vera Sans', 'DejaVu Sans', 'Lucida Grande', 'Verdana', 'Geneva', 'Lucid', 'Arial', 'Helvetica', 'Avant Garde', 'sans-serif']

    rcParams['figure.titleweight']    = 'bold'
    rcParams['figure.titlesize']      = 45 
    rcParams['figure.subplot.hspace'] = 0.2
    rcParams['figure.subplot.wspace'] = 0.1  #wspace: horizental space between subplots on the same row
    rcParams['figure.subplot.left']   = 0.1
    rcParams['figure.subplot.right']  = 0.9
    rcParams['figure.subplot.top']    = 0.9 # create a space between title and subplots
    rcParams['figure.subplot.bottom'] = 0.1

    rcParams['grid.alpha']         =  1
    rcParams['grid.color']         =  '#63cae9'
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
    rcParams['ytick.minor.visible']=  False


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
    rcParams['legend.handletextpad']   =  0
    rcParams['legend.isaxes']          =  True
    rcParams['legend.labelspacing']    =  0.5
    rcParams['legend.markerscale']     =  1.0
    rcParams['legend.numpoints']       =  2
    rcParams['legend.scatterpoints']   =  3
    rcParams['legend.shadow']          =  False
####################################################################
def slash(path):
    return path+(path[-1] != '/')*'/'
####################################################################
def getCommandLineArgs():
    try:
        edge_files = open(str(sys.argv[1]),'r').readlines()
        clean_paths  = []
        clean_titles = []
        for line in edge_files:
            line = line.strip().split()
            t = line[:-1]
            f = line[-1]
            assert os.path.isfile (f)
            clean_titles.append(' '.join(t))
            clean_paths.append(f)
            
        return clean_titles, clean_paths     
    except:
        print ("Usage: python3 bias.py [/absolute/path/to/input/file.txt (containing abs paths to edge files)]\nExiting..\n")
        sys.exit() 
####################################################################
def formatter(x, y):
    if x<=0:
        return ""
    return str(int(x))  
####################################################################
def ff(just,a_float):
    return str(round(a_float,1)).rjust(just,' ')
####################################################################
def print_stats(M):
    print ("TOTAL NO. NODES "+str(len(M.nodes())))
    print ("TOTAL NO. EDGES "+str((M.number_of_edges())))
    
    d               = list(M.degree().values())
    dou             = list(M.out_degree().values())
    din             = list(M.in_degree().values())
   
    d_count         = {x:d.count(x) for x in d}
    dou_count       = {x:dou.count(x) for x in dou}
    din_count       = {x:din.count(x) for x in din}
    
    avg_d            = np.average(d)
    avg_set_d        = np.average(list(set(d)))
    avg_freq_d       = np.average(list(d_count.values()))
    
    avg_ou           = np.average(dou)
    avg_set_ou       = np.average(list(set(dou)))
    avg_freq_ou      = np.average(list(dou_count.values()))
    
    avg_in           = np.average(din)
    avg_set_in       = np.average(list(set(din)))
    avg_freq_in       = np.average(list(din_count.values()))
    
    #total_edges_belonging_to_nodes_whose_ou_degree_is_greater_than_the_average
    d_above_avg      = [x for x in d if x >  avg_d]
    d_below_avg      = [x for x in d if x <= avg_d]   
    d_set_above_avg  = set(list([x for x in d if x >  avg_set_d]))
    d_set_below_avg  = set(list([x for x in d if x <= avg_set_d])) 
    
    dou_above_avg     = [x for x in dou if x >  avg_ou]
    dou_below_avg     = [x for x in dou if x <= avg_ou]
    dou_set_above_avg = set(list([x for x in dou if x >  avg_set_ou]))
    dou_set_below_avg = set(list([x for x in dou if x <= avg_set_ou]))
    
    din_above_avg     = [x for x in din if x >  avg_in]
    din_below_avg     = [x for x in din if x <= avg_in]
    din_set_above_avg = set(list([x for x in din if x >  avg_set_in]))
    din_set_below_avg = set(list([x for x in din if x <= avg_set_in]))
    
    #nodes whose degree is abo above average
    nodes_above = len([n for n in M.nodes() if M.degree(n)> avg_d])
    nodes_below = len([n for n in M.nodes() if M.degree(n)<=avg_d])
    print ("nodes_above_avg "+str(nodes_above))
    print ("nodes_below_avg "+str(nodes_below))
    print ("avg freq d   "+str(avg_freq_d))
    print ("avg freq dou "+str(avg_freq_ou))
    print ("avg freq din "+str(avg_freq_in))
    tmp=0
    for n in M.nodes():
        if d.count(M.degree(n)) > avg_freq_d:
            for s in M.successors(n):
                tmp+=1
    print ("no. edges originating from nodes whose degree frequency is above avg_freq "+str(tmp))
    
    bias_d = [M.degree(n)-avg_d for n in M.nodes() if M.degree(n)>avg_d ]
    print ("bias_d:  \t"+str(sum(bias_d)))
    
    bias_ou_d = [M.out_degree(n)-avg_ou for n in M.nodes() if M.out_degree(n)>avg_ou ]
    print ("bias_ind:\t"+str(sum(bias_ou_d)))
    
    bias_in_d = [M.in_degree(n)-avg_in for n in M.nodes() if M.in_degree(n)>avg_in ]
    print ("bias_oud:\t"+str(sum(bias_in_d)))
    just = 19
    print (                                "avg".rjust(32,' ')   +"  above-avg edges".rjust(just,' ')    +"below-avg edges".rjust(just,' ')    +"above+below".rjust(just,' ')                                +"avg_set ".rjust(just,' ')   +"above-avg_set ".rjust(just,' ')      +"below-avg_set ".rjust(just,' '))
    print ("-"*120)
    print ("deg:".ljust(10,' ')    +'| '   +ff(just,avg_d)       +ff(just,sum(d_above_avg)/2)          + ff(just,sum(d_below_avg)/2)         + ff(just,int((sum(d_below_avg)+sum(d_above_avg))/2))         +ff(just,avg_set_d)           +ff(just,sum(d_set_above_avg))         +ff(just,sum(d_set_below_avg)))           
    print ("ou_deg:".ljust(10,' ') +'| '   +ff(just,avg_ou)      +ff(just,sum(dou_above_avg))           + ff(just,sum(dou_below_avg))          + ff(just,sum(dou_below_avg)+sum(dou_above_avg))                +ff(just,avg_set_ou)          +ff(just,sum(dou_set_above_avg))         +ff(just,sum(dou_set_below_avg)))       
    print ("in_deg:".ljust(10,' ') +'| '   +ff(just,avg_in)      +ff(just,sum(din_above_avg))           + ff(just,sum(din_below_avg))          + ff(just,sum(din_below_avg)+sum(din_above_avg))                +ff(just,avg_set_in)          +ff(just,sum(din_set_above_avg))         +ff(just,sum(din_set_below_avg)))   
    print ("-"*120)
   
   
    print ("(degree, frequency):sum(freq)="+ff(just,sum(d_count.values()))+"\n"        +str(d_count))
    
    
    #print ("\n(ou_deg, frequency):\n"        +str(dou_count))
    #print ("\n(in_degree, frequency):\n"   +str(din_count))
    #print ('------------------------------------------------------------------')
    '''
    print ("M.in_degrees\n" +str(sorted(set(dou))))
    print ("M.out_degrees (log):\n"+str(sorted([float("{0:.2f}".format(round(math.log2(int(d)),2)))  for d in set(dou) if d!=0])))
    print ("M.in_degrees (log):\n" +str(sorted([float("{0:.2f}".format(round(math.log2(int(d)),2))) for d in set(din) if d!=0])))
    '''
####################################################################
def save_figure(network_file):
    plot_dir = slash(slash(os.getcwd())+'plots')
    if not os.path.isdir(plot_dir):
        os.mkdir(plot_dir)

    file_name = (network_file.split('/')[-1]).split('.')[0] 
    plt.savefig(plot_dir+'v2_'+file_name+".png", dpi=300,bbox_inches="tight") # http://matplotlib.org/api/figure_api.html#matplotlib.figure.Figure.savefig
    print ("plotted: "+plot_dir+'v2_'+file_name+".png")
####################################################################
def logify(SIZES):
    mins = min(SIZES)
    offset=0
    if mins<2:
        offset = 2-mins
    oSIZES = [math.pow(math.log(s+offset,2),2) for s in SIZES]
    print ('mins= '+str(mins).ljust(30,' ')+'offset= '+str(offset))
    BEFORE = sorted([s for s in SIZES])
    AFTER = sorted([s for s in oSIZES])
    for i in range(len(SIZES)):
        print (str(BEFORE[i]).ljust(30,' ')+str(AFTER[i]))
    
    return oSIZES 
####################################################################
def scatter_v1(interaction_likelihoods, colors, sizes, ax, title, fig, xlabel, ylabel, log=False):    
    
    sc = None
    Xs, Ys, Ss, Cs, lolim, hilim = [], [], [], [], 0, 0
    for (source_deg,target_deg) in interaction_likelihoods.keys():
        Xs.append (source_deg)
        Ys.append (target_deg)
        Ss.append(sizes[(source_deg, target_deg)])      
        Cs.append(colors[(source_deg, target_deg)])      
        lolim=min(lolim,min(Xs))
        hilim=max(hilim,max(Xs))
    #Ss = logify(Ss)
        
    sc=ax.scatter (Xs, Ys, alpha=.5, marker='o', edgecolors='black',s=[10*s for s in Ss],  c=Cs, cmap=plt.cm.get_cmap('plasma')) 
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_aspect('equal', adjustable='box')
    
    ax.tick_params(axis='x', which='both', left='off', right='off', bottom='on', top='off',  labelbottom='on', labeltop='off') # both major and minor ticks
    ax.tick_params(axis='y', which='both', bottom='off', top='off', left='on', right='off',  labelleft='on', labelright='off') # both major and minor ticks             
    ax.set_xticks(range(lolim, hilim, 1))
    if log==True:
        ax.set_yscale('log', basex=2, basey=2, subsx=[0,2,4,8,16], subsy=[0,2,4,8,16])
        ax.set_xscale('log', basex=2, basey=2, subsx=[0,2,4,8,16], subsy=[0,2,4,8,16])
    else:
        ax.set_yscale('linear', basex=2, basey=2, subsx=[0,2,4,8,16], subsy=[0,2,4,8,16])
        ax.set_xscale('linear', basex=2, basey=2, subsx=[0,2,4,8,16], subsy=[0,2,4,8,16])
    ax.set_xlabel (xlabel)
    ax.set_ylabel (ylabel)
    
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(formatter))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(formatter))
    
    '''
    ax.xaxis.set_major_formatter( formatter )
    ax.xaxis.set_minor_formatter( formatter )
    ax.yaxis.set_major_formatter( formatter )
    ax.yaxis.set_minor_formatter( formatter )

    ax.xaxis.set_major_locator( locator )
    ax.xaxis.set_minor_locator( locator )
    ax.yaxis.set_major_locator( locator )
    ax.yaxis.set_minor_locator( locator )
    '''
    cbar = fig.colorbar(sc, shrink=0.4, pad=0.01, aspect=20, fraction=.2) # 'aspect' ratio of long to short dimensions, # 'fraction' of original axes to use for colorbar
    cbar.outline.set_visible(False)
    cbar.set_label("$Frequency$")
    cbar_ax = cbar.ax
    cbar_ax.tick_params(labelsize=rcParams['legend.fontsize']/2.0) 
    cbar_ax.tick_params(axis='y', which='minor', bottom='off', top='off', left='off', right='off',  labelleft='off', labelright='off')
    cbar_ax.tick_params(axis='y', which='major', bottom='off', top='off', left='off', right='off',  labelleft='off', labelright='on')
    
    return ax
####################################################################
def scatter(interaction_likelihoods, colors, sizes, ax, title, fig, xlabel, ylabel, xlims, ylims, log=False):    
    sc = None
    Xs, Ys, Ss, Cs, lolim, hilim = [], [], [], [], 0, 0
    for (source_deg,target_deg) in interaction_likelihoods.keys():
        Xs.append (source_deg)
        Ys.append (target_deg)
        Ss.append(sizes[(source_deg, target_deg)])      
        Cs.append(colors[(source_deg, target_deg)])      
        lolim=min(lolim,min(Xs))
        hilim=max(hilim,max(Xs))
    #Ss = [math.pow(s,2) for s in Ss]
    tmp = {}
    SOURCES = list(set(Xs))
    TARGETS  = list(set(Ys))
    
    for source in SOURCES:
        tmp[source] = 0
        for target in TARGETS:
            if (source,target) in sizes.keys():
                tmp[source] +=colors[(source,target)]
    #sc=ax.scatter (Xs, Ys, alpha=.7, marker='o', edgecolors='black',s=[30*s for s in Ss],  c=Cs, cmap=plt.cm.get_cmap('plasma')) 

    cmap    = plt.cm.get_cmap('jet')
    bounds  = [.001,.1, 1, 5, 10, 15, 20, 25, 30, 90]#, 50, 60]#, 70, 80, 90, 100] # Im assuming that freq's <=60 for all networks; check subplot titles to make sure this is the case (below I appended max/min freqs in the title)
    norm    = mpl_colors.BoundaryNorm(bounds, ncolors=cmap.N)
    
    


    sc=ax.scatter (Xs, Ys, alpha=.5, marker='o', edgecolors='', s=[400*c for c in Cs], c=Cs, cmap=cmap, norm=norm) 
    #sc=ax.scatter (Xs, Ys, alpha=.5, marker='o', edgecolors='', s=[50*tmp[x] for x in Xs], c=Cs, cmap=cmap, norm=norm) 
    
    if log==True:
        ax.set_yscale('log', basex=2, basey=2, subsx=[0,2,4,8,16,32,64], subsy=[0,2,4,8,16,32,64])
        ax.set_xscale('log', basex=2, basey=2, subsx=[0,2,4,8,16,32,64], subsy=[0,2,4,8,16,32,64])
    else:
        ax.set_yscale('linear', basex=2, basey=2, subsx=range(0,hilim,1), subsy=range(0,hilim,1))
        ax.set_xscale('linear', basex=2, basey=2, subsx=range(0,hilim,1), subsy=range(0,hilim,1))
    ax.set_xlim(xlims)
    ax.set_ylim(ylims)
    
    ax.set_xlabel (xlabel)
    ax.set_ylabel (ylabel)
    ax.spines['top'].set_visible(False)
    #ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.set_aspect('equal', adjustable='box') # doesn't work with log
    ax.grid(which='minor', alpha=0.1)                                                
    ax.grid(which='major', alpha=0.3) 
    
    ax.tick_params(axis='x', which='both', left='off', right='off', bottom='on', top='off',  labelbottom='on', labeltop='off') # both major and minor ticks
    #ax.tick_params(axis='y', which='both', bottom='off', top='off', left='on', right='off',  labelleft='on', labelright='off') # both major and minor ticks             
    ax.tick_params(axis='y', which='both', bottom='off', top='off', left='off', right='on',  labelleft='off', labelright='on')
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(formatter))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(formatter))
    


    cbar = fig.colorbar(sc, shrink=0.4, pad=.08, aspect=20, fraction=.2) # 'aspect' ratio of long to short dimensions, # 'fraction' of original axes to use for colorbar
    cbar.outline.set_visible(False)
    cbar.set_label("$Frequency\,(\%\, interactions)$") # the \, adds a tiny space
    cbar_ax = cbar.ax
    cbar_ax.tick_params(axis='y', which='minor', bottom='off', top='off', left='off', right='off',  labelleft='off', labelright='off')
    cbar_ax.tick_params(axis='y', which='major', bottom='off', top='off', left='off', right='on',  labelleft='off', labelright='on', direction='out', length=4, width=.5, pad=0, labelsize=rcParams['xtick.labelsize']/2.0)
    '''
    axins = zoomed_inset_axes(ax, 6, loc=1)
    axins.set_xlim(20, 30)
    axins.set_ylim(20, 30)
    mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5")
    '''
    #ax.set_xlim([.1,100])
    #ax.set_ylim([.1,100])
    #ax.set_xticklabels([x for x in range(1, hilim+(5-hilim%5)+1, 1) if math.log(x,2)==int(math.log(x,2))])
    '''
    ax.xaxis.set_major_formatter( formatter )
    ax.xaxis.set_minor_formatter( formatter )
    ax.yaxis.set_major_formatter( formatter )
    ax.yaxis.set_minor_formatter( formatter )

    ax.xaxis.set_major_locator( locator )
    ax.xaxis.set_minor_locator( locator )
    ax.yaxis.set_major_locator( locator )
    ax.yaxis.set_minor_locator( locator )
    '''    
    return ax
####################################################################
def get_likely_interactors (M):
    # size  = source X, target y1,y2...yn, size of each y dot = % of sources of degree X targeting that y. Fixed source, % targets
    # color = the number of edges X to Y as a percentage of the total number of edges over the whole network, in log2
    colors = {}
    sizes  = {}
    colors_normalizer = float(len(M.edges())) # colours reflect interaction likelihood relative to the whole networks' edges
    # sizes_normalizer = different for each source; it's equal to number of interactions originating from a source of degree X
    all_degrees = sorted(list(set(M.degree().values())))
    likely_interactors = {}
    for e in M.in_edges_iter():
        source_deg = M.degree(e[0])
        target_deg = M.degree(e[1])
        if (source_deg,target_deg) in likely_interactors.keys():
            likely_interactors[(source_deg,target_deg)] +=1
        else:
            likely_interactors[(source_deg,target_deg)]  =1
    for source, target in likely_interactors.keys():
        colors[(source, target)] = (likely_interactors[(source, target)]/colors_normalizer)*100
    
    for X in all_degrees:
        size_normalizer=0.0
        sources_of_degree_X = [key for key in likely_interactors.keys() if key[0]==X]
        for key in sources_of_degree_X:
            size_normalizer+= likely_interactors[key]#float(sum(likely_interactors[X,target[1]] for target in sources_of_degree_X))
        #print ('size_normalizer: '+str(size_normalizer))
        for tup in sources_of_degree_X:
            sizes[(tup[0],tup[1])] = (float(likely_interactors[(tup[0],tup[1])])/size_normalizer)*100
        #print ('sizes: '+str(sizes))

    '''
    print("="*100+'\n'+'='*100)
    for source in sorted(all_degrees):
        for target in sorted(all_degrees):
            if (source,target) in likely_interactors.keys():
                #print (str(source).ljust(10,' ')+str(target).ljust(10,' ')+str(likely_interactors[(source,target)] ).ljust(10,' ')+str(sizes[(source,target)] ).ljust(30,' ')+str(colors[(source,target)] ).ljust(10,' '))
                print (str(source)+'    '+str(target)+'    '+str(likely_interactors[(source,target)] )+'    '+str(sizes[(source,target)] )+'\t'+str(colors[(source,target)] )+'    ')
   
    print ('all degrees: '+str(all_degrees))
    '''
    return likely_interactors, colors, sizes
####################################################################
def getCOORDs (fig_inch_dims, cols, rows, w2h_ratio=0.5):
    COORDs    = []
    figw_inch = fig_inch_dims[0]
    figh_inch = fig_inch_dims[1]
    ppercent  = .1 # percentage of area to be used for padding 
    totp      = cols*rows

    #everything else is in % of canvas
    Xpads     = (ppercent*figw_inch)/figw_inch # as % of fig width is padding
    Ypads     = (ppercent*figh_inch)/figh_inch # as % of fig height is padding

    xpad      = Xpads/cols
    ypad      = Ypads/rows
    
    axw      = ((figw_inch-(Xpads*figw_inch))/cols)/figw_inch  # as a % of fig width
    axh      = (axw - axw*w2h_ratio) / w2h_ratio #((figh_inch-(Xpads*figh_inch))/cols)/figh_inch      
    
    p, r        = 0, 0
    for i in range(int(totp)): 
        x_shift  = (axw+xpad)*r
        y_shift  = (axh+ypad)*math.floor(p/cols)
        if x_shift==0:
            x_shift = xpad*.05
        if y_shift == 0:
            y_shift = ypad*.05
        
        COORDs.append([x_shift, y_shift, axw, axh])
        
        p+=1
        r+=1
        if p%cols == 0: # starting a new row, zero-out r
            r = 0
    SORTED=[]
    COORDs = COORDs[::-1]
    for i in range(0, len(COORDs), cols):
        for j in COORDs[i:i+cols][::-1]:
            SORTED.append(j)
     
    print ('Xpads: '+str(Xpads)+'\tYpads: '+str(Ypads)+'\tfigw_inch: '+str(figw_inch)+'\tfigh_inch: '+str(figh_inch)+'\txpad: '+str(xpad)+'\typad: '+str(ypad)+'\taxw: '+str(axw)+'\taxh:'+str(axh))
    return  SORTED
##################################################################
def v1():
    update_rcParams()
    titles, network_files = getCommandLineArgs()
    output_file_name = []
    clean_titles =[]
    for t,f in zip(titles, network_files):
        output_file_name.append(f.split('/')[-1].split('.')[0])
        clean_titles.append(t.replace('_',' '))
    output_file_name = '_'.join(output_file_name)
    
    fig = plt.figure(figsize=(20, 6*len(network_files)))
    #fig.suptitle ("Likely interactors")

    rows = len(network_files)
    cols = 1
    pos  = 1
    for f,title, log in zip(network_files, clean_titles, [True, True]):
        M = init.load_network ({'network_file':f,'biased':False})
        #print_stats (M)     
        #likely_interactors = get_likely_interactors(M)
        likely_interactors, colors, sizes = get_likely_interactors(M)
        ax = fig.add_subplot(rows, cols, pos)
        xlabel, ylabel = "Degree of source node", "Degree of target node"
        if pos==1:
            xlabel =""
        ax = scatter_v1(likely_interactors, colors, sizes, ax, "", fig, xlabel, ylabel, log) 
        pos+=1
    save_figure(output_file_name)
    print ('Done')
    sys.exit(1)
##################################################################
if __name__ == "__main__":
    #v1() # call this if you wanna plot the old way, using add_plots instead of add_axes
    update_rcParams()
    titles, network_files = getCommandLineArgs()
    output_file_name, clean_titles = [], []
    
    for t,f in zip(titles, network_files):
        output_file_name.append(f.split('/')[-1].split('.')[0])
        clean_titles.append(t.replace('_',' '))
    output_file_name = '_'.join(output_file_name)
    
    fig_inch_dims = ((2*len(network_files), 2*len(network_files)))
    cols = 1
    rows = len(network_files)
    w2h_ratio=0.5
    
    fig = plt.figure(figsize=fig_inch_dims)    
    coords = getCOORDs (fig_inch_dims, cols, rows, w2h_ratio)

    pos  = 1
    for f,title, log in zip(network_files, clean_titles, [True]*len(network_files)):
        print ('#'*120 +'\n' + ' '*55 + f.split('/')[-1] + '\n' + '#'*120)
        #M = init.load_network ({'network_file':f, 'biased':False})
        #with open ('dumps/'+f.split('/')[-1].split('.')[0]+'.dump', 'wb') as d:
        #    pickle.dump(M,d)
        M=None
        with open ('dumps/'+f.split('/')[-1].split('.')[0]+'.dump', 'rb') as d:
            M = pickle.load(d)
        print_stats (M)     
        likely_interactors, colors, sizes = get_likely_interactors(M)
        ax = fig.add_axes(coords[pos-1])
        xlabel, ylabel = "Degree of source node", "Degree of target node"
        ax = scatter(likely_interactors, colors, sizes, ax, "", fig, xlabel, ylabel, [.5,64], [.5,64], log) 
        pos+=cols

    save_figure(output_file_name)
    