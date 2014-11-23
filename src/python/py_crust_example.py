'''
Demonstrates how to get a python shell in a wx app
'''

import wx
from wx.py.crust import Shell




if __name__ == '__main__':
    app = wx.App(0)
    parent_frame  =  wx.Frame( None, title = 'Test Frame' )
    pycrust_frame = wx.Frame( parent_frame, title='Type app to access variables' )

    app.shell = Shell(pycrust_frame) 
    app.shell.interp.locals['pcapp'] = app 
        
    # Prevent the py crust frame from being closed
    def onClose( event ): pycrust_frame.Show(False)
    wx.EVT_CLOSE(pycrust_frame, onClose) 

    # Import things we might need into the shell
    app.shell.run( 'import matplotlib' ) 
    app.shell.run( 'matplotlib.interactive(True)' ) 
    app.shell.run( 'from matplotlib import pyplot as plt' ) 
    app.shell.run( 'import numpy as np' ) 
    app.shell.run( 'from mpl_toolkits.mplot3d import axes3d' )
        
        
    # Add a menu option to the parent frame to show the py crust frame
    menubar = wx.MenuBar()
    filemenu = wx.Menu()
    show_shell_id = wx.NewId()
    filemenu.Append(show_shell_id, 'Show Shell')
    parent_frame.Bind( wx.EVT_MENU, lambda event: pycrust_frame.Show(True) )
    menubar.Append( filemenu, '&File' )
    parent_frame.SetMenuBar( menubar )
    
    
    parent_frame.Show(True)
    pycrust_frame.Show(False)
    app.MainLoop()
  
