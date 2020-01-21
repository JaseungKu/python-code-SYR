# Jaseung Ku, Jan 2017

import numpy as np
import pyqtgraph as pg
import time
from pyqtgraph.Qt import QtCore, QtGui

class plot1D:
    """
    Description:
    """
    def __init__(self, xlabel='xlabel()', xunit='', ylabel='ylabel()', yunit='', title='title', plotStyle='b-'):
           
        # set up window
        self.win = pg.GraphicsLayoutWidget()
        self.win.setWindowTitle('Pyqtgraph Figure')
        self.win.resize(600, 400)
        self.win.show()
        
        # subplot1
        self.p1 = self.win.addPlot(row=1, col=0)
        self.curve1=self.p1.plot([], [], pen='y', symbol='s',symbolSize=4, symbolBrush='y', symbolPen=None)
        self.p1.setLabel('left', ylabel, units=yunit)
        self.p1.setLabel('bottom', xlabel, units=xunit)
        self.p1.showAxis('top', True)
        self.p1.showAxis('right', True)
        self.p1.setTitle(title)
        self.p1.showGrid(x=True, y=True)
    
    def update(self, xdata, ydata):
        self.curve1.setData(xdata, ydata)
        pg.QtGui.QApplication.processEvents()
        
                       
class plot1D_2sub:
    """
    Description:
    """
    def __init__(self, xlabel1='xlabel1()',xunit1='', ylabel1='ylabel1()', yunit1='', xlabel2='xlabel2()', xunit2='', ylabel2='ylabel2()', yunit2='',title='title', plotStyle='b-'):
        # set up window
        self.win = pg.GraphicsLayoutWidget()
        self.win.setWindowTitle('Pyqtgraph Figure')
        self.win.resize(800, 600)
        self.win.show()
        
        # subplot1
        self.p1 = self.win.addPlot(row=1, col=0)
        self.curve1=self.p1.plot([], [], pen='y', symbol='s',symbolSize=4, symbolBrush='y', symbolPen=None)
        self.p1.setLabel('left', ylabel1, units=yunit1)
        self.p1.setLabel('bottom', xlabel1, units=xunit1)
        #self.p1.showAxis('top', True)
        self.p1.showAxis('right', True)
        self.p1.setTitle(title)
        self.p1.showGrid(x=True, y=True)
                
        # subplot2
        self.win.nextRow()
        self.p2 = self.win.addPlot(row=2, col=0)
        self.curve2 = self.p2.plot([],[], pen='y', symbol='s', symbolSize=4, symbolBrush='y', symbolPen=None)
        self.p2.setLabel('left', ylabel2, units=yunit2)
        self.p2.setLabel('bottom', xlabel2, units=xunit2)
        self.p2.showAxis('right', True)
        self.p2.showGrid(x=True, y=True)
        #p2.setYRange(-2.5, 2.5)

    def update(self, xdata1, ydata1, xdata2, ydata2):
        self.curve1.setData(xdata1, ydata1)
        self.curve2.setData(xdata2, ydata2)
        pg.QtGui.QApplication.processEvents()
    
class plot2D:
    """
    Description:
    """
    def __init__(self, xlabel='xlabel()', xunit='', ylabel='ylabel()', yunit='', title='title', figsize=(10,5)):
    
        pg.setConfigOptions(imageAxisOrder='row-major')
        pg.setConfigOption('background', 'k')
        pg.setConfigOption('foreground', [200,200,255])

        self.win = pg.GraphicsLayoutWidget()
        self.win.setWindowTitle('Pyqtgraph Figure')

        # A plot area (ViewBox + axes) for displaying the image
        self.p1 = self.win.addPlot()

        # color table
        #pos = np.array([0.0, 0.5, 1.0])
        #color = np.array([[0,0,0,255], [255,128,0,255], [255,255,0,255]], dtype=np.ubyte)
        self.pos = np.array([0.0, 1.0])
        self.color = np.array([[0,0,0,255], [255,255,255,255]], dtype=np.ubyte)
        self.map1 = pg.ColorMap(self.pos, self.color)
        self.lut = self.map1.getLookupTable(0.0, 1.0, 256)

        # Item for displaying image data
        self.img = pg.ImageItem(lut=self.lut)
        self.p1.addItem(self.img)
        self.win.resize(800, 400)
        self.win.show()
        
        # Generate image data
        #self.img.setImage(data)

        self.p1.setLabel('left', ylabel, units=yunit)
        self.p1.setLabel('bottom', xlabel, units=xunit)
        self.p1.showAxis('top', True)
        self.p1.showAxis('right', True)
        self.p1.setTitle(title)

    def update(self, array_2D, extent, cmap='Blues_r'):
        self.img.setImage(array_2D)
        self.qrect  = QtCore.QRectF(extent[0], extent[2], extent[1]-extent[0], extent[3]-extent[2])
        self.img.setRect(self.qrect)
        pg.QtGui.QApplication.processEvents()
        self.p1.autoRange() # zoom to fit imageo
      
