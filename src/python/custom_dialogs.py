#!/usr/bin/env python
import wx

class ParamDialog( wx.Dialog ):
    '''
    Presents parameters to be edited by the user
    '''
    
    def __init__( self, *args, **kwargs ):
        '''Create the dialog'''
        super( ParamDialog, self).__init__(*args, **kwargs)
        self.panel = wx.Panel( self )
    # end __init__
    
    def InitUI( self, param_dict ):
        '''Create a GUI option for each item in the param dict'''

        # Keep track of the data type for each param value so we can return
        # the same data types when the params are updated
        self.param_dict = param_dict
        self.param_dtypes = {}
        for key, value in self.param_dict.items():
            self.param_dtypes[ key ] = type( value )
        
        # Keep track of the text boxes for entering params with a dictionary
        self.param_boxes = {}
        self.sizer = wx.FlexGridSizer( cols = 2 )
        self.sizer.SetFlexibleDirection( wx.HORIZONTAL )
        self.sizer.AddGrowableCol( 1 )
        for key, val in param_dict.items():
            name  = wx.StaticText( self.panel, label = key )
            entry = wx.TextCtrl( self.panel, value = str(val) )
            self.param_boxes[ key ] = entry
            self.sizer.Add( name, 0, wx.EXPAND | wx.ALL, 4)
            self.sizer.Add( entry, 1, wx.EXPAND | wx.ALL, 4 )
            
        self.sizer.AddSpacer((-1,10) )
        self.sizer.AddSpacer((-1,10) )
        
        # Ok and cancel buttons
        ok = wx.Button( self, wx.ID_OK )
        cancel = wx.Button( self, wx.ID_CANCEL )
        ok.Bind( wx.EVT_BUTTON, self.OnOk )
        ok.SetDefault()
        cancel.Bind( wx.EVT_BUTTON, self.OnCancel )
        button_sizer = wx.BoxSizer( wx.HORIZONTAL )
        button_sizer.AddStretchSpacer()
        button_sizer.Add( ok, 0, wx.EXPAND | wx.ALL, 10 )
        button_sizer.Add( cancel, 0, wx.EXPAND | wx.ALL, 10 )
        button_sizer.AddStretchSpacer()
        
        self.panel.SetSizer( self.sizer )
        szr = wx.BoxSizer( wx.VERTICAL )
        szr.Add( self.panel, 1, wx.EXPAND )
        szr.Add( button_sizer, 0, wx.EXPAND )
        self.SetSizer( szr )
        #self.Fit()
    # end InitUI
    
    def get_params( self ):
        '''Return the updated param dictionary'''
        return self.param_dict
    # end get_params

    def OnOk( self, event ):
        # Update the param dict with whatever the user changed
        for key, box in self.param_boxes.items():
            # Get the new value from the text box and cast it to the correct type
            new_value = box.GetValue()
            new_value = self.param_dtypes[key]( new_value )
            self.param_dict[key] = new_value
        self.EndModal( wx.ID_OK )
        self.Destroy()
        
    def OnCancel( self, event ):
        self.EndModal( wx.ID_CANCEL )
        self.Destroy()
# end ParamDialog

if __name__ == '__main__':
    '''
    Demo code to set up a dialog with bogus parameters and get user input back
    '''
    
    app = wx.App(0)
    dialog = ParamDialog(None)
    params = {'param1': 'a somewhat long string', 'param2' : 123, 'param3' : 456.7 }

    print 'Creating dialog. Params are:'
    for key, val in params.items():
        print '{0} : {1}'.format(key, val )

    # Init the dialog, show it, and check whether the user hit OK or CANCEL
    dialog.InitUI( params )
    rval = dialog.ShowModal( )
    new_params = dialog.get_params()
    if rval == wx.ID_CANCEL:
        print 'CANCEL.'
    else:
        print 'OK'

    print 'New params are:'
    for key, val in new_params.items():
        print '{0} : {1}'.format(key, val )
    
