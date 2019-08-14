import matplotlib.pyplot as plt
#mpl.use('Agg')
import networkx as nx, os, sys, math, numpy as np, random
from matplotlib.pyplot import cm 
import matplotlib.patches as mpatches
import matplotlib.collections as collections
from matplotlib import rcParams
import matplotlib.font_manager as font_manager
from myast import *
sys.path.insert(0, os.getenv('lib'))
import utilv4 as util, init
###################################################################################################################
def update_rcParams():
    rcParams['savefig.pad_inches'] = .2

    rcParams['axes.grid']          = True
    rcParams['axes.titlesize']     = 36
    rcParams['axes.labelsize']     = 22

    font_path = os.getenv('HOME')+'/.fonts/adobe/Adobe_Caslon_Pro_Regular.ttf'
    prop = font_manager.FontProperties(fname=font_path)
    rcParams['font.family'] = prop.get_name()

    #rcParams['font.family']        = 'Adobe Caslon Pro'  # cursive, http://matplotlib.org/examples/pylab_examples/fonts_demo.html
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
    rcParams['axes.grid.which']    =  'both'


    rcParams['xtick.color']        =  'black'    #  ax.tick_params(axis='x', colors='red'). This will set both the tick and ticklabel to this color. To change labels' color, use: for t in ax.xaxis.get_ticklabels(): t.set_color('red')
    rcParams['xtick.direction']    =  'out'      # ax.get_yaxis().set_tick_params(which='both', direction='out')
    rcParams['xtick.labelsize']    =  16
    rcParams['xtick.major.pad']    =  1.0
    rcParams['xtick.major.size']   =  10.0      # how long the tick is
    rcParams['xtick.major.width']  =  1.0
    rcParams['xtick.minor.pad']    =  1.0
    rcParams['xtick.minor.size']   =  5.0
    rcParams['xtick.minor.width']  =  1
    rcParams['xtick.minor.visible']=  False


    rcParams['ytick.color']        =  'black'       # ax.tick_params(axis='x', colors='red')
    rcParams['ytick.direction']    =  'out'         # ax.get_xaxis().set_tick_params(which='both', direction='out')
    rcParams['ytick.labelsize']    =  16
    rcParams['ytick.major.pad']    =  4.0
    rcParams['ytick.major.size']   =  10.0
    rcParams['ytick.major.width']  =  1.0
    rcParams['ytick.minor.pad']    =  4.0
    rcParams['ytick.minor.size']   =  5
    rcParams['ytick.minor.width']  =  1
    rcParams['ytick.minor.visible']=  True


    rcParams['legend.borderaxespad']   =  0.5
    rcParams['legend.borderpad']       =  0.4
    rcParams['legend.columnspacing']   =  2.0
    rcParams['legend.edgecolor']       =  'inherit'
    rcParams['legend.facecolor']       =  'white'#'inherit'
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
###################################################################################################################
def slash(path):
    return path+(path[-1] != '/')*'/'
###################################################################################################################
def flip():
    return random.SystemRandom().choice([1,-1])
###################################################################################################################
def getCommandLineArgs():
    if len(sys.argv) < 2:
        print ("Usage: python3 in_pairs_scaling.py [/absolute/path/to/network/file.txt]\nExiting..\n")
        sys.exit()
    clean_lines = util.cleanPaths(sys.argv[1])
    TITLES = [L.split()[0].strip() for L in clean_lines]
    NETS   = [L.split()[1].strip() for L in clean_lines]
    return TITLES, NETS
###################################################################################################################
def load_network (network_edge_file):
    edges_file = open (network_edge_file,'r') #note: with nx.Graph (undirected), there are 2951  edges, with nx.DiGraph (directed), there are 3272 edges
    M=nx.DiGraph()
    next(edges_file) #ignore the first line
    for e in edges_file:
        interaction = e.split()
        assert len(interaction)>=2
        source, target = str(interaction[0]), str(interaction[1])
        if (len(interaction) >2):
            if (str(interaction[2]) == '+'):
                Ijk=1
            elif  (str(interaction[2]) == '-'):
                Ijk=-1
            else:
                print ("Error: bad interaction sign in file "+network_edge_file+"\nExiting...")
                sys.exit()
        else:
            Ijk=flip()
        M.add_edge(source, target, sign=Ijk)
    return M
