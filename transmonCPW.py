# Jaseung Ku
# Aug 2020

from scipy.special import ellipk
from scipy.constants import h, hbar, e, epsilon_0, mu_0, c
from scipy import optimize
import matplotlib.pyplot as plt
import numpy as np
from qutip import *

class CPW(object):
    """
    Coplanar Waveguide class
    
       air
    -------------       --------       -----------
       metal    |   s   |  w   |   s   |
    ----------------------------------------------
       dielectric
    ----------------------------------------------
       air
                      
    Parameters
    -----------
    w : width of center conductor in um
    s : gap size between center conductor and GND plane in um
    h : thickness of substrate in um
    t : thickness of metal in um
    epsilon_r: relative permeability of substrate
        
    TODO
    ----
    lambda_L vs thickness for metal.
    
    """
    
    def __init__(self, w=10, s=5, h=500, t=0.1, epsilon_r=11.6):
        self.w = w
        self.s = s
        self.h = h
        self.t = t
        self.epsilon_r = epsilon_r
        
    @property
    def b(self):
        return self.w + 2 * self.s
    
    @property
    def lambda_L(self):
        """
        London penentration depth of a metal in um. 
        This depends on thickness and temperature, but we assume T=0 since operating temperature is much lower than Tc.
        """
        
        # return 0.08 # for 100nm Nb
        return NotImplemented
    
    @property
    def epsilon_eff(self):
        """
        Effectvie permittivity for CPW with a single dielectric and no ground under the dielectric. Unitless
        Ref: Gupta et al., Microwsrip lnes and slotlines, 2nd edition
        Note that in scipy, the arguement to the complete elliptical integral of the first kind needs to be
        the square of k1.  
        In scipy, K(m) = \int_0^1 1 \frac{dt}{\sqrt( (1-t^2)(1-m*t^2))}, but in Gupta's book
                , K(k) = \int_0^1 1 \frac{dt}{\sqrt( (1-t^2)(1-k^2*t^2))}.
        """
               
        k1 = self.w / self.b
        k1_p = np.sqrt(1 - k1**2)

        k2 = np.sinh(np.pi*self.w/4/self.h) / np.sinh(np.pi*self.b/4/self.h)
        k2_p = np.sqrt(1 - k2**2)

        epsilon_eff = 1 + (self.epsilon_r - 1)/2*ellipk(k2**2)*ellipk(k1_p**2)/ellipk(k2_p**2)/ellipk(k1**2) 
                        
        return epsilon_eff
           
    @property
    def C_l(self):
        """
        Capacitance per unit length, F/m
        Ref: Gupta, Microstrip lines and slotlines
        Goppl paper uses the same expression, C_l = 4 * epsilon_0 * self.epsilon_eff * ellipk(k1**2)/ellipk(k1_p**2)
        """
        k1 = self.w / self.b
        k1_p = np.sqrt(1 - k1**2)
        k2 = np.sinh(np.pi*self.w/4/self.h) / np.sinh(np.pi*self.b/4/self.h)
        k2_p = np.sqrt(1 - k2**2)
            
        C1 = 2 * epsilon_0 * ellipk(k1**2)/ellipk(k1_p**2)
        C2 = 2 * epsilon_0 * (self.epsilon_r - 1) * ellipk(k2**2)/ellipk(k2_p**2)
        
        C_l = 2*C1 + C2
        
        return C_l

    @property
    def Lm_l(self):
        """ 
        Magnetic inductance per unit length, H/m
        Ref: Goople paper, Yosida1995(Schuster thesis): They show the same expressions.
        """
        k0 = self.w / self.b
        k0_p = np.sqrt(1 - k0**2)
        L_l = mu_0 / 4 * ellipk(k0_p**2)/ellipk(k0**2)
        
        return L_l
    
    @property
    def Lk_l(self):
        """
        Kinetic inductance per length on metal
        Ref: Yosida1995 (Schuster thesis)
        """
        
        k = self.w / self.b
        
        g = 1 / (2*(k*ellipk(k**2))**2) * (-np.log(self.t/4/self.w) + 2 * (self.w + self.s) / self.b * np.log(self.s/(self.w + self.s)) \
                                        - self.w/self.b *np.log(self.t/4/self.b))
        Lk_l = mu_0 * self.lambda_L / (self.w * self.s) * g
        
        return Lk_l
            
    
