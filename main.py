import numpy as np


P_x = 1000
P_y = 5000
P_z = 7000

R_outer_mid = 0.05
R_inner_mid = 0.04
L_mid = 0.25
num_mid = 3
Alpha_mid = np.radians(360/num_mid)
I_mid = (np.pi/4)*(R_outer_mid**4 - R_inner_mid**4)

R_outer_d = 0.05
R_inner_d = 0.04
L_d = 0.25
num_d = 3
Phi_d = np.radians(60)
Alpha_d = np.radians(360/num_d)

R_outer_u = 0.05
R_inner_u = 0.04
L_u = 0.25 
num_u = 3
Phi_u = np.radians(60)
Alpha_u = np.radians(360/num_d)


E_modulus = 100 * 10**9



#------ Create support vectors

F_z_d = np.array([0,0,-P_z/3])

L_d_vec_list = []


for i in range (3):
    Alpha_i = i * Alpha_d
    L_d_vec = np.array([L_d*np.cos(Phi_d),
                     L_d*np.cos(Phi_d)*np.sin(Alpha_i),
                       L_d*np.sin(Phi_d)])

    L_d_vec_list.append(L_d_vec)

#Assume that the side bars do not apply any z force
#Decompose forces on bottom and top bars

F_ax_d_list = [] 
F_trans_d_list = []

for attachment in L_d_vec_list:
    F_ax_d = attachment * np.dot(F_z_d,attachment)/np.dot(attachment,attachment)
    F_trans_d = F_z_d - F_ax_d
    
    F_ax_d_list.append(F_ax_d)
    F_trans_d_list.append(F_trans_d)

print(F_ax_d_list)
#print(F_trans_d_list)

#Assume the side bars apply all the xy force
#------ Deflection for mid section



# F_x_d = P_x/3
# F_y_d = P_y/3
# F_z_d = P_z/3

# F_d = np.array([F_x_d,F_y_d,F_z_d])

# #-------- Decomposing forces


# F_ax_d[i] = 

# 
# F_per_d = F_d - F_ax_d

# F_mid = 



# M_d = np.cross(F_d ,)








# Defl_mid = (3 * E_modulus)/(L_mid**3)


# F_xy_d= (F_y_d_att**2 + F_x_d_att**2)**0.5

# F_res_d = (F_xy_d**2 + F_z_d**2)**0.5




# M_d_att = (F_z_d_att * l_u_d_att * np.cos(Phi_d_att)) + (F_xy_att * l_u_d_att * np.sin(Phi_d_att))

# print(M_d_att)
