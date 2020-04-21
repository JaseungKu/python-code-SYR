import numpy as np

def g_eff(wc, w1, w2, C1, C2, C12, C1c, C2c, Cc):
    """
    w in GHz and C in fF
    """
    eta = C1c*C2c/C12/Cc
    Sigma = 2 / (1/(w1+wc) + 1/(w2+wc))
    Delta = 2/(1/(w1-wc) + 1/(w2-wc))

    g = 1/2*(wc*eta/2/Delta - wc*eta/2/Sigma + eta + 1)* C12 *np.sqrt(w1*w2)/np.sqrt(C1*C2)
    
    return g

def g1(wc,w1,C1,C1c,Cc):
    """
    Qubit-coupler coupling strengh in GHz.
    C in fF
    """
    g1 = 1/2*C1c/np.sqrt(C1*Cc)*np.sqrt(w1*wc)
    
    return g1

def g2(wc,w2,C2,C2c,Cc):
    """
    Qubit-coupler coupling strengh in GHz.
    C in fF
    """
    g2 = 1/2*C2c/np.sqrt(C2*Cc)*np.sqrt(w2*wc)
    
    return g2

def g12(w1,w2,C1,C2,C12, C1c,C2c,Cc):
    """
    Qubit-qubit coupling strengh in GHz.
    C in fF
    """
    eta = C1c*C2c/C12/Cc
    g12 = 1/2*(1 + eta)*C12/np.sqrt(C1*C2)*np.sqrt(w1*w2)
    
    return g12