#     @property
#     def Z0(self):
#         """
#         Characteristic impedance of CPW.
#         Ref: Simons book (Schuster thesis)
#         """
#         k = self.w / self.b
#         k3 = np.sqrt(np.pi*self.w/4/self.h) / np.sqrt(np.pi*self.b/4/self.h)
#         k_p = np.sqrt(1 - k**2)
#         k3_p = np.sqrt(1 - k3**2)
        
#         Z0 = 60 * np.pi / np.sqrt(self.epsilon_eff) / (ellipk(k**2)/ellipk(k_p**2) + ellipk(k3**2)/ellipk(k3_p**2))
        
#         return Z0

    @property
    def Z0(self):
        """
        Characteristic impedance of CPW.
        Ref: Gupta
        """
        k = self.w / self.b
        k_p = np.sqrt(1 - k**2)
       
        Z0 = 30 * np.pi/np.sqrt(self.epsilon_eff) * ellipk(k_p**2)/ellipk(k**2)
       
        return Z0
    
    @property
    def vph(self):
        """ phase velocity"""

        return c/np.sqrt(self.epsilon_eff)

class QuarterWaveResonator(CPW):
    """
    CPW quart-wave resonator class. This inherits CPW class.
    
    Parameters
    ----------
    w, a, h, epsilon_sd
    w_r : undressed(no paracitics) fundamental resonant freq in rad/s       
    kappa : linewidh of resonant peak in rad/s
    
    TODO:
    Calculate frequency shift by coupling cap.
    """
    def __init__(self, w_r=None, kappa=None, L_paracitic=0, C_paracitic=0,**kwargs):
        super().__init__(**kwargs)
        self.w_r = w_r        
        self.kappa = kappa
        # self._L_paracitic = L_paracitic
        # self._C_paracitic = C_paracitic
                
    def __str__(self):
        out = f'w={self.w} um, s={self.s} um, h={self.h} um, e_r={self.epsilon_r}, f_r={self.w_r/2/np.pi/1e9 :.3f} GHz, kappa/2np.pi={self.kappa/2/np.pi/1e6 :.3f} MHz'
        return out

    
    @property
    def resonator_length(self):
        """
        Calculate the length of quarter-wave resonator in meter. 
        Lambda*freq = vph=c/sqrt(epsilon_eff)
        """
        # if self.kinetic_induct_include:
        #     total_induct_per_length = self.Lm_l + self.Lk_l
        # else:
        #     total_induct_per_length = self.Lm_l
            
        # w_r_pulled = self.get_dressed_res_freq()
        
        l = self.vph / (self.w_r/2/np.pi) / 4
        
        return l
    
    def get_w_r_dressed(self, L_paracitic=0, C_paracitic=0):
        """ Dressed resonant frequency in rad/s """
        C_LEA = (np.pi/4/self.Z0)/self.w_r
        L_LEA = (4*self.Z0/np.pi)/self.w_r
        
        C_tot = C_LEA + C_paracitic
        L_tot = L_LEA + L_paracitic
        
        w_r_dressed = 1/np.sqrt(L_tot*C_tot)
        
        return w_r_dressed
    
    
    def get_w_r_undressed(self, w_r_dressed, L_paracitic=0, C_paracitic=0):
        """ Undressed resonant frequency in rad/s"""
        w_Cp = np.pi/(4*self.Z0*C_paracitic)
        w_Lp = (4*self.Z0)/(np.pi*L_paracitic)
        w_LpCp = 1/np.sqrt(self.L_paracitic*C_paracitic)
        
        w_r_undressed = 1/2*( 
                        -(1/w_Cp+1/w_Lp)
                        + np.sqrt( (1/w_Cp+1/w_Lp)**2 + 4*(1/w_r_dressed**2-1/w_LpCp**2)))
        w_r_undressed = 1/w_r_undressed
      
        return w_r_undressed
    
    @property
    def Qc(self):
        return self.w_r/ self.kappa
    
    @property
    def Mc(self):
        """
        Mutual inductance between resonator and feedline, given w_r and kappa.
        Ref: Madison Simulation-and-Design
        """
        M = self.Z0 / self.w_r * np.sqrt(8/self.Qc/np.pi)
        
        return M 