class plot2D_4sub(object):
    """
    Description:
    """
    def __init__(self, xlabel1='xlabel1()', xunit1='', ylabel1='ylabel1()', yunit1='', xlabel2='xlabel2()', xunit2='', ylabel2='ylabel2()', yunit2='', xlabel3='xlabel3()',  xunit3='', ylabel3='ylabel3()', yunit3='', xlabel4='xlabel4()', xunit4='', ylabel4='ylabel4()', yunit4='', title='title' ):
        
        #app = QtGui.QApplication([])
        self.view = pg.GraphicsView()
        self.l = pg.GraphicsLayout(border=(100,100,100))
        self.view.setCentralItem(self.l)
        self.view.show()
        self.view.setWindowTitle('pyqtgraph example: GraphicsLayout')
        self.view.resize(800,800)

        ## Add 2 plots into the first row (automatic position)
        self.p1 = self.l.addPlot(title="Plot amp")
        self.curve1 = self.p1.plot([], [],pen='y', symbol='s',symbolSize=4, symbolBrush='y', symbolPen=None)
        self.p1.setLabel('left', ylabel1, units='dB')
        self.p1.setLabel('bottom', xlabel1, units='Hz')
        self.p1.showAxis('right', True)
        self.p1.showGrid(x=True, y=True)
        
        self.l.nextRow()
        self.p2 = self.l.addPlot(title="Plot phase")
        self.curve2 = self.p2.plot([], [],pen='y', symbol='s',symbolSize=4, symbolBrush='y', symbolPen=None)
        self.p2.setLabel('left', ylabel2, units='dB')
        self.p2.setLabel('bottom', xlabel2, units='Hz')
        self.p2.showAxis('right', True)
        self.p2.showGrid(x=True, y=True)
        
        ## Add a sub-layout into the second row (automatic position)
        self.l.nextRow()
        self.l2 = self.l.addLayout(colspan=3, border=(50,0,0))

        self.vb = self.l2.addViewBox(lockAspect=True)
        self.img1 = pg.ImageItem([[]])
        sel.fvb.addItem(self.img1)

        self.l2.nextCol()
        self.vb2 = self.l2.addViewBox(lockAspect=True)
        self.img2 = pg.ImageItem([[]])
        self.vb2.addItem(self.img2)     
            
    def update1D(self, xdata1, ydata1, xdata2, ydata2): 
        self.curve1.setData(xdata1, ydata1)
        self.curve2.setData(xdata2, ydata2)
        pg.QtGui.QApplication.processEvents()
        
    def update2D(self, array1_2D, array2_2D, extent, cmap='Blues_r'):
        
        self.qrect  = QtCore.QRectF(extent[0], extent[2], extent[1]-extent[0], extent[3]-extent[2])
        self.img1.setImage(array1_2D)
        self.img1.setRect(self.qrect)
        
        self.img2.setImage(array2_2D)
        self.img2.setRect(self.qrect)
        
        pg.QtGui.QApplication.processEvents()
        self.p1.autoRange() # zoom to fit imageo
        self.p2.autoRange() # zoom to fit imageo