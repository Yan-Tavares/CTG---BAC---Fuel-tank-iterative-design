import math as m

#random values for now
E = 1600000
I = 1046
R = 4
L = 60
F = 24368.4324 #not random acceleration from wp4 times (mass of S/C - mass of fuel tank)  = 292.24 kg, acceleration = 8.5 g with g = 9.801 units
t1 = 0.007
p = 101325
v = 0.333
lamda = 1 


def Check_failure(t1):

    F = 24368.4324
    failure1 = False 
    failure2 = False 
    A = m.pi*(R**2) 


    def sigma_applied_calulator(F, A):
        s_applied = F/A 
        
        return s_applied

    sigma_applied =  sigma_applied_calulator(F, A) 
    ##print ('Sigma applied:', sigma_applied) 

    def Euler_column_buckling_calculator(E, I, A, L): 

        critical_stress = (m.pi**2 * E * I)/ (A * L**2) 
        return critical_stress 
    sigma_cr = Euler_column_buckling_calculator(E, I, A, L) 

    ##print("Critical Euler column buckling stress:", sigma_cr) 


    if sigma_cr < sigma_applied:
        failure1 = True
    else:
        failure1 = False


    # if failure1:
    #     print('Tank fails due to Euler column buckling.')
    # else:
    #     print('No failure due to Euler column buckling.')

    def k_calculator(lamda, L, R, t1, v):
        k = lamda + (12 / m.pi**4) * (L**4 / (R**2 * t1**2)) * (1 - v**2) * (1 / lamda)
        return k

    k_value = k_calculator(lamda, L, R, t1, v) 

    def Q_calculator(p, E, R, t1): 
        Q = (p/E)*(R/t1)**2 
        return Q 
    
    Q = Q_calculator(p, E, R, t1) 

    def Shell_buckling_calculator(E, t1, L, v, p, Q, k_value):
        
        sigma_cr1 = (1.983 - 0.983*m.e**(-23.14*Q))* k_value *((m.pi**2*E)/(12*(1-v**2)))*(t1/L)**2
        return sigma_cr1

    Sigma_cr1 = Shell_buckling_calculator(E, t1, L, v, p, Q, k_value)
    ##print("Critical stress for shell buckling:", Sigma_cr1)

    if Sigma_cr1 < sigma_applied: 
        failure2 = True  
    else: 
        failure2 = False 
    # if failure2: 
    #     print('Tank fails due to shell buckling.') 
    # else: 
    #     print('No failure due to shell buckling.') 
    return failure1, failure2 

#print(Check_failure(t1)) # Returns the euler column buckling stress and critical stress for shell buckling.
