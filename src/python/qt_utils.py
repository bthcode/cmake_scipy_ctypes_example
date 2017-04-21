import os
from PyQt4 import QtCore, QtGui

from IPython.qt.console.rich_ipython_widget import RichIPythonWidget
from IPython.qt.manager import QtKernelManager
from IPython.qt.inprocess import QtInProcessKernelManager
from IPython.kernel.zmq.ipkernel import Kernel
from IPython.kernel.inprocess.ipkernel import InProcessKernel
from IPython.lib import guisupport



class Embedded_Console( RichIPythonWidget ):
    '''The guts of this code was taken from https://gist.github.com/stephanh42/a8db0dc2e9cc5aaf4214'''

    def __init__( self, parent ):
        super(self.__class__, self).__init__(parent)
        
        # Create an in-process kernel
        kernel = InProcessKernel(gui='qt4')
        kernel_manager = QtInProcessKernelManager(kernel=kernel)

        kernel_manager.start_kernel()
        kernel_client = kernel_manager.client()
        kernel_client.start_channels()

            
        self.kernel_manager = kernel_manager
        self.kernel_client = kernel_client
        self.kernel = kernel
        self.exit_requested.connect(self._stop)
        self.show()
    # end __init__

    def _stop(self):
        self.kernel_manager.shutdown_kernel()
        self.kernel_client.stop_channels()
        self.kernel_manager = None
    # end _stop
    
    def push_var( self, name, val ):
        '''Send the input var to the console. It will be available to the console as name'''
        self.kernel.shell.push({ name : val } )
    # end push_var

# end Embedded_Console


class Embedded_Console_Window( QtGui.QMainWindow ):
    '''Wraps an Embedded_Console in a main window'''
    def __init__(self, parent):
        super(self.__class__, self).__init__(parent)
        self.console = Embedded_Console( self )
        self.setCentralWidget( self.console )
        self.show()
    # end __init__

    def push_var( self, *args ):
        self.console.push_var( *args )
# end Embedded_Console_Window


class Console_Test( QtGui.QMainWindow ):
    '''Test class for console'''
    def __init__(self):
        super(self.__class__, self).__init__(None)


        self.console = Embedded_Console_Window(self)
        self.console.push_var( 'test', self)
        self.console.hide()
        
        self.menubar = self.menuBar()
        self.file_menu = self.menubar.addMenu( '&File' )

        view_console_action = QtGui.QAction('View console', self )
        view_console_action.triggered.connect( lambda : self.console.show() )
        self.file_menu.addAction( view_console_action )
        self.show()

        
def test_console():
    app = QtGui.QApplication([])
    win = Console_Test()
    app.exec_()
    
if __name__ == '__main__':
    test_console()