###################################################################################################################
def scale0 (d=None, N=None, maxd=None, mind=None, a=None, b=None, meand=None, std=None, alpha=None):
    # http://stackoverflow.com/questions/5294955/how-to-scale-down-a-range-of-numbers-with-a-known-min-and-max-value
    # mapping data in interval [mind, maxd] into interval [a,b]
    #        (b-a)(x - min)
    # f(x) = --------------  + a            <<< raise all this to power alpha to dodge the linearity
    #          max - min
    if d==None:
        return py2tex('((b-a)*(d-mind))/(maxd-mind)')
    else:
        if d < meand:
            return 0
        numerator   = (b-a)*(d-mind)
        denumenator = maxd-mind
        return  numerator/denumenator
###################################################################################################################
def scale1 (d=None, N=None, maxd=None, mind=None, a=None, b=None, meand=None, std=None, alpha=None):
    # http://stackoverflow.com/questions/5294955/how-to-scale-down-a-range-of-numbers-with-a-known-min-and-max-value
    # mapping data in interval [mind, maxd] into interval [a,b]
    #        (b-a)(x - min)
    # f(x) = --------------  + a            <<< raise all this to power alpha to dodge the linearity
    #          max - min
    if d==None:
        return py2tex('((0.5*((d-mind)**2)/N))**\u03B1')
    if d < meand:
        return 0
    numerator   = (b-a)*math.pow((d-mind), 2)
    denumenator = N
    return  math.pow((float(numerator)/float(denumenator)) +a,alpha)
###################################################################################################################
def scale2 (d=None, N=None, maxd=None, mind=None, a=None, b=None, meand=None, std=None, alpha=None):
    if d==None:
        return py2tex('(((d-\u03BC)**2)/N)**\u03B1')
    if d <= meand:
        return 0
    numerator   = (b-a)*math.pow((d-meand),2)
    denumenator = N*b
    return  math.pow((float(numerator)/float(denumenator)) +a,alpha)
###################################################################################################################
def scale3 (d=None, N=None, maxd=None, mind=None, a=None, b=None, meand=None, std=None, alpha=None):
    if d==None:
        return py2tex('(((d-\u03BC)**2)/N)**((1/log(d,2))**\u03B1)')
    if d <= meand:
        return 0
    numerator   = (b-a)*math.pow((d-meand),2)
    denumenator = N/2
    return  math.pow((float(numerator)/float(denumenator)) +a, (1/math.log(d,2))**alpha) 
###################################################################################################################
def scale4 (d=None, N=None, maxd=None, mind=None, a=None, b=None, meand=None, std=None, alpha=None):
    if d==None:
        return py2tex('(((d-\u03BC)**2)/N)**(1/(log(d**2,2))**\u03B1)')
    if d <= meand:
        return 0
    numerator   = (b-a)*math.pow((d-meand),2)
    denumenator = N
    return  math.pow((float(numerator)/float(denumenator)) +a, (1/math.log(d**2,2))**alpha) 
