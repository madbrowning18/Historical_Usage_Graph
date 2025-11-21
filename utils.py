import numpy as np
import networkx as nx

def hierarchy_pos(G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):

    '''
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723
    Licensed under Creative Commons Attribution-Share Alike 
    
    If the graph is a tree this will return the positions to plot this in a 
    hierarchical layout.
    
    G: the graph (must be a tree)
    
    root: the root node of current branch 
    - if the tree is directed and this is not given, 
      the root will be found and used
    - if the tree is directed and this is given, then 
      the positions will be just for the descendants of this node.
    - if the tree is undirected and not given, 
      then a random choice will be used.
    
    width: horizontal space allocated for this branch - avoids overlap with other branches
    
    vert_gap: gap between levels of hierarchy
    
    vert_loc: vertical location of root
    
    xcenter: horizontal location of root
    '''
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))  #allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
        '''
        see hierarchy_pos docstring for most arguments

        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed

        '''
    
        if pos is None:
            pos = {root:(xcenter,vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)  
        if len(children)!=0:
            dx = width/len(children) 
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G,child, width = dx, vert_gap = vert_gap, 
                                    vert_loc = vert_loc-vert_gap, xcenter=nextx,
                                    pos=pos, parent = root)
        return pos

            
    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)


import plotly
import plotly.express as px
import pandas as pd
from plotly.graph_objs import Bar, Scatter, Figure, Layout, Table
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
plotly.offline.init_notebook_mode(connected=True)
pd.options.plotting.backend = "plotly"

import plotly.io as pio
pio.renderers.default = "iframe"

def plot_time(df, date_col="date", breaks="D", title="Document Activity Over Time"):
    """
    Plot a resampled count of activity.
    Supports custom date column name and custom title.
    """
    df.index = df[date_col]
    df2 = df[date_col].resample(breaks).count().rename('count').reset_index()

    fig = px.line(
        df2,
        x=date_col,
        y="count",
        template='plotly_dark',
        title=title
    )
    fig.show()



# Define a colormap
def get_color(value):
    # Adjust this function according to your gradient requirements
    if value <= 25:
        return 'green'
    elif value <= 50:
        return 'yellow'
    elif value <= 75:
        return 'orange'
    else:
        return 'red'

def get_color_from_df(df, node):
    try:
        temp = df[df['Document Location'].str.contains(node, regex = False)]
        if len(temp) > 0:
            return(temp.loc[temp['age'].idxmin(),'color'])
        else:
            return('grey')
    except:
        print(node)
 