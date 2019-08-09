import os, sys, time, pickle
import seaborn as sns
sys.path.insert(0, os.getenv('lib'))
import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx, math, numpy as np
import matplotlib.colorbar as mplcbar
from matplotlib import rcParams
import pylab
import matplotlib.ticker as ticker
from scipy.stats import itemfreq
from scipy import stats as scipy_stats, random

import utilv4 as util, init
flip = util.flip
####################################################################
def update_rcParams():
    rcParams['font.family']        = 'Adobe Caslon Pro'  # cursive, http://matplotlib.org/examples/pylab_examples/fonts_demo.html
    rcParams['font.serif']         = 'Helvetica' #['Bitstream Vera Sans', 'DejaVu Sans', 'Lucida Grande', 'Verdana', 'Geneva', 'Lucid', 'Arial', 'Helvetica', 'Avant Garde', 'sans-serif']
    rcParams['xtick.major.pad']=0
    rcParams['ytick.major.pad']=0
    
    '''
    rcParams['savefig.pad_inches'] = .2

    rcParams['axes.grid']          = True
    rcParams['axes.titlesize']     = 30
    rcParams['axes.labelsize']     = 10


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
    rcParams['xtick.labelsize']    =  20
    rcParams['xtick.major.pad']    =  4.0
    rcParams['xtick.major.size']   =  5.0      # how long the tick is
    rcParams['xtick.major.width']  =  1.0
    rcParams['xtick.minor.pad']    =  4.0
    rcParams['xtick.minor.size']   =  2.0
    rcParams['xtick.minor.width']  =  0.5
    rcParams['xtick.minor.visible']=  False


    rcParams['ytick.color']        =  'black'       # ax.tick_params(axis='x', colors='red')
    rcParams['ytick.direction']    =  'out'         # ax.get_xaxis().set_tick_params(which='both', direction='out')
    rcParams['ytick.labelsize']    =  20
    rcParams['ytick.major.pad']    =  4.0
    rcParams['ytick.major.size']   =  5.0
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
    '''
####################################################################
def setup():
    titles, network_files = getCommandLineArgs()
    output_file_name, clean_titles = [], []
    for t,f in zip(titles, network_files):
        output_file_name.append(f.split('/')[-1].split('.')[0])
        clean_titles.append(t.replace('_',' '))
    output_file_name = '_'.join(output_file_name)
    return clean_titles, network_files, output_file_name
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
    print ("===========================================================================================================================================================================================================")
    print ("deg:".ljust(10,' ')    +'| '   +ff(just,avg_d)       +ff(just,sum(d_above_avg)/2)          + ff(just,sum(d_below_avg)/2)         + ff(just,int((sum(d_below_avg)+sum(d_above_avg))/2))         +ff(just,avg_set_d)           +ff(just,sum(d_set_above_avg))         +ff(just,sum(d_set_below_avg)))           
    print ("ou_deg:".ljust(10,' ') +'| '   +ff(just,avg_ou)      +ff(just,sum(dou_above_avg))           + ff(just,sum(dou_below_avg))          + ff(just,sum(dou_below_avg)+sum(dou_above_avg))                +ff(just,avg_set_ou)          +ff(just,sum(dou_set_above_avg))         +ff(just,sum(dou_set_below_avg)))       
    print ("in_deg:".ljust(10,' ') +'| '   +ff(just,avg_in)      +ff(just,sum(din_above_avg))           + ff(just,sum(din_below_avg))          + ff(just,sum(din_below_avg)+sum(din_above_avg))                +ff(just,avg_set_in)          +ff(just,sum(din_set_above_avg))         +ff(just,sum(din_set_below_avg)))   
    print ("===========================================================================================================================================================================================================")
   
   
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
    plt.savefig(plot_dir+'heatmap_'+file_name+".png", dpi=100,bbox_inches="tight") # http://matplotlib.org/api/figure_api.html#matplotlib.figure.Figure.savefig
    print ("plotted: "+plot_dir+'heatmap_'+file_name+".png")
