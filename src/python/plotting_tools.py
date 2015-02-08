'''
Tools for making nice plots
'''
import matplotlib
matplotlib.use('wxagg')
import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
import matplotlib.gridspec as gridspec
from matplotlib.figure import Figure

import numpy as np

class SlicePlotter( wx.Frame ):
    '''
    Creates a GUI window with a plot of the input matrix.
    Controls are provided for then plotting slices of this matrix on another axis
    Valid kwargs are:
        slice_range  : Defines the x-axis for a slice of the data. Must be the same size as data_matrix.shape[1]
        frame_range  : Defines the frame axis for the data.  Must be the same size as data_matrix.shape[0]
        points       : A two-column array of (frame, vertical_coordinate) pairs for plotting with the data_matrix
        title        : A string specifying the title of the window
    '''
    def __init__(self, data_matrix, parent=None, **kwargs):

        # Pull stuff out of the input arguments, defaulting unspecified arguments using dict.pop
        title            = kwargs.pop('title', 'Slice Plotter')
        self.data_matrix = data_matrix
        self.slice_range = kwargs.pop( 'slice_range', np.arange(self.data_matrix.shape[1]) )
        self.frame_range = kwargs.pop( 'frame_range', np.arange(self.data_matrix.shape[0]) )
        self.data_points = kwargs.pop( 'points', np.zeros( (0,2) ) )
        wx.Frame.__init__( self, parent, title = title )

                        
        # Create the panels, etc
        # Control panel on left with canvas on right
        control_panel = wx.Panel( self )
        plot_panel    = wx.Panel( self )

        self.figure = Figure()
        gs = gridspec.GridSpec(3,3)
        self.colorbar_ax         = self.figure.add_subplot(gs[0,2])
        self.image_ax            = self.figure.add_subplot(gs[1:,:2])
        self.vertical_slice_ax   = self.figure.add_subplot(gs[1:, 2], sharey = self.image_ax )
        self.horizontal_slice_ax = self.figure.add_subplot(gs[0, :2], sharex = self.image_ax)
        
        
        self.canvas = FigureCanvas( plot_panel, wx.ID_ANY, self.figure)
        self.canvas.mpl_connect('button_press_event', self.on_canvas_click )
        self.figure.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, wspace=0.15, hspace=0.15)
        
        # Create a status bar.  This will show the x/y location of the cursor in each plot    
        self.status_bar = wx.StatusBar(self, -1)
        self.status_bar.SetFieldsCount(1)
        self.SetStatusBar(self.status_bar)
        self.canvas.mpl_connect('motion_notify_event', self.on_update_status_bar)
        
        
        self.toolbar = NavigationToolbar2Wx( self.canvas )


        plot_szr = wx.BoxSizer( wx.VERTICAL )
        plot_szr.Add( self.canvas, 1, wx.EXPAND | wx.ALL, 1)
        plot_szr.Add( self.toolbar, 0, wx.ALL, 1 )
        self.toolbar.Realize()
        self.toolbar.update()
        plot_panel.SetSizer( plot_szr )

        # Set up the controls
        szr = wx.BoxSizer(wx.VERTICAL)
        self.frame_box = wx.TextCtrl(control_panel, value = '', style = wx.TE_PROCESS_ENTER)
        self.frame_box.Bind(wx.EVT_TEXT_ENTER, self.on_new_frame)
        szr.Add(self.frame_box, 0, wx.EXPAND)
        
        # Forward/back buttons
        hszr = wx.BoxSizer(wx.HORIZONTAL)
        prev_frame_button =  wx.Button( control_panel, wx.ID_ANY, "<-")
        hszr.Add( prev_frame_button, 0, wx.ALL, 1 )
        prev_frame_button.Bind( wx.EVT_BUTTON, self.on_prev_frame )        
        next_frame_button =  wx.Button( control_panel, wx.ID_ANY, "->" )
        hszr.Add( next_frame_button, 0, wx.ALL, 1 )
        szr.Add(hszr, 0, wx.EXPAND)
        next_frame_button.Bind( wx.EVT_BUTTON, self.on_next_frame )


        # Up/down buttons
        self.freq_box = wx.TextCtrl(control_panel, value = '', style = wx.TE_PROCESS_ENTER)
        self.freq_box.Bind(wx.EVT_TEXT_ENTER, self.on_new_frame)
        szr.Add(self.freq_box, 0, wx.EXPAND)
        hszr = wx.BoxSizer(wx.HORIZONTAL)
        up_button =  wx.Button( control_panel, wx.ID_ANY, "up")
        hszr.Add( up_button, 0, wx.ALL, 1 )
        up_button.Bind( wx.EVT_BUTTON, self.on_go_up )        
        down_button =  wx.Button( control_panel, wx.ID_ANY, "down" )
        hszr.Add( down_button, 0, wx.ALL, 1 )
        szr.Add(hszr, 0, wx.EXPAND)
        down_button.Bind( wx.EVT_BUTTON, self.on_go_down )

        
        control_panel.SetSizer(szr)    
        szr = wx.BoxSizer(wx.HORIZONTAL)
        szr.Add(control_panel, 0, wx.ALL | wx.EXPAND, 1)
        szr.Add(plot_panel, 1, wx.ALL | wx.EXPAND, 1)
        self.SetSizer( szr )

        # Key press stuff so we can go forward/back with the arrow keys        
        self.Bind(wx.EVT_KEY_UP, self.on_keypress)


        # Tie clicking on the figure to the plotting of the data
        self.canvas.mpl_connect('button_press_event', self.on_canvas_click )
        self.frame_number = int(self.frame_range[0])
        self.frame_box.SetValue( str( self.frame_number ) )
        self.freq_number = 0
        self.freq_box.SetValue( str( self.freq_number ) )


        # Plot an image of the data matrix with the points on top
        self.flipped_mat = np.flipud( data_matrix.T )
        img = self.image_ax.imshow( self.flipped_mat, aspect='auto', interpolation='bicubic', \
                               extent = [self.frame_range[0], self.frame_range[-1], self.slice_range[0], self.slice_range[-1]])
        self.figure.colorbar( img, cax = self.colorbar_ax )
        self.image_ax.plot( self.data_points[:,0], self.data_points[:,1], 'ko' )

        # We need the slice_data_points so that we have can plot the data points with
        # the correct height in the slice plot 
        # This is because of the change of scale which the slice_range creates
        self.slice_data_points = self.data_points.copy()
        for idx in range(self.slice_data_points.shape[0]):
            self.slice_data_points[idx,1] = np.argmin( np.abs(self.slice_range - self.slice_data_points[idx,1] ) )


        self.plot_slice( self.frame_number, self.freq_number )
        self.SetSize((800, 800))
        self.Show()
        
    # end __init__    

    def on_update_status_bar(self, event):
        if event.inaxes:
            x,         y = event.xdata, event.ydata
            int_x, int_y = int(x), int(y)
            if event.inaxes == self.image_ax\
                and int_x < self.flipped_mat.shape[1]\
                and int_x >= 0\
                and int_y < self.flipped_mat.shape[0]\
                and int_y >= 0:
                text = 'x={0}, y={1}, z={2}'.format(x, y, self.flipped_mat[int_y, int_x])
            else:
                text = 'x={0}, y={1}'.format(x, y)

            self.status_bar.SetStatusText(text, 0)
    # end on_update_status_bar
            
    def on_new_frame( self, event=None ):
        '''Gets the frame number from the text box and calls the plot function'''
        self.frame_number = int( self.frame_box.GetValue() )
        self.freq_number = int( self.freq_box.GetValue() )
        self.plot_slice( self.frame_number, self.freq_number )
    # end on_new_frame

    def on_prev_frame(self, event):
        self.frame_number = max(self.frame_number-1, self.frame_range[0])
        self.frame_box.SetValue(str(self.frame_number))
        self.on_new_frame()
    # end on_prev_frame

    def on_next_frame(self, event):
        self.frame_number = min(self.frame_number+1, self.frame_range[-1])
        self.frame_box.SetValue(str(self.frame_number))
        self.on_new_frame()
    # end on_next_frame

    def on_go_down(self, event):
        self.freq_number = max(self.freq_number-1, 0)
        self.freq_box.SetValue(str(self.freq_number))
        self.on_new_frame()
    # end on_prev_frame

    def on_go_up(self, event):
        self.freq_number = min(self.freq_number+1, self.data_matrix.shape[1]-1)
        self.freq_box.SetValue(str(self.freq_number))
        self.on_new_frame()
    # end on_next_frame
        

    def plot_slice( self, frame, freq ):
        '''Plots a slice of data for the given frame number'''
        frame_idx         = frame - self.frame_range[0]
        frame_data        = self.data_matrix[frame_idx, :]
        horizontal_data   = self.data_matrix[:, freq]
        mask              = self.data_points[:,0] == frame
        hmask             = self.data_points[:,1] == freq
        inds              = self.slice_data_points[mask, 1].astype(int)
        frame_data_points = self.data_points[mask, 1]
        hinds             = self.slice_data_points[hmask, 1].astype(int)
        freq_data_points  = self.data_points[hmask, 1]
        
        # Plot the frame-slice (removing old data) along with the data points for the current frame
        self.vertical_slice_ax.lines = []
        self.vertical_slice_ax.plot( frame_data, self.slice_range, 'r' )
        self.vertical_slice_ax.plot( frame_data[inds], frame_data_points, 'ko' )

        # Plot the horizontal (freq) slice
        self.horizontal_slice_ax.lines = []
        self.horizontal_slice_ax.plot( self.frame_range, horizontal_data, 'r' )
        self.horizontal_slice_ax.plot( freq_data_points, horizontal_data[hinds], 'ko' )

        
        # Plot vertical and horizontal markers on the image axis (removing the old ones)
        xlims = self.image_ax.get_xlim()
        ylims = self.image_ax.get_ylim()
        self.image_ax.patches = []
        self.image_ax.axvspan( frame - 0.5, frame + 0.5, color='k', alpha=0.3)
        self.image_ax.axhspan( freq - 0.5,  freq + 0.5,  color='k', alpha=0.3)
        self.image_ax.set_xlim( xlims )
        self.image_ax.set_ylim( ylims )

        self.canvas.draw()
    # end plot_slice
    
    
    def on_canvas_click(self, event):
        '''Plots the data for the frame number clicked on'''
        # Don't do anything if we are not in an axis or a toolbar button is selected
        if event.xdata == None or event.ydata == None or\
           event.inaxes != self.image_ax or event.inaxes.get_navigate_mode() != None:
            return
        else:
            self.frame_number = int(event.xdata)
            self.frame_box.SetValue( str( self.frame_number ) )
            self.freq_number = int(event.ydata)
            self.freq_box.SetValue( str( self.freq_number ) )

            self.on_new_frame( event = None )
    # end on_canvas_click


    def on_keypress( self, event ):
        ''' Processes the event triggered by a key being pressed.
        '''
        key = event.GetKeyCode()
        if key == wx.WXK_LEFT:
            if not event.ControlDown() and not event.AltDown():
                self.on_prev_frame( event = None )
        elif key == wx.WXK_RIGHT:
            if not event.ControlDown() and not event.AltDown():
                self.on_next_frame( event = None )
        elif key == wx.WXK_UP:
            if not event.ControlDown() and not event.AltDown():
                self.on_go_up( event = None )
        elif key == wx.WXK_DOWN:
            if not event.ControlDown() and not event.AltDown():
                self.on_go_down( event = None )

# end SlicePlotter



if __name__ == '__main__':
    app = wx.App(0)
    data = np.random.rand( 2000, 512 )
    plotter = SlicePlotter( data, points=np.array([[1,100], [100, 500], [200, 200]]) )
    
    app.MainLoop()
    

    
