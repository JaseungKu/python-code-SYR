# Jaseung Ku, Aug 2016

import numpy as np
import matplotlib.pyplot as plt
import time

class plot1D:
    """
    Description:
    """
    def __init__(self, xlabel='xlabel()', ylabel='ylabel()', title='title', plotStyle='b-'):
        self.fig, self.axes = plt.subplots(1,1)
        self.lines, = self.axes.plot([], [], plotStyle) 
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        self.axes.ticklabel_format(useOffset=False)                      
#        self.textvar = plt.figtext(0.75, 0.92,'freq=')
            
    def update(self, x, y):
        self.lines.set_xdata(x)
        self.lines.set_ydata(y)
#        plt.gcf().texts.remove(self.textvar) # This and next line make code slow.
#        self.textvar = plt.figtext(0.75, 0.92,'freq='+str(x[-1]))
        self.axes.relim()
        self.axes.autoscale()
        #plt.draw()
        self.fig.canvas.draw() 
        self.fig.canvas.flush_events()
      #  plt.pause(0.001)


class plot1D_2sub:
    """
    Description:
    """
    def __init__(self, xlabel1='xlabel1()', ylabel1='ylabel1()', xlabel2='xlabel2()',ylabel2='ylabel2()',title='title', plotStyle='b-'):
        self.fig, (self.axes1, self.axes2) = plt.subplots(2,1)
        self.lines1, = self.axes1.plot([], [], plotStyle) 
        self.lines2, = self.axes2.plot([], [], plotStyle) 
        self.fig.suptitle(title)
        self.axes1.set_xlabel(xlabel1)
        self.axes1.set_ylabel(ylabel1)
        self.axes2.set_xlabel(xlabel2)
        self.axes2.set_ylabel(ylabel2)
        self.axes1.ticklabel_format(useOffset=False)
        self.axes2.ticklabel_format(useOffset=False)
#        self.textvar = plt.figtext(0.75, 0.92,'freq=')
            
    def update(self, xdata1, ydata1, xdata2, ydata2):
        self.lines1.set_xdata(xdata1)
        self.lines1.set_ydata(ydata1)
        self.lines2.set_xdata(xdata2)
        self.lines2.set_ydata(ydata2)
#        plt.gcf().texts.remove(self.textvar) # This and next line make code slow.
#        self.textvar = plt.figtext(0.75, 0.92,'freq='+str(x[-1]))
        self.axes1.relim()
        self.axes1.autoscale()
        self.axes2.relim()
        self.axes2.autoscale()
        #plt.draw()
        self.fig.canvas.draw() 
        self.fig.canvas.flush_events()
       # plt.pause(0.0001)

class plot2D:
    """
    Description:
    """
    def __init__(self, xlabel='xlabel()', ylabel='ylabel()', title='title', figsize=(12,5)):
        self.fig, self.axes = plt.subplots(nrows=1, figsize=figsize)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.xticks    
        self.axes.ticklabel_format(useOffset=False)
        #self.axesimage = self.axes.matshow([[]])
        #plt.colorbar(self.axesimage)
        #self.textvar = plt.figtext(0.75, 0.92, 'variable=')
    
    def update(self, array_2D, extent, cmap='viridis'):
        self.axesimage = self.axes.matshow(array_2D, cmap=cmap, extent=extent, origin='lower', aspect='auto')
        self.axesimage.set_data(array_2D)
        self.axes.xaxis.set_ticks_position('bottom')  
        #plt.colorbar(self.axesimage)
        #plt.gcf().texts.remove(self.textvar) # This and next line make code slow. Use when appropriate.
        #self.textvar = plt.figtext(0.75, 0.92, 'variable='+str(var))
        self.axes.autoscale()
        #plt.draw()
        self.fig.canvas.draw() 
        self.fig.canvas.flush_events()
       #plt.pause(0.001)
            
class plot2D_4sub(object):
    """
    Description:
    """
    def __init__(self, xlabel1='xlabel1()', ylabel1='ylabel1()', xlabel2='xlabel2()',ylabel2='ylabel2()', 
                 xlabel3='xlabel3()',ylabel3='ylabel3()',xlabel4='xlabel4()',ylabel4='ylabel4()',title='title', figsize=(12,8)):
        self.fig = plt.figure(figsize = figsize)
        self.axes1 = plt.subplot2grid((4,2), (0,0), colspan=2)
        self.axes2 = plt.subplot2grid((4,2), (1,0), colspan=2)
        self.axes3 = plt.subplot2grid((4,2), (2,0), rowspan=2)
        self.axes4 = plt.subplot2grid((4,2), (2,1), rowspan=2)
                              
        self.lines1, = self.axes1.plot([], [], 'b-o') 
        self.lines2, = self.axes2.plot([], [], 'b-o') 
                              
        self.axes1.set_xlabel(xlabel1)
        self.axes1.set_ylabel(ylabel1)
        self.axes2.set_xlabel(xlabel2)
        self.axes2.set_ylabel(ylabel2)
        self.axes3.set_xlabel(xlabel3)
        self.axes3.set_ylabel(ylabel3)
        self.axes4.set_xlabel(xlabel4)
        self.axes4.set_ylabel(ylabel4)                           
        self.axes1.ticklabel_format(useOffset=False)                      
        self.axes2.ticklabel_format(useOffset=False)                      
        self.axes3.ticklabel_format(useOffset=False)                      
        self.axes4.ticklabel_format(useOffset=False)                      
#        self.textvar = plt.figtext(0.75, 0.92,'freq=')
            
    def update1D(self, xdata1, ydata1, xdata2, ydata2):
        self.lines1.set_xdata(xdata1)
        self.lines1.set_ydata(ydata1)
        self.lines2.set_xdata(xdata2)
        self.lines2.set_ydata(ydata2)
