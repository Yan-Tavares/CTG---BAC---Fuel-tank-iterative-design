import math as m
import numpy as np
#import Failure_Check as fc
from Functions import Attachment_design as Ad
from Functions import WP5_ParisV2 as Paris

def Force_calculator(m_tank_dry,m_attachment):
    m_SC_dry = 374
    m_fuel = 143.42

    a_x = 3 * 9.81
    a_y = 3 * 9.81
    az = 8.5*9.81 
    SF = 1.5
    
    m_tot = m_fuel + m_SC_dry + m_attachment + m_tank_dry

    F_x_max = m_tot * a_x * SF
    F_y_max = m_tot * a_y * SF
    F_z_max = m_tot * az * SF

    return F_x_max,F_y_max,F_z_max

def Attachment_mass_calc(F_x_max,F_y_max,F_z_max):
    D_max_crossection = 0.10

    n_att_upper = 3
    L_att_upper = 0.2650

    n_att_midle = 3
    L_att_middle = 0.1460

    n_att_lower = 3
    L_att_lower = 0.1725

    m_att_upper = Ad.Attachment_design(F_x_max,F_y_max,F_z_max, D_max_crossection , L_att_upper  , 3 ,"Upper","H_Cylinder")[6]*n_att_upper
    m_att_middle = Ad.Attachment_design(F_x_max,F_y_max,F_z_max, D_max_crossection , L_att_middle  , 3 ,"Middle","I_Beam")[6]*n_att_midle
    m_att_lower = Ad.Attachment_design(F_x_max,F_y_max,F_z_max, D_max_crossection , L_att_lower  , 3 ,"Bottom","H_Cylinder")[6]*n_att_lower

    return m_att_upper,m_att_middle,m_att_lower


def Mass_tank_calculation(Rho,t1,R):
    m = 4/3*np.pi*((R+t1)**3 - (R**3))*Rho

    return m


 #Design space is a square which has a side of D_max_crossection

#----------------- IMPUT PARAMETERS

Rho = 2.84*10**3 # AL-2219: 2.85*10**
E = 73.8*10**9 # AL-2219: 73.8*10**9
R = 0.33
t1 = 0.007
m_att_tot = 0
biggest_t1 = t1
t1_stepsize = 0.0001

#----------------- ITERATIVE DESIGN





m_tank_dry = Mass_tank_calculation(Rho,t1,R)


F_x_max,F_y_max,F_z_max = Force_calculator(m_tank_dry,m_att_tot)
m_att_tot = sum(Attachment_mass_calc(F_x_max,F_y_max,F_z_max))
Sigma_cr1, sigma_cr, sigma_applied = Paris.Check_failure(t1,E,F_z_max)[2:5]

print("-----------------------------------------")
print("Initial Properties")
print("-----------------------------------------\n")
print('Initial thickness', t1 * 1000, '[mm]')
print('Initial mass of the fuel tank', round(m_tank_dry,2), '[kg]')
print('Initial mass of the attachments', round(m_att_tot,2), '[kg]')
print('Shell Buckling', round(Sigma_cr1 *10**(-6),4), '[Mpa]')
print('Column Buckling', round(sigma_cr *10**(-6),4), '[Mpa]')
print('Sigma applied', round(sigma_applied *10**(-6),4), '[Mpa]')

print("\n")


steps = 2

for i in range (0,steps):


    if not Paris.Check_failure(t1,E,F_z_max)[0]:
        while not Paris.Check_failure(t1,E,F_z_max)[0] and t1 >= 0: 
            if t1 < 0.0022 + t1_stepsize: 
                break 

            if t1 - t1_stepsize > 0: 
                t1 -=  t1_stepsize # stepsize 

    if Paris.Check_failure(t1,E,F_z_max)[0]:
        while Paris.Check_failure(t1,E,F_z_max)[0]: 
            t1 += t1_stepsize # stepsize 


    Sigma_cr1, sigma_cr, sigma_applied = Paris.Check_failure(t1,E,F_z_max)[2:5]

    m_tank_dry = Mass_tank_calculation(Rho,t1,R)
    F_x_max,F_y_max,F_z_max = Force_calculator(m_tank_dry,m_att_tot)
    m_att_tot = sum(Attachment_mass_calc(F_x_max,F_y_max,F_z_max))


print("-----------------------------------------")
print("Final Properties")
print("-----------------------------------------\n")


print('Final tank mass', round(m_tank_dry,2), '[kg]')
print('Final attachment mass', round(m_att_tot,2), '[kg]')
print('Shell Buckling', round(Sigma_cr1 *10**(-6),4), '[Mpa]')
print('Column Buckling', round(sigma_cr *10**(-6),4), '[Mpa]')
print('Sigma applied', round(sigma_applied *10**(-6),4), '[Mpa]')


print("\n")


print('The final thickness is', round(t1*1000, 4), '[mm]')  

# print("Total mass is", Mass_count(mass_list), '[kg]') 





E = 1600000
I = 1046
R = 4
L = 60
total_mass = 517.42-26.654 


p = 101325
v = 0.333
lamda = 1 
stepsize = 0.0005 


# def Mass_count(mass_list): #should get the mass of the attachments as a list, 5.4, talk to Yan. 
#     # Iterate in 5.3, talk to Paris. 
#     sum_from_list = sum(mass_list)  
#     total_mass = 374-26.654 + sum_from_list
#     return total_mass 




# def Check_failure(t):  
#     return fc.failure1 

# Compare t1 and t2 with internal pressure  



