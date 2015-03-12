#!/usr/bin/env python
'''
Tools for making nice plots
Uses matplotlib backend (currently wx or gtk) to provide tools for editing 
matplotlib plots after they have been created
NOTE: I have imported all of pyplot into this module, so you may call it
as though you were calling pyplot directly.  The difference is that with
some of the functions, such as plot, a window will be brought up allowing
you to toggle the visibility of the artists
'''



import matplotlib
if __name__ != '__main__':
    from matplotlib.pyplot import *


def plot( *args, **kwargs):
    '''
    Works the same as matplotlib.pyplot.plot, with the addition of a panel
    being created which allows the user to toggle visibility of 
    the artists in the axis
    '''
    matplotlib.pyplot.plot( *args, **kwargs )
    create_plot_browser( matplotlib.pyplot.gca() )
# end plot

def scatter( *args, **kwargs):
    '''
    Works the same as matplotlib.pyplot.scatter, with the addition of a panel
    being created which allows the user to toggle visibility of 
    the artists in the axis
    '''
    matplotlib.pyplot.scatter( *args, **kwargs )
    create_plot_browser( matplotlib.pyplot.gca() )
# end scatter

    

def create_plot_browser( ax ):
    '''Creates a window for modifying how artists are displayed in an axis'''

    # Call browser creation code appropriate to the current backend
    backend = matplotlib.get_backend().lower()
    if backend == 'wxagg':
        import plotting_tools_wx
        plotting_tools_wx.create_plot_browser( ax )
    elif backend == 'gtkagg':
        import plotting_tools_gtk
        plotting_tools_gtk.create_plot_browser( ax )
# end create_plot_browser


if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser('Test plotting_tools module')
    parser.add_argument('backend', help='Backend to use with matplotlib. Currently supports wxagg and gtkagg')
    
    args = parser.parse_args()
    matplotlib.use( args.backend )
    import matplotlib.pyplot

    fig = matplotlib.pyplot.figure()
    ax = fig.add_subplot(111)
    ax.plot( [1,2,3] )
    ax.scatter( [1,2,3], [3,2,1], color='g')
    ax.plot( [2, 2, 1], 'r' )
    fig.show()

    create_plot_browser( ax )
    
    matplotlib.pyplot.show()