#        plt.gcf().texts.remove(self.textvar) # This and next line make code slow.
#        self.textvar = plt.figtext(0.75, 0.92,'freq='+str(x[-1]))
        self.axes1.relim()
        self.axes1.autoscale()
        self.axes2.relim()
        self.axes2.autoscale()
        #plt.draw()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
      #  plt.pause(0.001)
        
    def update2D(self, array1_2D, array2_2D, extent, cmap='Blues_r'):
        self.axesimage1 = self.axes3.matshow(array1_2D, cmap=cmap, extent=extent, origin='lower', aspect='auto')
        self.axesimage2 = self.axes4.matshow(array2_2D, cmap=cmap, extent=extent, origin='lower', aspect='auto')
        self.axesimage1.set_data(array1_2D)
        self.axesimage2.set_data(array2_2D)
        self.axes3.xaxis.set_ticks_position('bottom')  
        self.axes4.xaxis.set_ticks_position('bottom')  
        #plt.colorbar(self.axesimage)
        #plt.gcf().texts.remove(self.textvar) # This and next line make code slow. Use when appropriate.
        #self.textvar = plt.figtext(0.75, 0.92, 'variable='+str(var))
        self.axes3.autoscale()
        self.axes4.autoscale()
        #plt.draw()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
      #  plt.pause(0.001)   

class PlotDAQ:
    """
    Description:
    """
    def __init__(self, xlabel1='xlabel1()'
                 , ylabel1='ylabel1()'
                 , xlabel2='xlabel2()'
                 , ylabel2='ylabel2()'
                 , xlabel3='xlabel3()'
                 , ylabel3='ylabel3()'
                 , title='title'
                 , figsize=(12,8)):
        
        self.fig = plt.figure(figsize = figsize)
        grid = plt.GridSpec(6,1 ,wspace=0.7, hspace=0.5)
        
        self.axes1 = self.fig.add_subplot(grid[0,0])
        self.axes2 = self.fig.add_subplot(grid[1,0])
        self.axes3 = self.fig.add_subplot(grid[2:6,0])
        self.axes1.set_title(title)    

        self.axes1.grid(which='both', linestyle='--')
        self.axes2.grid(which='both', linestyle='--')
        self.axes3.grid(which='both', linestyle='--')
                                      
        label_fontsize = 14
        ticklabel_fontsize = 12

        self.axes1.set_xlabel(xlabel1, fontsize=label_fontsize)
        self.axes1.set_ylabel(ylabel1, fontsize=label_fontsize)
        self.axes2.set_xlabel(xlabel2, fontsize=label_fontsize)
        self.axes2.set_ylabel(ylabel2, fontsize=label_fontsize)
        self.axes3.set_xlabel(xlabel3, fontsize=label_fontsize)
        self.axes3.set_ylabel(ylabel3, fontsize=label_fontsize)
        
        self.axes1.ticklabel_format(useOffset=False)                      
        self.axes2.ticklabel_format(useOffset=False)                      
        self.axes3.ticklabel_format(useOffset=False)                      
        
        self.lines1, = self.axes1.plot([], [], 'b-') 
        self.lines2, = self.axes2.plot([], [], 'b-') 
        self.lines3, = self.axes3.plot([], [], 'ro', fillstyle='none')
        self.lines4, = self.axes3.plot([], [], 'k-')
                
        self.axes3.tick_params(axis='x', labelsize=ticklabel_fontsize)
        self.axes3.tick_params(axis='y', labelsize=ticklabel_fontsize)
                       
    def update(self, timedata, ydata1, ydata2, I_avg, V_avg, V_fit, fit_res):
        self.lines1.set_xdata(timedata)
        self.lines1.set_ydata(ydata1)
        self.lines2.set_xdata(timedata)
        self.lines2.set_ydata(ydata2)
        
        self.lines3.set_xdata(I_avg)
        self.lines3.set_ydata(V_avg)
        self.lines4.set_xdata(I_avg)
        self.lines4.set_ydata(V_fit)

        self.axes1.relim()
        self.axes1.autoscale()
        self.axes2.relim()
        self.axes2.autoscale()
        self.axes3.relim()
        self.axes3.autoscale()
        
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        
        self.axes3.legend(("Data", f'Linear Fit\nR={fit_res:.1f} Ω'), loc=0, fontsize=16, frameon=False)
        
class PlotXY(object):
    """
    Description: plot VI
    """
    def __init__(self
                 , xlabel1='xlabel()'
                 , ylabel1='ylabel()'
                 , title='title'
                 , figsize=(10,8)):
        
        self.fig = plt.figure(figsize = figsize)
           
        self.axes1 = self.fig.add_subplot()
        self.axes1.set_title(title)    
        self.axes1.grid(which='both', linestyle='--')
                                      
        label_fontsize = 14
        ticklabel_fontsize = 12
        self.axes1.set_xlabel(xlabel1, fontsize=label_fontsize)
        self.axes1.set_ylabel(ylabel1, fontsize=label_fontsize)
        self.axes1.ticklabel_format(useOffset=False)                      
                       
        self.axes1.tick_params(axis='x', labelsize=ticklabel_fontsize)
        self.axes1.tick_params(axis='y', labelsize=ticklabel_fontsize)
               
#         self.axes1.axhline(color='k', linestyle='-')
#         self.axes1.axvline(color='k', linestyle='-')
        
        self.lines1, = self.axes1.plot([], [], 'bo-') 
        
    def update(self, I, V):
        self.lines1.set_xdata(I)
        self.lines1.set_ydata(V)
        
        self.axes1.relim()
        self.axes1.autoscale()
               
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        