class Transmon(object):
    """
    Charge qubit object
    
    Parameters
    ----------
    Ej : Josephson energy in Joule
    Ec : Charging energy in Joule
    N : number of charge states involved for Hamiltonian matrix
    ng_vec : numpy array of gate charge values.
    
    - Use classmethod 'in_GHz' if you want to use GHz unit for Ej and Ec.
    - Usage:  q = Transmon(Ej=10*1e9*h, Ec=0.3*1e9*h) or 
              q = Transmon.in_GHz(Ej=10, Ec=0.3)  
    """
    
    def __init__(self, Ej=0, Ec=0, N=10, Cj=0, ng_vec=np.linspace(-3, 3, 200)):
        self.Ej = Ej 
        self.Ec = Ec 
        self.N = N        
        self.ng_vec = ng_vec
        self.C_g= None # coupling capacitance
        self.Cj = 0 # junction capacitance
        
    @classmethod
    def in_GHz(cls, Ej=10, Ec=0.3, **kwargs):
        return cls(Ej=Ej*1e9*h, Ec=Ec*1e9*h, **kwargs)
        
    @property
    def energies(self):
        return  self._get_energies()
    
    def _get_energies(self):
        energies = np.array([self.hamiltonian(ng).eigenenergies() for ng in self.ng_vec])
        return energies
    
    def hamiltonian(self, ng):
        """
        Return the charge qubit hamiltonian as a Qobj instance.
        """
        N = self.N
        m = np.diag(4 * self.Ec * (np.arange(-N,N+1)-ng)**2) + 0.5 * self.Ej * (np.diag(-np.ones(2*N), 1) + 
                                                               np.diag(-np.ones(2*N), -1))
        return Qobj(m)

    @property
    def total_cap(self):
        """
        Total capacitance : C_j + C_g + C_s
        C_j : junction capacitance
        C_g : cap. between resonator and qubit
        C_s : shunt capacitance
        """
        return e**2 / self.Ec /2
    
    @total_cap.setter
    def total_cap(self, val):
        self.Ec  = e**2 / val /2
        
    @property
    def Ej_to_Ec_ratio(self):
        return self.Ej / self.Ec

    @property
    def charge_dispersion(self):
        """ Difference between max and min f01 """
        energies = self.energies  # to evaluate energies once
        f01 = (energies[:,1] - energies[:,0])/h
        charge_dispersion = (f01.max()-f01.min())

        return charge_dispersion
    
    @property
    def anharmonicity(self):
        energies = self.energies  # to evaluate energies once
        f01 = (energies[:,1] - energies[:,0]) / h
        f12 = (energies[:,2] - energies[:,1]) / h
        anharmonicity = (f12-f01).mean() 

        return anharmonicity
    
    @property
    def w01(self):
        """
        qubit frequency in Hz. Average of max and min over ng
        """
        energies = self.energies  # to **2evaluate energies once
        f01 = (energies[:,1] - energies[:,0]) / h
        freq_01 = (f01.max() + f01.min()) / 2

        return freq_01 * 2 * np.pi
    
    @property
    def f01(self):
        return self.w01 / 2/ np.pi
   
    def g01(self, res):
        """
        Calculate the coupling strength.
        Ref: Koch paper
        
        Parameters:
        res: Resonator object
        C_g: Coupling capacitance between resonator and qubit
        """

        Ej, Ec = self.Ej, self.Ec
        w_r = res.w_r
                
        matrix_element_01 = np.sqrt(1/2)*(Ej/8/Ec)**(1/4)
        if self.C_g is not None:
            beta = self.C_g / self.total_cap
        else:
            raise Exception('C_g is not defined')
        #     alpha = e**2 / (4*np.pi*epsilon_0*hbar*c)
        
        l = res.resonator_length
        Cr = res.C_l * l / 2  # This is true for both half-wave (goppl paper) and quarter-wave resonator (Gao thesis).
        V0rms = np.sqrt(hbar * w_r / 2 /Cr)
        
        g_01 = 2 * beta * e * V0rms * matrix_element_01 / hbar

        return g_01
    
    def g01_Madison(self, res):
        """
        g = 1/2 * Cg /np.sqrt(Cg+Cs)/np.sqrt(Cg+Cr)*np.sqrt(wr*wq)
        Cg: gate capacitance in F
        Cs: qubit shunt capacitance in F
        Cr: lump-element effective capacitance, Cr = C_l * l /2 , is this only true for half-wave CPW? what is Cr for quarter-wave
        wr: resonator frequency, rad/s
        wq: qubit 01 frequency, rad/s
        
        This expression comes from the model that two LC resonators coupled via gate capacitor(Cg).
        Note: I think Cg+Cs should be replaced with Cg+Cs+Cj....
        """
        C_r = res.C_l*res.resonator_length/2
        g_01 = 1/2 * self.C_g / np.sqrt(self.total_cap) / np.sqrt(self.C_g + C_r) * np.sqrt(self.w01 * res.w_r)
        
        return g_01
    
    def Chi01(self, res):
        """
        Ref: Koch paper
        res : Resonator object
        C_g : capacitance between resonator and qubit in rad/sec
        """
        delta = self.w01 - res.w_r
        anharm = self.anharmonicity
        
        if self.C_g is not None:
            Chi01 = self.g01(res)**2 / delta * (anharm/(anharm + delta)) 
        else:
            raise Exception('C_g is not defined.')
            
        return Chi01
    
    def plot_energies(self, ymax=(20, 3)):
        """
        Plot energy levels as a function of bias parameter ng_vec.
        """
        energies = self.energies  # to evaluate energies once
        
        fig, axes = plt.subplots(1,2, figsize=(16,6))

        for n in range(energies.shape[1]):
            axes[0].plot(self.ng_vec, energies[:,n]/1e9/h)

        axes[0].set_ylim((energies[0,:]/1e9/h).min() * 1.3, ymax[0]) # modified, JK
        axes[0].set_xlabel(r'$n_g$', fontsize=18)
        axes[0].set_ylabel(r'$E_n$', fontsize=18)

        for n in range(energies.shape[1]):
            axes[1].plot(self.ng_vec, (energies[:,n]-energies[:,0])/(energies[:,1]-energies[:,0]))

        axes[1].set_ylim(-0.2, ymax[1])
        axes[1].set_xlabel(r'$n_g$', fontsize=18)
        axes[1].set_ylabel(r'$(E_n-E_0)/(E_1-E_0)$', fontsize=18)
        
        return fig, axes
    
    def find_Ej_Ec(self, f01, anharm):
        """ 
        Given f01 and anharmonicity, find Ej and Ec.
        Minimize (f01-f(Ej, Ec))**2 + (anharmonictiy- anharm(Ej,Ec))**2 
        
        Args: f01 and anharm in SI unit
        Returns Ej and Ec.
        """
        sol = optimize.fmin(self._func, [12e9*h, 0.3e9*h], args=(f01, anharm))
        print(f'Ej={sol[0]/h/1e9} GHz, Ec={sol[1]/h/1e9} GHz')
        
        return sol
    
    def _func(self, x, *args):
        self.Ej = x[0]
        self.Ec = x[1]
#         print(f'Ej={self.Ej}')
#         print(f'Ec={self.Ec}')
        
        return (self.f01 - args[0])**2 +(self.anharmonicity - args[1])**2
    
    @property
    def Ic(self):
        """ 
        From Ej, calculate Ic from Ej = hbar*Ic/(2e)
               
        Returns: critical current of JJ
        """
                
        return self.Ej/hbar*(2*e)
    
    @property
    def Lj(self):
        """
        Josephson inductance .
        """
        return (h/2/e/2/np.pi)**2/self.Ej
