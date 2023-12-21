import math as m
import numpy as np


def sigma_applied_calulator(F, A):
        s_applied = F/A 
        
        return s_applied

def Euler_column_buckling_calculator(E, I, A, L): 
        critical_stress = (m.pi**2 * E * I)/ (A * L**2) 
        return critical_stress

def k_calculator(lamda, L, R, t1, v):
    k = lamda + (12 / m.pi**4) * (L**4 / (R**2 * t1**2)) * (1 - v**2) * (1 / lamda)
    return k

def Q_calculator(p, E, R, t1): 
    Q = (p/E)*(R/t1)**2 
    return Q 

def Shell_buckling_calculator(E, t1, L, v, p, Q, k_value):
    
    sigma_cr1 = (1.983 - 0.983*m.e**(-23.14*Q))* k_value *((m.pi**2*E)/(12*(1-v**2)))*(t1/L)**2
    return sigma_cr1


def Check_failure(t1,E,F):
    lamda = 1 
    R = 0.33
    L = 2*R
    p = 3*10**6
    v = 0.333

    I = (np.pi/4) * ((R+t1)**4 - R**4)
    A = m.pi*((R+t1)**2 - (R)**2) 

    sigma_applied =  sigma_applied_calulator(F, A) 
    sigma_cr = Euler_column_buckling_calculator(E, I, A, L)

    # print("The Sigma aplied",sigma_applied)

    # print("Critical column buckling:", sigma_cr)

    # failure1 = False 
    # failure2 = False
    
    if sigma_cr < sigma_applied:
        failure1 = True
    else:
        failure1 = False


    # if failure1:
    #     print('Tank fails due to Euler column buckling.')
    # else:
    #     print('No failure due to Euler column buckling.')

    k_value = k_calculator(lamda, L, R, t1, v) 
    Q = Q_calculator(p, E, R, t1) 

    Sigma_cr1 = Shell_buckling_calculator(E, t1, L, v, p, Q, k_value)
    
    # print("Critical stress for shell buckling:", Sigma_cr1)

    if Sigma_cr1 < sigma_applied: 
        failure2 = True  
    else: 
        failure2 = False 
    # if failure2: 
    #     print('Tank fails due to shell buckling.') 
    # else: 
    #     print('No failure due to shell buckling.') 
    return failure1, failure2, Sigma_cr1, sigma_cr, sigma_applied

#print(Check_failure(t1)) # Returns the euler column buckling stress and critical stress for shell buckling.
