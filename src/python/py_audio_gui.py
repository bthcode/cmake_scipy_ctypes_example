#!/usr/bin/env python


import sys
import os
import argparse

import matplotlib
import matplotlib
matplotlib.use('WXAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
import matplotlib.gridspec as gridspec
from matplotlib.widgets import RectangleSelector
import matplotlib.cm as cm

import wx
import wx.lib.newevent

import wavfile
import numpy as np
from collections import OrderedDict

import scipy.signal as ss

import custom_dialogs


SelectAudioEvent, EVT_SELECT_AUDIO = wx.lib.newevent.NewCommandEvent()

class CustomToolbar(NavigationToolbar2Wx):
    ''' Demonstration of a custom toolbar, including interacting with built-in wx toolbar controls '''

    def __init__(self, gui, canvas):
        '''Create the toolbar'''
        NavigationToolbar2Wx.__init__(self, canvas)
        self.gui         = gui
        self.pan_id      = self.wx_ids['Pan']
        self.zoom_id     = self.wx_ids['Zoom']
        self.pan_tool    = self.FindById(self.pan_id)
        self.zoom_tool   = self.FindById(self.zoom_id)
        self.Bind(wx.EVT_TOOL, self._on_toggle_pan_zoom, self.pan_tool)
        self.Bind(wx.EVT_TOOL, self._on_toggle_pan_zoom, self.zoom_tool)
        self.button      = wx.Button( self, label = 'Region Selector' )
        self.button.Bind( wx.EVT_BUTTON, self._on_region_select )
        self.AddControl( self.button )
    # end __init__
    

    def _on_region_select(self, event):
        print "_on_region_select"
        event = SelectAudioEvent(self.GetId())
        self.GetEventHandler().ProcessEvent(event)
    # end _on_region_select


    def _on_toggle_pan_zoom(self, event):
        '''
        Since there are custom pan/zoom buttons, turn off other when one is pressed  
        '''
        event.Skip()
    # end _on_toggle_pan_zoom

# end CustomToolbar



class AudioGui( wx.Frame ):
    ''' Sample GUI showing wx and matplotlib for audio '''
    def __init__( self, parent, wav_file ):
        wx.Frame.__init__( self, parent )
        self.wav_file = wav_file
        self.win_size = 1024
        self.advance  = 512
        self.overlap  = self.win_size - self.advance
        self.display_type = 'samples'
        
        self.cmapnames = cm._cmapnames
        self.cmapidx   = 0
        self.init_gui()
        self.load_audio()
    # end __init__

    def get_specgram( self, samples, win_size, advance, oversample ):
        '''
        Gets spectrum for samples, returns as a matrix
        [in] samples    - audio samples
        [in] win_size   - analysis window size in samples
        [in] advance    - number of samples to advance between frames
        [in] oversample - how much to oversample by
        [ret] matrix    - nframes x fft_len

        Notes: uses a hanning window ( the scipy.signal version so it's periodic )
        ''' 
        num_frames    = samples.shape[0] / advance
        fft_full_len  = win_size * oversample
        fft_half_len  = ( fft_full_len / 2.0 ) + 1
        hh            = ss.hanning( win_size, False )
        spec_buf   = np.zeros( (num_frames, fft_half_len), dtype=np.complex )
        for frame_id in range( num_frames ):
            frame_start   = frame_id * advance
            frame_end     = frame_start + win_size
            if frame_end > samples.shape[0]:
                break
            spectrum      = np.fft.fft( hh * samples[frame_start:frame_end,0], n=fft_full_len )
            spec_buf[ frame_id, : ] = spectrum[ :fft_half_len ]
        return spec_buf
    # end get_specgram

    def load_audio(self):
        self.sample_rate, self.samples = wavfile.read( self.wav_file )

        self.win_size    = int( self.win_combobox.GetValue() )
        self.overlap_pct = float( self.overlap_combobox.GetValue() )
        self.oversample  = int (self.oversample_combobox.GetValue() )
        self.overlap_samples = int( self.win_size * self.overlap_pct ) 
        self.advance         = self.win_size - self.overlap_samples

        self.specgram = self.get_specgram( self.samples, self.win_size, self.advance, self.oversample )
        self.ax.plot( self.samples )
        self.canvas.draw()
    # end load_audio


    def init_gui( self ):
        ''' layout:
        szr
          |--main_panel_sizer
                   |--hsizer
                        |--control_panel
                        |--self.canvas
        +--------------------------------------------+
        | MENU BAR                                   |
        +--------------------------------------------+
        |    |                                       |
        |    |                                       |
        |    |                                       |
        |    |                                       |
        |    |                                       |
        +----+---------------------------------------+
        '''
        main_panel  = wx.Panel( self )

        # 1. Set up a plotting canvas
        self.figure = Figure()
        self.ax     = self.figure.add_subplot(111)
        self.canvas = FigureCanvas( main_panel, wx.ID_ANY, self.figure )
        self.figure.subplots_adjust(left=0.08, right=0.95, bottom=0.08, top=0.92, hspace=.1, wspace=.1)
        self.status_bar = wx.StatusBar(self, -1)
        self.status_bar.SetFieldsCount(1)
        self.SetStatusBar(self.status_bar)
        self.canvas.mpl_connect('motion_notify_event', self.on_update_status_bar)


        # 2. Set up a buttons canvas
        control_panel = wx.Panel( main_panel )
        control_panel.SetMinSize( ( 200, -1 ) )

        # Grid sizer to hold buttons
        control_buttons_sizer = wx.GridSizer( cols = 1 )

        # Sample button1
        button1   = wx.Button( control_panel, label = 'Time/Spectra' )
        button1.Bind( wx.EVT_BUTTON, self._on_button1 )
        control_buttons_sizer.Add( button1 )

        # Color map
        self.combobox2   = wx.ComboBox( control_panel, name='Colormap', choices=self.cmapnames, value='Spectral'  )
        self.combobox2.Bind( wx.EVT_COMBOBOX, self._on_cmap_change )
        control_buttons_sizer.Add( self.combobox2 )

        # win size
        self.win_sizes = [ '256', '512', '1024', '2048', '4096', '8192' ]
        self.win_combobox= wx.ComboBox( control_panel, name='win_size', choices=self.win_sizes, value='1024'  )
        self.win_combobox.Bind( wx.EVT_COMBOBOX, self._on_fft_param_change )
        control_buttons_sizer.Add( self.win_combobox)


        # fft size
        self.oversamples = [ '1', '2', '4', '8', '16' ]
        self.oversample_combobox= wx.ComboBox( control_panel, name='win_size', choices=self.oversamples, value='2'  )
        self.oversample_combobox.Bind( wx.EVT_COMBOBOX, self._on_fft_param_change )
        control_buttons_sizer.Add( self.oversample_combobox)
    
        # window overlap
        self.overlaps = [ '0.25', '0.5', '0.75', '0.95' ]
        self.overlap_combobox= wx.ComboBox( control_panel, name='win_size', choices=self.overlaps, value='0.75'  )
        self.overlap_combobox.Bind( wx.EVT_COMBOBOX, self._on_fft_param_change )
        control_buttons_sizer.Add( self.overlap_combobox)

        # Maxima on/off
        maxima_button   = wx.Button( control_panel, label = 'Show Maxima' )
        maxima_button.Bind( wx.EVT_BUTTON, self._on_maxima_button )
        control_buttons_sizer.Add( maxima_button )
        self.maxima_lines = None


        control_panel.SetSizerAndFit( control_buttons_sizer )

        # 3. Set up custom tool bar
        self.toolbar = CustomToolbar(self, self.canvas)
        self.toolbar.Realize()

        # put it all in sizers
        hsizer = wx.BoxSizer( wx.HORIZONTAL )
        hsizer.Add( control_panel )
        hsizer.Add( self.canvas )

        # --------- MENU BAR ------------------#
        menubar             = wx.MenuBar() 
        filemenu            = wx.Menu()

        # Open Action
        self.ON_MENU_OPEN   = wx.NewId()
        filemenu.Append( self.ON_MENU_OPEN, "&Open", "" )
        self.Bind(wx.EVT_MENU, self._on_open, id=self.ON_MENU_OPEN )

        self.ON_MENU_QUIT   = wx.NewId()
        filemenu.Append( self.ON_MENU_QUIT, "&Quit", "" )
        self.Bind( wx.EVT_MENU, self.on_close, id=self.ON_MENU_QUIT )
        

        menubar.Append( filemenu, "&File" )
        self.SetMenuBar( menubar )
        # --------- END MENU BAR --------------#
        
        # sizer for main panel
        main_panel_sizer = wx.BoxSizer( wx.VERTICAL )
        main_panel_sizer.Add( hsizer, 1, wx.EXPAND )
        main_panel_sizer.Add( self.toolbar, 0, wx.EXPAND )
        main_panel.SetSizer( main_panel_sizer )

        # overall sizer
        szr = wx.BoxSizer( wx.VERTICAL )
        szr.Add( main_panel, 1, wx.EXPAND )
        self.SetSizerAndFit( szr )

        self.Show()
    # end init_gui

    def _on_fft_param_change( self, evt ):
        print self.win_combobox.GetValue()
        print self.overlap_combobox.GetValue()
        print self.oversample_combobox.GetValue()
        self.win_size    = int( self.win_combobox.GetValue() )
        self.overlap_pct = float( self.overlap_combobox.GetValue() )
        self.oversample  = int (self.oversample_combobox.GetValue() )
        self.overlap_samples = int( self.win_size * self.overlap_pct ) 
        self.advance         = self.win_size - self.overlap_samples

        self.specgram = self.get_specgram( self.samples, self.win_size, self.advance, self.oversample )
        if self.display_type == 'samples':
            return
        self.ax.cla()
        self.ax.imshow( 20*np.log10(np.abs(self.specgram).T) , origin='lower', aspect='auto', cmap=self.combobox2.GetValue() )
        self.canvas.draw()        

    # end _on_fft_param_change

    def on_close( self, evt ):
        print "on quit"
        self.Close()
    # end on_close

    def _on_button1( self, evt ):
        print "caught button1"
        self.ax.cla()
        if self.display_type == 'samples':
            self.ax.imshow( 20*np.log10(np.abs(self.specgram).T), origin='lower', aspect='auto', cmap=self.cmapnames[ self.cmapidx ] )
            self.display_type = 'spectra'
        elif self.display_type == 'spectra':
            self.ax.plot( self.samples )
            self.display_type = 'samples'
        self.canvas.draw()        
    # end _on_button1

    def _on_maxima_button( self, evt ):
        print "caught maxima button"

        # if not in spectra moode, bail
        if self.display_type != 'spectra':
            return
        # turn off maxima lines if they exist, then bail
        if self.maxima_lines != None:
            print self.maxima_lines
            self.ax.lines.remove( self.maxima_lines )
            self.canvas.draw()
            self.maxima_lines = None
            return
        # maxima lines must be off and in spectra mode, so:
        #  1. calculate maxima
        #  2. plot them
        #  3. store handle to them in self.maxima_lines
        self.maxima = []
        for frame_idx, row in enumerate( self.specgram ):
            max_idxs = ss.argrelextrema( np.abs(row), np.greater ) 
            for fbin in max_idxs[0]:
                self.maxima.append( [frame_idx, fbin] ) 
        self.maxima = np.array( self.maxima )
        self.maxima_lines, = self.ax.plot( self.maxima[:,0], self.maxima[:,1], 'b.', alpha=0.35 )
        self.canvas.draw()        
    # end _on_button1



    def _on_cmap_change( self, evt ):
        # get zoom level so we can restore it
        zoomx = self.ax.get_xlim()
        zoomy = self.ax.get_ylim()
        if self.display_type == 'spectra':
            self.ax.cla()
            self.ax.imshow( 20*np.log10(np.abs(self.specgram).T), origin='lower', aspect='auto', cmap=self.combobox2.GetValue() )
            # restore zoom level
            self.ax.set_xlim( zoomx )
            self.ax.set_ylim( zoomy )
            self.canvas.draw()        
    # end change_colors


    def on_update_status_bar(self, event):
        if event.inaxes:
            x, y = event.xdata, event.ydata
            text = 'x = ' + str(x) + '  y = ' + str(y)
            self.status_bar.SetStatusText(text, 0)
    # end on_update_status_bar                      

    def _on_open( self, event ):
        print "_on_open"
    # end _on_open

# end class AudioGui

if __name__=="__main__":
    print "------------ EXAMPLE PYTHON AUDIO GUI ---------------"

    ############ CMD LINE PARSING ############
    parser   = argparse.ArgumentParser( 'EXAMPLE PYTHON AUDIO GUI' )
    parser.add_argument( 'wav_file' )
    args     = parser.parse_args()
    wav_file = args.wav_file 

    ############ GUI ###############
    app = wx.App(0)
    AG = AudioGui( None, wav_file )
    app.MainLoop()