####################################################################
def get_likely_interactors (M):
    # target_likelihood  = source X, target y1,y2...yn, size of each y dot = % of sources of degree X targeting that y. Fixed source, % targets
    # interaction_likelihood = the number of edges X to Y as a percentage of the total number of edges over the whole network, in log2
    interaction_likelihood = {}
    target_likelihood  = {}
    interaction_likelihood_normalizer = float(len(M.edges())) # colours reflect interaction likelihood relative to the whole networks' edges
    # target_likelihood_normalizer = different for each source; it's equal to number of interactions originating from a source of degree X
    all_degrees = sorted(list(set(M.degree().values())))
    binary_interactions_count = {}
    for e in M.in_edges_iter():
        source_deg = M.degree(e[0])
        target_deg = M.degree(e[1])
        if (source_deg,target_deg) in binary_interactions_count.keys():
            binary_interactions_count[(source_deg,target_deg)] +=1
        else:
            binary_interactions_count[(source_deg,target_deg)]  =1
    for source, target in binary_interactions_count.keys():
        interaction_likelihood[(source, target)] = (binary_interactions_count[(source, target)]/interaction_likelihood_normalizer)*100
    
    for X in all_degrees:
        size_normalizer=0.0
        sources_of_degree_X = [key for key in binary_interactions_count.keys() if key[0]==X]
        for key in sources_of_degree_X:
            size_normalizer+= binary_interactions_count[key]#float(sum(binary_interactions_count[X,target[1]] for target in sources_of_degree_X))
        #print ('size_normalizer: '+str(size_normalizer))
        for tup in sources_of_degree_X:
            target_likelihood[(tup[0],tup[1])] = (float(binary_interactions_count[(tup[0],tup[1])])/size_normalizer)*100
        #print ('target_likelihood: '+str(target_likelihood))

    '''
    print("="*100+'\n'+'='*100)
    for source in sorted(all_degrees):
        for target in sorted(all_degrees):
            if (source,target) in binary_interactions_count.keys():
                #print (str(source).ljust(10,' ')+str(target).ljust(10,' ')+str(binary_interactions_count[(source,target)] ).ljust(10,' ')+str(target_likelihood[(source,target)] ).ljust(30,' ')+str(interaction_likelihood[(source,target)] ).ljust(10,' '))
                print (str(source)+'    '+str(target)+'    '+str(binary_interactions_count[(source,target)] )+'    '+str(target_likelihood[(source,target)] )+'\t'+str(interaction_likelihood[(source,target)] )+'    ')
   
    print ('all degrees: '+str(all_degrees))
    '''
    return binary_interactions_count, interaction_likelihood, target_likelihood
####################################################################
def get_likely_interactors_detailed (M):
    inhibition_likelihood          = {} # relative to total (-) interactions network-wide
    promotion_likelihood           = {} # relative to total (+) interactions network-wide
    inhibition_target_likelihood   = {} # relative to total (-) interactions originating from a given source
    promotional_target_likelihood  = {} # relative to total (+) interactions originating from a given source
    all_degrees = sorted(list(set(M.degree().values())))
    inhibitions_count = {}
    promotions_count  = {}
    for e in M.edges():
        source_deg = M.degree(e[0])
        target_deg = M.degree(e[1])
        sign       = M[e[0]][e[1]]['sign']
        if sign == 1:
            if (source_deg,target_deg) in promotions_count.keys():
                promotions_count[(source_deg,target_deg)] +=1
            else:
                promotions_count[(source_deg,target_deg)]  =1
        elif sign == -1:
            if (source_deg,target_deg) in inhibitions_count.keys():
                inhibitions_count[(source_deg,target_deg)] +=1
            else:
                inhibitions_count[(source_deg,target_deg)]  =1        
        else:
            print('\nFATAL: I dont recognize this sign\nExiting ..')
            sys.exit(1)
    assert sum(inhibitions_count.values())+sum(promotions_count.values()) == len(M.edges())
    overall_inhibitions_normalizer = float(sum(inhibitions_count.values()))
    overall_promotions_normalizer  = float(sum(promotions_count.values()))
    
    # overall likelihoods
    for source, target in inhibitions_count.keys():
        inhibition_likelihood[(source, target)] = (inhibitions_count[(source, target)]/overall_inhibitions_normalizer)*100
    for source, target in promotions_count.keys():
        promotion_likelihood[(source, target)] = (promotions_count[(source, target)]/overall_promotions_normalizer)*100
    # fixed-source likelihoods
    for X in all_degrees:
        sources_of_degree_X = [key for key in inhibitions_count.keys() if key[0]==X]
        normalizer          = float(sum([inhibitions_count[key] for key in sources_of_degree_X]))
        for interaction in sources_of_degree_X:
            inhibition_target_likelihood[interaction] = (inhibitions_count[interaction]/normalizer)*100
    for X in all_degrees:
        sources_of_degree_X = [key for key in promotions_count.keys() if key[0]==X]
        normalizer          = float(sum([promotions_count[key] for key in sources_of_degree_X]))
        for interaction in sources_of_degree_X:
            promotional_target_likelihood[interaction] = (promotions_count[interaction]/normalizer)*100        
        
    print (str(len(inhibition_likelihood.keys())))
    print (str(len(promotion_likelihood.keys())))
    print (str(len(inhibition_target_likelihood.keys())))
    print (str(len(promotional_target_likelihood.keys())))
    return inhibition_likelihood, promotion_likelihood, inhibition_target_likelihood, promotional_target_likelihood
