import math as m
import numpy as np
#import Failure_Check as fc
from Functions import Attachment_design as Ad
from Functions import WP5_ParisV2 as Paris

def Force_calculator(m_tank_dry,m_attachment):
    m_SC_dry = 374 - 76.54
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
    D_max_crossection = 0.02

    n_att_upper = 3
    L_att_upper = 0.2650

    n_att_midle = 3
    L_att_middle = 0.1460

    n_att_lower = 4
    L_att_lower = 0.1725

    m_att_upper, D_min_upper = Ad.Attachment_design(F_x_max,F_y_max,F_z_max, D_max_crossection , L_att_upper  , n_att_upper ,"Upper","H_Cylinder")[6]*n_att_upper, Ad.Attachment_design(F_x_max,F_y_max,F_z_max, D_max_crossection , L_att_upper  ,  n_att_upper ,"Upper","H_Cylinder")[5]
    m_att_middle, D_min_middle = Ad.Attachment_design(F_x_max,F_y_max,F_z_max, D_max_crossection , L_att_middle  , n_att_midle ,"Middle","I_Beam")[6]*n_att_midle, Ad.Attachment_design(F_x_max,F_y_max,F_z_max, D_max_crossection , L_att_middle  , n_att_midle ,"Middle","I_Beam")[5]
    m_att_lower, D_min_lower = Ad.Attachment_design(F_x_max,F_y_max,F_z_max, D_max_crossection , L_att_lower  , n_att_lower ,"Bottom","H_Cylinder")[6]*n_att_lower, Ad.Attachment_design(F_x_max,F_y_max,F_z_max, D_max_crossection, L_att_lower  , n_att_lower ,"Bottom","H_Cylinder")[5]

    

    return m_att_upper,m_att_middle,m_att_lower,D_min_upper,D_min_middle,D_min_lower


def Mass_tank_calculation(Rho,t1,R):
    m = 4/3*np.pi*((R+t1)**3 - (R**3))*Rho

    return m


#----------------- IMPUT PARAMETERS
D_max_crossection = 0.02
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


steps = 1

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
    m_att_tot = sum(Attachment_mass_calc(F_x_max,F_y_max,F_z_max)[0:3])

F_x_max,F_y_max,F_z_max = Force_calculator(m_tank_dry,m_att_tot)
D_min_upper,D_min_middle,D_min_lower = Attachment_mass_calc(F_x_max,F_y_max,F_z_max)[3:6]
m_att_upper,m_att_middle,m_att_lower = Attachment_mass_calc(F_x_max,F_y_max,F_z_max)[0:3]


# n_att_lower = 1
# L_att_lower = 0.1725
# print("Lower attachment axial load", Ad.Attachment_design(F_x_max,F_y_max,F_z_max, D_max_crossection , L_att_lower  , n_att_lower ,"Bottom","H_Cylinder")[-1])

print("-----------------------------------------")
print("Final Properties")
print("-----------------------------------------\n")

print('Final tank thickness is', round(t1*1000, 4), '[mm]') 
print('Final tank mass', round(m_tank_dry,2), '[kg]')
print('Final attachment mass', round(m_att_tot,2), '[kg]')
print('Upper attachment thickness', round((D_max_crossection - D_min_upper)*1000,2), '[mm]')
print('Middle attachment thickness', round((D_max_crossection - D_min_middle)*1000,2), '[mm]')
print('Lower attachment thickness', round((D_max_crossection - D_min_lower)*1000,2), '[mm]')
print('Shell Buckling', round(Sigma_cr1 *10**(-6),4), '[Mpa]')
print('Column Buckling', round(sigma_cr *10**(-6),4), '[Mpa]')
print('Sigma applied', round(sigma_applied *10**(-6),4), '[Mpa]')
print("\n")


print(m_att_upper )
print(m_att_middle)
print(m_att_lower)

# print("Total mass is", Mass_count(mass_list), '[kg]') 


# n_att_upper = 3
# L_att_upper = 0.2650

# n_att_midle = 3
# L_att_middle = 0.1460

# n_att_lower = 3
# L_att_lower = 0.1725

# max_trans_up = Ad.Attachment_design(F_x_max,F_y_max,F_z_max, D_max_crossection , L_att_upper  , 3 ,"Upper","H_Cylinder")[2]
# max_trans_mid = Ad.Attachment_design(F_x_max,F_y_max,F_z_max, D_max_crossection , L_att_middle  , 3 ,"Middle","I_Beam")[2]
# max_trans_down = Ad.Attachment_design(F_x_max,F_y_max,F_z_max, D_max_crossection , L_att_lower  , 3 ,"Bottom","H_Cylinder")[2]

# print(max_trans_up)
# print(max_trans_mid)
# print(max_trans_down)



# def Mass_count(mass_list): #should get the mass of the attachments as a list, 5.4, talk to Yan. 
#     # Iterate in 5.3, talk to Paris. 
#     sum_from_list = sum(mass_list)  
#     total_mass = 374-26.654 + sum_from_list
#     return total_mass 




# def Check_failure(t):  
#     return fc.failure1 

# Compare t1 and t2 with internal pressure  



