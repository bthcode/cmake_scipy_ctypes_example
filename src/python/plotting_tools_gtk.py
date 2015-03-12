import gtk
import matplotlib
matplotlib.use( 'gtkagg' )
from plotting_utils import *

class ArtistTogglePanel( gtk.Window ):
    '''
    Presents a panel for toggling artists (e.g., lines or scatter plots) on and off
    '''

    object_types = [matplotlib.lines.Line2D, matplotlib.collections.PathCollection] 

    def __init__( self, ax, *args, **kwargs ):
        super( ArtistTogglePanel, self ).__init__(*args, **kwargs)
        self.ax = ax

        self.vbox    = gtk.VBox( False, 2 )
        self.table   = gtk.Table(columns=3, homogeneous = False)

        # Make an entry for each plottable in the axis
        self.artists = get_plottables( self.ax, self.object_types )
        self.setup_toggles()
        self.vbox.pack_start( self.table )

        # Now add a refresh button for when more stuff is plotted
        refresh = gtk.Button( 'Refresh' )
        refresh.connect("button_press_event", self._on_refresh )

        self.vbox.pack_start(refresh, False, False, 0)

        self.add( self.vbox )
        self.show_all()
    # end __init__


    def setup_toggles( self ):
        ''' Sets up the controls for each of the artists'''

        # Delete any existing controls
        for child in self.table.get_children():
            self.table.remove( child )


        # Create the title row
        self.table.attach(gtk.Label('Enable'), 0, 1, 0, 1)
        self.table.attach(gtk.Label("Type"), 1, 2, 0, 1)
        self.table.attach(gtk.Label("Color"), 2, 3, 0, 1)

        # Add a row for each artist
        for artist in self.artists:
            self.add_row( artist )

    # end setup_toggles

    def add_row( self, artist ):
        '''
        Adds a row to the GUI for given artist
        '''

        # Resize the table to allow one more row to be added
        cols = self.table.get_property('n-columns')
        rows = 1 + self.table.get_property('n-rows')
        self.table.resize(rows, cols)
 
        # Add a checkbox for toggling visibility,
        # a text box containing the type of the artist,
        # and a label that shows the color of the artist
        box         = gtk.CheckButton( )
        box.set_active( artist.get_visible() )
        box.connect("button_press_event", lambda widget, data: self._on_box_checked(artist) )
 
        artist_type = type(artist)
        type_label  = gtk.Label(artist_type.__name__ )

        color_rgb   = get_color_rgb( artist )
        color_label = gtk.Label()
        event_box   = gtk.EventBox()
        event_box.add( color_label )
        event_box.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(red=color_rgb[0], green=color_rgb[1], blue=color_rgb[2] ) )

        self.table.attach(box,        0, 1, rows-1, rows)
        self.table.attach(type_label, 1, 2, rows-1, rows)
        self.table.attach(event_box,  2, 3, rows-1, rows)
    # end add_row


    def _on_refresh( self, widget, data ):
        ''' Callback for refreshing the list of artists'''
        self.artists = get_plottables( self.ax, self.object_types )
        self.setup_toggles()
        self.show_all()
    # end _on_refresh


    def _on_box_checked(self, artist):
        '''Callback for when a checkbox is toggled'''

        # Hide if visible and show if invisible
        visible = artist.get_visible()
        artist.set_visible(not visible); 
        self.ax.figure.canvas.draw()
    # end _on_box_checked

# end ArtistTogglePanel

def create_plot_browser( ax ):
    ArtistTogglePanel( ax )

# end create_plot_browser


if __name__=='__main__':

    # Create a figure, plot some stuff, and create the plot browser as a unit test
    
    fig = matplotlib.pyplot.figure()
    ax = fig.add_subplot(111)
    ax.plot( [1,2,3] )
    ax.scatter( [1,2,3], [3,2,1], color='g')
    ax.plot( [2, 2, 1], 'r' )
    fig.show()


    create_plot_browser( ax )

    gtk.main()
