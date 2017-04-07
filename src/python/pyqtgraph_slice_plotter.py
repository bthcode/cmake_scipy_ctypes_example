from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import numpy as np

class Test(QtGui.QMainWindow):
    def __init__(self, parent):
        super(self.__class__, self).__init__(parent)

        w = pg.GraphicsLayoutWidget()
        self.status_bar = QtGui.QStatusBar()
        self.setStatusBar( self.status_bar )
        
        self.plot_item = pg.PlotItem()
        self.image_item = pg.ImageItem()
        self.image_item.setOpts(axisOrder='row-major') #Need this or image will be transposed
        self.plot_item.addItem( self.image_item )

        w.addItem( self.plot_item, row=1, col=1, rowspan=3, colspan=3 )


        # Plot items for displaying the 'cuts' of the 2d image
        self.hplot = pg.PlotItem()
        self.vplot = pg.PlotItem()
        self.hplot.setMaximumHeight( 100 )
        self.vplot.setMaximumWidth( 100 )
        self.hplot.hideAxis('bottom')
        self.vplot.hideAxis('left')
        w.addItem(self.hplot, row=0, col=1 )
        w.addItem(self.vplot, row=1, col=0 )


        def mouseMoved(evt):
 
            mousePoint = self.image_item.getViewBox().mapSceneToView(evt)
            # Get horizontal index and vertical index into 2d array. 
            hidx = int(mousePoint.y())
            vidx = int(mousePoint.x())
            vidx = min(vidx, self.image_item.image.shape[1]-1)
            vidx = max(0, vidx)
            hidx = min(hidx, self.image_item.image.shape[0]-1)
            hidx = max(0, hidx)
 
            self.status_bar.showMessage( 'x = {:.2f}, y = {:.2f}, z = {:.2f}'.format(mousePoint.x(), mousePoint.y(), self.image_item.image[hidx, vidx] ) )
            self.hline.setValue( mousePoint.y() )
            self.vline.setValue( mousePoint.x() )

            # Plot the slices
            vslice = self.image_item.image[:, vidx]
            hslice = self.image_item.image[hidx,:]
            self.hplot.plot(hslice, clear=True)
            pl = self.vplot.plot(vslice, clear=True)
            pl.rotate(90)

        proxy = pg.SignalProxy(self.image_item.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)
        self.image_item.scene().sigMouseMoved.connect(mouseMoved)

        # Make the image we want to display
        x = np.arange(-5, 5, 0.1)
        y = np.arange(-5, 10, 0.1)
        xx, yy = np.meshgrid(x, y, sparse=True)
        self.img = np.sin(xx**2 + yy**2) / (xx**2 + yy**2)
        #self.img = np.random.rand( 200,300 )
        
        self.image_item.setImage( self.img )

        self.image_item.getViewBox().setLimits( xMin = 0, yMin = 0,
                                                xMax = self.image_item.image.shape[1],
                                                yMax = self.image_item.image.shape[0] )


        self.hline = pg.InfiniteLine(angle=0, pen=(255,0,0,100))
        self.vline = pg.InfiniteLine(angle=90, pen=(255,0,0,100))
        self.plot_item.addItem( self.hline )
        self.plot_item.addItem( self.vline )
        
        self.setCentralWidget( w )
        self.show()

# end Test

if __name__=='__main__':
    app = QtGui.QApplication([])
    win = Test(None)
    print('created')
    app.exec_()

    
