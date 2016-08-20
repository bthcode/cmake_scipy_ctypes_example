'''
Tools for making nice plots
'''
import matplotlib
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt

import numpy as np

class SlicePlotter:
    def __init__(self, buf, title="Slice Plot"):
        self.title               = title
        self.buf                 = buf
        self.figure              = plt.figure()
        gs                       = gridspec.GridSpec(3,3)
        self.image_ax            = self.figure.add_subplot(gs[1:,:2])
        self.colorbar_ax         = self.figure.add_subplot(gs[0,2])
        self.vertical_slice_ax   = self.figure.add_subplot(gs[1:, 2], sharey = self.image_ax )
        self.horizontal_slice_ax = self.figure.add_subplot(gs[0, :2], sharex = self.image_ax)
        img = self.image_ax.imshow( self.buf, aspect='auto', origin='bottom' )

        # initialize slice plots to img middle
        self.plot_slice(self.buf.shape[0]/2, self.buf.shape[1]/2)

        # set up button press callback
        self.figure.canvas.mpl_connect('button_press_event', self.on_canvas_click)
        #self.figure.canvas.mpl_connect('key_press_event', self.on_keypress)

        self.figure.colorbar( img, cax = self.colorbar_ax )
        self.figure.show()
    # end __init__

    def on_canvas_click(self, event):
        '''Plots the data for the frame number clicked on'''
        # Don't do anything if we are not in an axis or a toolbar button is selected
        if event.xdata == None or event.ydata == None or\
           event.inaxes != self.image_ax or event.inaxes.get_navigate_mode() != None:
            return
        else:
            self.col_number = int(event.xdata)
            self.row_number = int(event.ydata)
            self.plot_slice(self.row_number , self.col_number)
    # end on_canvas_click

    def plot_slice(self, row, column):
        '''Plots a slice of data for the given frame number'''
        xlims = self.image_ax.get_xlim()
        ylims = self.image_ax.get_ylim()

        column_data        = self.buf[:, column]
        horizontal_data    = self.buf[row , :]

        # Plot the horizontal slice
        self.horizontal_slice_ax.clear()
        self.horizontal_slice_ax.plot( np.arange(len(horizontal_data)), horizontal_data, 'r' )
        
        # Plot column slice
        self.vertical_slice_ax.clear()
        self.vertical_slice_ax.plot(column_data, np.arange(len(column_data)), 'r')
        
        # Plot vertical and horizontal markers on the image axis (removing the old ones)
        self.image_ax.patches = []
        self.image_ax.axvspan(column - 0.5, column + 0.5, color='k', alpha=0.3)
        self.image_ax.axhspan(row - 0.5,  row + 0.5,  color='k', alpha=0.3)
        self.image_ax.set_xlim(xlims)
        self.image_ax.set_ylim(ylims)

        self.horizontal_slice_ax.grid(True)
        self.vertical_slice_ax.grid(True)
        self.figure.suptitle(self.title + ": {0}, {1}".format(row, column))
        self.figure.canvas.draw()
    # end plot_slice
# end class Splotter


if __name__=="__main__":
    #data = np.arange(24*36).reshape(24,36)
    data = np.zeros((512,1024))
    for i in range(512):
        data[i,:] = i* np.sin((np.arange(1024)+i)*0.1)
    SP = SlicePlotter(data, title="Example Slice Plotter" )
    plt.show()