###################################################################################################################
def format_ax (ax, xlabel, ylabel):
    ax.set_ylim([-.1, 1])   
    ax.set_xlim([0, 60])   
    ax.grid(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    #ax.set_aspect('equal', adjustable='box')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    #ax.set_aspect('equal', adjustable='box')
    ax.tick_params(axis='x', which='both', left='off', right='off', bottom='on', top='off',  labelbottom='on', labeltop='off') # both major and minor ticks
    ax.tick_params(axis='y', which='both', bottom='off', top='off', left='on', right='off',  labelleft='on', labelright='off') # both major and minor ticks             
    #ax.set_xticks(range(lolim, hilim, 1))
    #ax.set_yscale('log')
    #ax.set_xscale('log')
    ax.set_xlabel (xlabel)
    ax.set_ylabel (ylabel)
    
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
###################################################################################################################
def update_patch(patch_colors,patch_labels,ALPHAS,j,c,k,alpha,THE_alpha,method=1):
    if method == 1: #default, show periodic alphas, maximum 15
        if len(ALPHAS)<15:
            if len (patch_colors)==j:
                patch_colors.append([])                
            patch_colors[j].append(c)# = list(c)
            patch_labels.append('$\\quad\\alpha = '+str(alpha)+'$')                
        elif math.log(k,2)==int(math.log(k,2)) or str(alpha) == str(max(ALPHAS)) or str(alpha) == str(THE_alpha):
            if len (patch_colors)==j:
                patch_colors.append([])                
            patch_colors[j].append(c)# = list(c)
            patch_labels.append('$\\quad\\alpha = '+str(alpha)+'$')
    else: # show min,max, and THE_alpha only
        if len (patch_colors)==j:
            patch_colors.append([])  
        if str(alpha) == str(THE_alpha) or str(alpha) == str(min(ALPHAS)) or str(alpha) == str(max(ALPHAS)):
            patch_colors[j].append(c)# = list(c)
            patch_labels.append('$\\quad\\alpha = '+str(alpha)+'$') 
###################################################################################################################
def get_colors():
    return [iter(cm.GnBu(np.linspace(0,1,len(ALPHAS[scale])+skip))), \
                   iter(cm.YlOrBr(np.linspace(0,1,len(ALPHAS[scale])+skip))),\
                   iter(cm.YlGn(np.linspace(0,1,len(ALPHAS[scale])+skip))),\
                   iter(cm.Spectral(np.linspace(0,1,len(ALPHAS[scale])+skip))), ] #http://matplotlib.org/users/colormaps.html 
###################################################################################################################
###################################################################################################################
if __name__ == "__main__":
    
    update_rcParams()
    #----------------------------------------------------------------------------------------------
    scale     = scale2
    THE_alpha = 0.2 # this alpha will be plotted distinctly from the others
    #----------------------------------------------------------------------------------------------  
    formula = '$score(d)='+scale()+'$'
    formula_xy = [0,0.9] # use maxd to infer an appropriate position of this formula
    ALPHAS = {scale0:np.arange(1,3,.5), scale1:np.arange(.2,.3,.05), scale2:np.arange(.1,.31,.01), scale3:np.arange(1.6,2,.01), scale4:np.arange(.8,1.5,.1)}
    #scale1 winner 0.25
    #scale2 winner 0.21
    #scale3 winner 1.83
    #
    #----------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------   
    fig = plt.figure()
    # we are going to map the set of all degrees [mind, maxd] into the interval [0,1]
    TITLES, NETS = getCommandLineArgs()
    if len(NETS)>4:
        print("I can only handle 4 NETS at a time, if you need more add more colors to variable 'colors'\nExiting ..")
        sys.exit(1)    
    skip        = 5  
    #Spectral, PuBu
    colors      = get_colors()   
    legend_size   =  int(math.log(len(ALPHAS[scale]), 2))
    print ("legend_size".ljust(30,' ')+str(legend_size)+"\nlen ALPHAS[scale]".ljust(30,' ')+str(len(ALPHAS[scale])))
    patch_entries, patch_colors, patch_labels, network_names = [], [], [], []

    j, xlim = 0, 0
    for title, network_file in zip(TITLES,NETS):
        patch_colors.append([])
        network_file      = network_file.strip().replace('\n','')
        #network_names.append('$'+(network_file.split("/")[-1].split('.')[0]).replace('_','\_')+'$')
        network_names.append(title)#('$'+title+'$')
        
        color             = colors[j]        
        for i in range(skip): #increase skip value to start off with more solid color (but decrease it if len(ALPHAS) is large)
            next(color)          
        #M                 = load_network (network_file)
        M                 = init.load_network ({'network_file':network_file, 'biased':False}, undirected=False,quite=True)
        original_degs     = [d for d in M.degree().values()] 
        set_original_degs = sorted(list(set(original_degs)))
        deg_counts        = [original_degs.count(d) for d in set_original_degs]
        avg_frequency     = np.average(deg_counts)
        std               = np.std(original_degs)
        meand             = math.ceil(np.average(original_degs))
        mind              = min(set_original_degs)#min(deg_counts)#min(set_original_degs)
        maxd              = max(set_original_degs)
        N                 = M.number_of_nodes()
        a, b              = 0, 0.5
        xlim              = max(xlim, max(set_original_degs))
        formula_xy[0]     = max(formula_xy[0], maxd/3)
        degrees           = [d for d in M.degree().values()]
        assert math.ceil(float(sum(degrees))/N) == meand        
        print("mean_all "+str(np.average(original_degs))+"\nmean_set "+str(np.average(set_original_degs))+"\nstd all "+str(np.std(original_degs))+"\nstd set "+str(np.std(set_original_degs))+'\n')      
        k=2
        maximum_harvest=[0,0]
        for alpha in ALPHAS[scale]:       
            c, marker,linewidth =next(color), '', 2.5
            if str(alpha) == str(THE_alpha):
                marker,linewidth ='o', 0
            
            scaled_degs=[scale(d, N, maxd, mind, a, b, meand, std, alpha) for d in set_original_degs]
            effective_harvest = [a*b*c for a,b,c in zip(scaled_degs,deg_counts,set_original_degs)]        
            
            sc=plt.plot(set_original_degs, scaled_degs, c=c, linewidth=linewidth, marker=marker,markeredgecolor='none',alpha=.6)                 
            update_patch(patch_colors,patch_labels,ALPHAS[scale],j,c,k,alpha,THE_alpha, method=2)
            print ("original degs(set):".ljust(37,' ')+" ".join([str(round(x,1)).rjust(4,' ') for x in set_original_degs]))
            print ("original count:".ljust(37,' ')+" ".join([str(round(x,1)).rjust(4,' ') for x in deg_counts]))
            print ("scaled degs(set), alpha ".ljust(27,' ')+(str(round(alpha,3))+":").ljust(10,' ')+" ".join([str(round(x,1)).rjust(4,' ') for x in sorted(scaled_degs)]))
            print ("scaled*count, sum ".ljust(27,' ')+ str(round(sum(effective_harvest),1)).ljust(10,' ')+" ".join([str(round(x,1)).rjust(4,' ') for x in effective_harvest]))
            print("")
            if sum(effective_harvest) > maximum_harvest[0]:
                maximum_harvest[0], maximum_harvest[1] = sum(effective_harvest), alpha
            k+=1

        #taken from plot_inverse.py
        print("")
        print ("maximum harvest "+str(maximum_harvest[0])+" at alpha "+str(maximum_harvest[1])) 
        print("")
        j += 1
    
    ax = plt.gca()
    format_ax (ax,"Degree","Conservatinon score") 
    plt.plot(range(xlim+1), [0.5]*(xlim+1), linewidth=3, c='grey', linestyle='-')
    #plt.plot(range(xlim), [0.25]*xlim, linewidth=2, c='grey', linestyle='-')
     
    network_patch=[]
    if len(network_names)>1:
        for row in patch_colors: 
            network_patch.append(collections.CircleCollection([800]*len(row), facecolor = row, edgecolor='none'))
    else: #single network, no need to show color circles
        network_patch.append(collections.CircleCollection([800], facecolor = 'none', edgecolor='none'))
     
    #---------------------------------------------------
    patch_colors = [x for x in zip(*patch_colors)]
    #---------------------------------------------------
    k=0
    for row in patch_colors:           
        patch_entries.append(collections.CircleCollection([200]*len(row), facecolor = row, edgecolor='none'))
        k+=1
    
    L1 = plt.legend(patch_entries, patch_labels, frameon=False, loc=(0.05, 0.75),                       scatterpoints=len(NETS),  scatteryoffsets=[0.18],        handlelength=3, fontsize=16, handleheight=1.3) 
    plt.gca().add_artist(L1)
    L2 = plt.legend(network_patch, network_names, frameon=False, loc=(0.6, 0.05*len(network_names)),  scatterpoints=legend_size, scatteryoffsets=[0.16], handlelength=1.5, fontsize=30, handleheight=len(network_names)*1.4)  
    plt.gca().add_artist(L2) 
    
    #plt.annotate(formula, xy=(.2, .2), xytext=(.2, .2), arrowprops=dict(facecolor='black', shrink=0.05),)
    plt.annotate(formula, xy=formula_xy, xytext=formula_xy, fontsize=30)
    plt.yticks([0,.25, .5], ['0','0.25','0.5'])
    
        
    plot_dir = slash(slash(os.getcwd())+'plots')
    if not os.path.isdir(plot_dir):
        os.mkdir(plot_dir)

    file_name = '_'.join(TITLES)
    plt.savefig(plot_dir+file_name+".png", dpi=500,bbox_inches="tight") # http://matplotlib.org/api/figure_api.html#matplotlib.figure.Figure.savefig
    print ("plotted: "+plot_dir+file_name+".png")  
    plt.show()  
