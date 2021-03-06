# plotter.py
import matplotlib.pyplot as plt
import numpy as np
import nmmn.plots
parula = nmmn.plots.parulacmap() 

class QuadPlotter:
    """
    Quad plot window to plot real, imag, amp, and phase of S21.
    This is uses as a singleton.
    """
    def __init__(self, plot_dim=1, xlabel='xlabel()', ylabel=None, title=None, figsize=(12,10)):
        """ Create a layout of plot.
            Don't know what goes into each axes yet.
        """
        self.plot_dim = plot_dim
        self.xlabel = xlabel
        self.ylabel = ylabel
        
        self.fig = plt.figure(figsize = figsize)
        grid = plt.GridSpec(2,2,wspace=0.2, hspace=0.2)
        self.fig.suptitle(title)
        
        self.axes_amp = self.fig.add_subplot(grid[0,0])
        self.axes_phase = self.fig.add_subplot(grid[0,1])
        self.axes_real = self.fig.add_subplot(grid[1,0])
        self.axes_imag = self.fig.add_subplot(grid[1,1])
        
        self.plot_dim = plot_dim
        
        self.initialize()
    
    def initialize(self):     
        
        label_fontsize = 14
        tick_label_fontsize = 12
        
        self.axes_amp.set_xlabel(self.xlabel, fontsize=label_fontsize)
        self.axes_phase.set_xlabel(self.xlabel, fontsize=label_fontsize)
        self.axes_real.set_xlabel(self.xlabel, fontsize=label_fontsize)
        self.axes_imag.set_xlabel(self.xlabel, fontsize=label_fontsize)
            
        self.axes_amp.tick_params(axis='x', labelsize=tick_label_fontsize)
        self.axes_amp.tick_params(axis='y', labelsize=tick_label_fontsize)
        self.axes_phase.tick_params(axis='x', labelsize=tick_label_fontsize)
        self.axes_phase.tick_params(axis='y', labelsize=tick_label_fontsize)
        self.axes_real.tick_params(axis='x', labelsize=tick_label_fontsize)
        self.axes_real.tick_params(axis='y', labelsize=tick_label_fontsize)
        self.axes_imag.tick_params(axis='x', labelsize=tick_label_fontsize)
        self.axes_imag.tick_params(axis='y', labelsize=tick_label_fontsize)
        
        if self.plot_dim==1:
            self.line_amp, = self.axes_amp.plot([], [])
            self.line_phase, = self.axes_phase.plot([], [])
            self.line_real, = self.axes_real.plot([], [])
            self.line_imag, = self.axes_imag.plot([], [])
        
            self.axes_amp.set_ylabel('|S21|', fontsize=label_fontsize)
            self.axes_phase.set_ylabel('Phase(degree)', fontsize=label_fontsize)
            self.axes_real.set_ylabel('S21 Real', fontsize=label_fontsize)
            self.axes_imag.set_ylabel('S21 Imag', fontsize=label_fontsize)
            
        elif self.plot_dim==2:
                        
            self.axes_amp.set_ylabel(self.ylabel, fontsize=label_fontsize)
            self.axes_phase.set_ylabel(self.ylabel, fontsize=label_fontsize)
            self.axes_real.set_ylabel(self.ylabel, fontsize=label_fontsize)
            self.axes_imag.set_ylabel(self.ylabel, fontsize=label_fontsize)
        else:
            raise('Error! Plot dimension must be either 1 or 2.')
         
    def update(self, **kwargs):
        """
        Args:
            If plot_dim is 1, take 2 keyword arguments of
            xdata and ydata.
            If plot_dim is 2, take 3 keyword arguments of
            xdata, ydata, and data.
        """
        if self.plot_dim==1:
            xdata = kwargs['xdata']
            ydata = kwargs['ydata']
            self.line_amp.set_xdata(xdata)
            self.line_amp.set_ydata(np.abs(ydata))
            self.line_phase.set_xdata(xdata)
            self.line_phase.set_ydata(np.angle(ydata, deg=True))
            self.line_real.set_xdata(xdata)
            self.line_real.set_ydata(ydata.real)
            self.line_imag.set_xdata(xdata)
            self.line_imag.set_ydata(ydata.imag)
            
            self.axes_amp.relim()
            self.axes_amp.autoscale()
            self.axes_phase.relim()
            self.axes_phase.autoscale()
            self.axes_real.relim()y_axis
            self.axes_real.autoscale()
            self.axes_imag.relim()
            self.axes_imag.autoscale()
                        
            self.fig.canvas.draw() 
            self.fig.canvas.flush_events()
            
        elif self.plot_dim==2:            
            data = kwargs['data']
            x_mesh, y_mesh = np.meshgrid(kwargs['xdata'], kwargs['ydata'])                       
            color_amp   = self.axes_amp.pcolormesh(x_mesh, y_mesh, np.abs(data), cmap=parula)
            color_phase = self.axes_phase.pcolormesh(x_mesh, y_mesh, np.angle(data, deg=True), cmap=parula)       
            color_real  = self.axes_real.pcolormesh(x_mesh, y_mesh, data.real, cmap=parula)
            color_imag  = self.axes_imag.pcolormesh(x_mesh, y_mesh, data.imag, cmap=parula)
            # self.fig.colorbar(color_amp, cax=self.axes_amp)
            
            self.fig.canvas.draw() 
            self.fig.caself.nvas.flush_events()