####################################################################
def getCOORDs (fig_inch_dims, cols, rows, w2h_ratio=0.5):
    COORDs    = []
    figw_inch = fig_inch_dims[0]
    figh_inch = fig_inch_dims[1]
    ppercent  = .25 # percentage of area to be used for padding 
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
def format_axes(ax, cbar_ax, all_degrees, title):
    ax.set_title(title, fontsize=20)  
    ax.set_xlim([min(all_degrees),max(all_degrees)])
    ax.set_ylim([min(all_degrees),max(all_degrees)])
    ax.set_aspect('equal')
    ax.set_xlabel('source', labelpad=0, fontdict={'size':20, 'rotation':0}) 
    ax.set_ylabel('target', labelpad=0, fontdict={'size':20, 'rotation':90}) 
    ax.tick_params(axis='both', which='major', labelsize=20, pad=0)   
    ax.tick_params(axis='both', which='minor', bottom='off', top='off', left='off', right='off', labelleft='off', labelright='off') 
    ax.tick_params(axis='x',    which='major', bottom='on', top='off', left='off', right='off',  labelleft='off', labelright='off', labelbottom='on', pad=0.0, width=1, length=10) #http://matplotlib.org/devdocs/api/_as_gen/matplotlib.axes.Axes.tick_params.html
    ax.tick_params(axis='y',    which='major', bottom='off', top='off', left='on', right='off',  labelleft='on', labelright='off', pad=0.0, width=1, length=10) #http://matplotlib.org/devdocs/api/_as_gen/matplotlib.axes.Axes.tick_params.html

    cbar_ax.set_aspect(10)
    cbar_ax.set_ylabel('% interactions', labelpad=20, fontdict={'size':20, 'rotation':90}) 
    cbar_ax.tick_params(axis='both', which='major', labelsize=10)   
    cbar_ax.tick_params(axis='both', which='minor', bottom='off', top='off', left='off', right='off', labelleft='off', labelright='off') 
    cbar_ax.tick_params(axis='y',    which='major', bottom='off', top='off', left='off', right='on',  labelleft='off', labelright='on', pad=0.0, width=.2, length=5) #http://matplotlib.org/devdocs/api/_as_gen/matplotlib.axes.Axes.tick_params.html
##################################################################
def heatmap(stat, ax, cbar_ax, title):
    X = sorted(list(set([key[0] for key in stat.keys()])))
    Y = sorted(list(set([key[1] for key in stat.keys()])))
    
    all_degrees = sorted(list(set(X+Y)))
    X, Y = [x for x in all_degrees], [x for x in all_degrees]
    Z = []
    for x in X:
        Z.append([])
        for y in Y:
            if (x,y) in stat.keys():
                Z[-1].append(stat[(x,y)])
            else:
                Z[-1].append(0)

    X, Y      = np.meshgrid(X, Y)
    intensity = np.array(Z)
    ################ pcolormesh option, correct xticks yticks ########################
    
    # TODO: normalize the data so the plot is a bit more smooth, you then need to get the ticks of the colormap and de-normalize them
    
    ax.pcolormesh(X,Y,intensity,cmap='Blues')
    norm = mpl.colors.Normalize(vmin=intensity.min(), vmax=intensity.max()) # http://matplotlib.org/users/colormapnorms.html
    colorbase = mpl.colorbar.ColorbarBase(cbar_ax, cmap=mpl.cm.Blues, norm=norm, orientation='vertical', label='mylabel') #http://matplotlib.org/examples/api/colorbar_only.html
    format_axes (ax, cbar_ax, all_degrees, title)
    #colorbase.locator=ticker.LogLocator(base=2)
    ################ seaborn way option, ** INCORRECT ** xticks yticks #################
    '''
    intensity = np.array(Z)
    cbar_ax.set_ylabel('ylabel', fontdict={'size':20, 'rotation':90}) # http://matplotlib.org/examples/text_labels_and_annotations/text_demo_fontdict.html, http://matplotlib.org/users/text_props.html    
    ax=sns.heatmap(intensity, 
                    cbar=True, 
                    ax=ax, 
                    cmap="Blues", 
                    robust=False,   #NOTE: If robust=True and vmin or vmax are absent, the colormap range is computed with robust quantiles instead of the extreme values. http://seaborn.pydata.org/generated/seaborn.heatmap.html
                    square=True,
                    xticklabels=5,
                    yticklabels=5
                    #cbar_ax=cbar_ax
                  ) #,xticklabels=55, yticklabels=55, linewidths=.5, vmin=1, vmax=max(all_degrees)
    ax.set_xlabel('source')
    ax.set_ylabel('target')
    '''
    #####################################################################################
    #cbar_ax.set_aspect(10)
    #cbar_kws={'shrink':0.6, 'pad':.1, 'aspect':20, 'fraction':.2,'label':'mycbar'} # aspect=width, shrink=height
    
    #ax.set_aspect('equal')
    #ax.spines['top'].set_visible(False)
    #ax.spines['right'].set_visible(False)
    #ax.set_aspect('equal', adjustable='box')
    
    #ax=ax.pcolormesh(X, Y, intensity, cmap='ocean_r', vmin=min(all_degrees), vmax=max(15,1)) #ocean, Blues, terrain
    #cbar=plt.colorbar(ax,shrink=0.6, pad=.1, aspect=20, fraction=.2)
    #cbar.set_label('my cbar')
    
    #plt.colorbar(ax,shrink=0.6, pad=.1, aspect=20, fraction=.2)
    # http://seaborn.pydata.org/generated/seaborn.heatmap.html
    #cbar = fig.colorbar(ax, shrink=0.6, pad=.1, aspect=20, fraction=.2) 
    #cbar.outline.set_visible(False)
    #cbar.set_label('my cbar')
    #ax.set_title('plot name')  
    return True
