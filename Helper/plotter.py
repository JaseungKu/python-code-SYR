# plotter.py

import matplotlib.pyplot as plt
import numpy as np
import nmmn.plots
parula = nmmn.plots.parulacmap() 

class QuadPlotter(object):
    """
    Quad plot window to plot real, imag, amp, and phase of S21.
    """
    def __init__(self, figsize=(12,10)):
        """ Create a layout of plot.
            Don't know what goes into each axes yet.
        """
        
        self.fig = plt.figure(figsize = figsize)
        grid = plt.GridSpec(2,2,wspace=0.2, hspace=0.2)
#         self.fig.suptitle(title)
        
        self.axes_amp = self.fig.add_subplot(grid[0,0])
        self.axes_phase = self.fig.add_subplot(grid[0,1])
        self.axes_real = self.fig.add_subplot(grid[1,0])
        self.axes_imag = self.fig.add_subplot(grid[1,1])
      
    
    def initialize(self, plot_dim=1, xlabel='xlabel()', ylabel=None, title='title'):
        self.fig.suptitle(title)
        self.plot_dim = plot_dim
        label_fontsize = 14
        tick_label_fontsize = 12
        self.axes_amp.set_xlabel(xlabel, fontsize=label_fontsize)
        self.axes_phase.set_xlabel(xlabel, fontsize=label_fontsize)
        self.axes_real.set_xlabel(xlabel, fontsize=label_fontsize)
        self.axes_imag.set_xlabel(xlabel, fontsize=label_fontsize)
            
        self.axes_amp.tick_params(axis='x', labelsize=tick_label_fontsize)
        self.axes_amp.tick_params(axis='y', labelsize=tick_label_fontsize)
        self.axes_phase.tick_params(axis='x', labelsize=tick_label_fontsize)
        self.axes_phase.tick_params(axis='y', labelsize=tick_label_fontsize)
        self.axes_real.tick_params(axis='x', labelsize=tick_label_fontsize)
        self.axes_real.tick_params(axis='y', labelsize=tick_label_fontsize)
        self.axes_imag.tick_params(axis='x', labelsize=tick_label_fontsize)
        self.axes_imag.tick_params(axis='y', labelsize=tick_label_fontsize)
        
        if plot_dim==1:
            self.line_amp, = self.axes_amp.plot([], [])
            self.line_phase, = self.axes_phase.plot([], [])
            self.line_real, = self.axes_real.plot([], [])
            self.line_imag, = self.axes_imag.plot([], [])
        
            self.axes_amp.set_ylabel('|S21|', fontsize=label_fontsize)
            self.axes_phase.set_ylabel('Phase(degree)', fontsize=label_fontsize)
            self.axes_real.set_ylabel('S21 Real', fontsize=label_fontsize)
            self.axes_imag.set_ylabel('S21 Imag', fontsize=label_fontsize)
            
        elif plot_dim==2:
                        
            self.axes_amp.set_ylabel(ylabel, fontsize=label_fontsize)
            self.axes_phase.set_ylabel(ylabel, fontsize=label_fontsize)
            self.axes_real.set_ylabel(ylabel, fontsize=label_fontsize)
            self.axes_imag.set_ylabel(ylabel, fontsize=label_fontsize)
        else:
            raise('Error! Plot dimension must be either 1 or 2.')
         
    def update(self, **kwargs):
        """
        Args:
            If plot_dim is 1, take keyword arguments of
            xdata, amp, phase, real and imag.
            
            If plot_dim is 2, take keyword arguments of
            x_axis, y_axis, amp, phase, real, imag.
        """
        if self.plot_dim==1:
            self.line_amp.set_xdata(kwargs['xdata'])
            self.line_amp.set_ydata(kwargs['amp'])
            self.line_phase.set_xdata(kwargs['xdata'])
            self.line_phase.set_ydata(kwargs['phase'])
            self.line_real.set_xdata(kwargs['xdata'])
            self.line_real.set_ydata(kwargs['real'])
            self.line_imag.set_xdata(kwargs['xdata'])
            self.line_imag.set_ydata(kwargs['imag'])
            
            self.axes_amp.relim()
            self.axes_amp.autoscale()
            self.axes_phase.relim()
            self.axes_phase.autoscale()
            self.axes_real.relim()
            self.axes_real.autoscale()
            self.axes_imag.relim()
            self.axes_imag.autoscale()
                        
            self.fig.canvas.draw() 
            self.fig.canvas.flush_events()
            
        elif self.plot_dim==2:
            x_mesh, y_mesh = np.meshgrid(kwargs['x_axis'], kwargs['y_axis'])            
            color_amp = self.axes_amp.pcolormesh(x_mesh, y_mesh, kwargs['amp'], cmap=parula)
            color_phase = self.axes_phase.pcolormesh(x_mesh, y_mesh, kwargs['phase'], cmap=parula)       
            color_real = self.axes_real.pcolormesh(x_mesh, y_mesh, kwargs['real'], cmap=parula)
            color_imag = self.axes_imag.pcolormesh(x_mesh, y_mesh, kwargs['imag'], cmap=parula)
            # self.fig.colorbar(color_amp, cax=self.axes_amp)
            
            self.fig.canvas.draw() 
            self.fig.canvas.flush_events()

class IQPlotter(object):
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
          
# quad_plotter = QuadPlotter()