class IQPlotter:
    """
    Plot in IQ plane.
    """
    def __init__(self, figsize=(8,8), xlabel='I', ylabel='Q', title='IQ plot'):
        """ Create a layout of plot.
            Don't know what goes into each axes yet.
        """
        
        self.fig, self.ax = plt.subplots(1, 1, figsize = figsize)
#         self.fig.tight_layout()    
        self.fig.suptitle(title)
    
        label_fontsize = 14
        tick_label_fontsize = 12
        
        self.ax.set_xlabel(xlabel, fontsize=label_fontsize)
        self.ax.set_ylabel(ylabel, fontsize=label_fontsize)
            
        self.ax.tick_params(axis='x', labelsize=tick_label_fontsize)
        self.ax.tick_params(axis='y', labelsize=tick_label_fontsize)
        
        self.line, = self.ax.plot([], [],'.')   
        
    def update(self, S21):
        """
        Args:
            S21: numpy array of S21
        
        """
        
        self.line.set_xdata(np.real(S21))
        self.line.set_ydata(np.imag(S21))
                                  
        self.ax.axis('equal')
        self.ax.relim()        
        self.ax.autoscale()
        
        self.fig.canvas.draw() 
        self.fig.canvas.flush_events()  

class Plot1D:
    """
    Description:
    """
    def __init__(self, figsize=(10,8), xlabel='xlabel()', ylabel='ylabel()', title='title', plotStyle='b-'):
        
        self.fig, self.ax = plt.subplots(1,1, figsize=figsize)
                
        label_fontsize = 14
        tick_label_fontsize = 12
        
        self.ax.set_xlabel(xlabel, fontsize=label_fontsize)
        self.ax.set_ylabel(ylabel, fontsize=label_fontsize)
            
        self.ax.tick_params(axis='x', labelsize=tick_label_fontsize)
        self.ax.tick_params(axis='y', labelsize=tick_label_fontsize)
        
        self.ax.set_title(title)
        
        self.lines, = self.ax.plot([], [], plotStyle) 

            
    def update(self, xdata, ydata):
        self.lines.set_xdata(xdata)
        self.lines.set_ydata(ydata)

        self.axes.relim()
        self.axes.autoscale()
        
        self.fig.canvas.draw() 
        self.fig.canvas.flush_events()
      
    
# quad_plotter = QuadPlotter()