##################################################################
def plotter(over_all_minus, overall_plus, per_source_minus, per_source_plus, titles, log, fig, coords, pos): 
    for stat,title in zip([over_all_minus, overall_plus, per_source_minus, per_source_plus],titles):
        print('\theatmap\t'+str(pos+1))
        ax               = fig.add_axes(coords[pos])
        coords[pos+1][2] = .07*coords[pos+1][2] #shrink the cbar width
        coords[pos+1][3] = .7*coords[pos+1][3] #shrink the cbar height
        coords[pos+1][1] += .25*coords[pos+1][3] # center it relative to the heat map, left it up by the same amount you shrank the height
        cbar_ax          = fig.add_axes(coords[pos+1])
        sc               = heatmap(stat, ax, cbar_ax, title)
        pos             +=2
##################################################################
def dump(data,i):
    with open ('data'+str(i)+'.dump','wb') as f:
        pickle.dump(data,f)
##################################################################
if __name__ == "__main__":
    update_rcParams()
    titles, network_files, output_file_name = setup()
    fig_inch_dims = ((13*len(network_files), 13*len(network_files)))
    fig = plt.figure(figsize=fig_inch_dims)
    num_plots = len(network_files)*4*2 # 4 stats, 2 axes each (1 plot, 1 colorbar)
    cols = 4 # when u change this, font sizes get screwed up out of proportion, 
    rows = int(math.ceil(num_plots/float(cols)))
    assert (rows*cols)==len(network_files)*8
    w2h_ratio=0.5
    coords = getCOORDs (fig_inch_dims, cols, rows, w2h_ratio)
    i=1
    pos = 0
    for f,title, log in zip(network_files, titles, [True]*len(network_files)):
        print('network '+str(i))
        #M = init.load_network ({'network_file':f, 'biased':False})
        #inhibition_likelihood, promotion_likelihood, inhibition_target_likelihood, promotional_target_likelihood = get_likely_interactors_detailed(M)
        #dump([inhibition_likelihood, promotion_likelihood, inhibition_target_likelihood, promotional_target_likelihood],i)
        inhibition_likelihood, promotion_likelihood, inhibition_target_likelihood, promotional_target_likelihood=None,None,None,None
        with open ('data'+str(i)+'.dump','rb') as f:
            inhibition_likelihood, promotion_likelihood, inhibition_target_likelihood, promotional_target_likelihood = pickle.load(f)
        plotter(inhibition_likelihood, promotion_likelihood, inhibition_target_likelihood, promotional_target_likelihood, ['inhibition_likelihood', 'promotion_likelihood', 'inhibition_target_likelihood', 'promotional_target_likelihood'], log, fig, coords, pos) 
        i+=1
        pos+=4*2 # 4 because there are 4 stats per network, *2 cos of colorbars
    print('saving ..')
    save_figure(output_file_name)
    
    