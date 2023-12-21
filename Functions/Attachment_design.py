import numpy as np



def Normal_Stress(F_ax,F_trans,Length,A,I,s_max):
  Nominal_stress = F_ax/A
  Max_Bending_stress = F_trans * Length * s_max / I
  Max_Normal_stress = Nominal_stress + Max_Bending_stress
  
  return Max_Normal_stress
  

def Attachment_load_calculator(Force_vector,Att_vector_list):

  F_ax_list = []
  Abs_F_ax_list = []
  F_trans_list = []
  Abs_F_trans_list = []

  for attachment in Att_vector_list:
    F_ax = attachment * np.dot(Force_vector,attachment)/np.dot(attachment,attachment)
    F_trans = Force_vector - F_ax

    F_ax_list.append(F_ax)
    F_trans_list.append(F_trans)

    Abs_F_ax_list.append(np.linalg.norm(F_ax))
    Abs_F_trans_list.append(np.linalg.norm(F_trans))
  
  return Abs_F_ax_list, Abs_F_trans_list, F_ax_list, F_trans_list

def Minimal_variable_dimension(Rho, Sigma_yield, F_ax, F_trans, Length, Def_max_dimension, att_type):

  if att_type == "H_Cylinder":
    R_inner_stepsize = 0.0002
    R_outer = Def_max_dimension
    R_inner = Def_max_dimension - 0.001

    A = (np.pi)*(R_outer**2 - R_inner**2)
    I = (np.pi/4)*(R_outer**4 - R_inner**4)
    Sigma = Normal_Stress(F_ax,F_trans,Length,A,I,R_outer)

    print(Sigma)
    
    while Sigma_yield <= Sigma:
    
      R_inner -= R_inner_stepsize
      A = (np.pi)*(R_outer**2 - R_inner**2)
      I = (np.pi/4)*(R_outer**4 - R_inner**4)

      Sigma = Normal_Stress(F_ax,F_trans,Length,A,I,R_outer)
    
    Mass = Rho * Length * A
    return R_inner, Mass, Sigma

  if att_type == "I_Beam":
    D_inner_stepsize = 0.0002
    D_outer = Def_max_dimension
    D_inner = Def_max_dimension - 0.001
    
    A = Def_max_dimension*(Def_max_dimension - D_inner)
    I = 2* (1/12 * Def_max_dimension*(Def_max_dimension - D_inner)**3 + A * (Def_max_dimension - D_inner/2)**2)
    
    Sigma = Normal_Stress(F_ax,F_trans,Length,A,I,D_outer)

    while Sigma_yield <= Sigma:
      D_inner-= D_inner_stepsize

      A = Def_max_dimension*(Def_max_dimension - D_inner)
      I = 2* (1/12 * Def_max_dimension*(Def_max_dimension - D_inner)**3 + A * (Def_max_dimension - D_inner/2)**2)

      Sigma = Normal_Stress(F_ax,F_trans,Length,A,I,D_outer)

    Mass = Rho * Length * A
    return D_inner, Mass, Sigma

#----------------- ATTACHMENT CROSSECTION

def Attachment_design(P_x,P_y,P_z,D_outer,L,n_att,att_location,att_type):
  E_modulus = 100 * 10**9
  Sigma_yield = 1480*10**6 #Carbon Fiber - Epoxy UD
  Rho = 1.580*10**3 #Carbon Fiber - Epoxy UD

  SF_xy = 1.5
  SF_z = 1.5

  #----------------- LOADS AND SAFETY FACTOR
  P_x *= SF_xy
  P_y *= SF_xy
  P_z *= SF_z
  Alpha_P = np.arctan(P_y/P_x)


  Phi_u = np.radians(-40)
  Phi_d = np.radians(90)

  if att_location == "Upper":
    
    num_u = n_att
    Alpha_u = np.radians(360/num_u)
    F_z_u = np.array([0,0,P_z/(num_u*2)])

    L_u = L

    #----------------- CREATE ATTACHMENT VECTORS
    L_u_vec_list = []
    for i in range (num_u): #Upper attachment
      Alpha_i = i * Alpha_u
      L_u_vec = np.array([L_u*np.cos(Phi_u)*np.cos(Alpha_i),
                        L_u*np.cos(Phi_u)*np.sin(Alpha_i),
                          L_u*np.sin(Phi_u)])

      L_u_vec_list.append(L_u_vec)

    L_vec_list = L_u_vec_list

    #----------------- CALCULATE AXIAL AND TRANSVERSAL LOADS
    Abs_F_ax_list, Abs_F_trans_list, F_ax_list, F_trans_list  = Attachment_load_calculator(F_z_u,L_u_vec_list)


  if att_location == "Middle":

    num_mid = n_att
    Alpha_mid = np.radians(360/num_mid)
    F_xy_mid = np.array([P_x/(num_mid),P_y/(num_mid),0])
    
    L_mid = L

    #----------------- CREATE ATTACHMENT VECTORS
    L_mid_vec_list = []
    for i in range (num_mid): #Mid attachment
      Alpha_i = i * Alpha_mid
      L_mid_vec = np.array([L_mid*np.cos(Alpha_i),
                          L_mid*np.sin(Alpha_i),
                          0])

      L_mid_vec_list.append(L_mid_vec)

    L_vec_list = L_mid_vec_list

    #----------------- CALCULATE AXIAL AND TRANSVERSAL LOADS
    cosine_factor = 0
    Abs_F_ax_list, Abs_F_trans_list, F_ax_list, F_trans_list = Attachment_load_calculator(F_xy_mid,L_mid_vec_list)
    
    #----------------- SET DESIGN LOADS
    for i in range (num_mid):
      Alpha_i = i * Alpha_mid
      Delta_alpha = Alpha_P - Alpha_i
      
      cosine_factor += 1 - abs(np.cos(Delta_alpha))

    Abs_F_ax_list = np.array(Abs_F_ax_list)
    Abs_F_ax_list *= (1+cosine_factor)

  if att_location == "Bottom":

    num_d = n_att
    Alpha_d = np.radians(360/num_d)
    F_z_d = np.array([0,0,P_z/(num_d*2)])
    
    L_d = L

    #----------------- CREATE ATTACHMENT VECTORS
    L_d_vec_list = []
    for i in range (num_d): #Bottom attachment
      Alpha_i = i * Alpha_d
      L_d_vec = np.array([L_d*np.cos(Phi_d)*np.cos(Alpha_i),
                        L_d*np.cos(Phi_d)*np.sin(Alpha_i),
                          L_d*np.sin(Phi_d)])

      L_d_vec_list.append(L_d_vec)
    
    L_vec_list = L_d_vec_list

    #----------------- CALCULATE AXIAL AND TRANSVERSAL LOADS
    Abs_F_ax_list, Abs_F_trans_list,F_ax_list, F_trans_list = Attachment_load_calculator(F_z_d,L_d_vec_list)

  D_min, Mass_att,Sigma = Minimal_variable_dimension(Rho, Sigma_yield, max(Abs_F_ax_list), max(Abs_F_trans_list), L, D_outer, att_type)
  
  return L_vec_list,Abs_F_ax_list, Abs_F_trans_list,F_ax_list, F_trans_list, D_min, Mass_att,Sigma
  

# D_xy_max = 0.03
# L = 0.25
# P_x = 1000
# P_y = 12000 
# P_z = 7000

# L_u_vec_list, Abs_F_ax_u_list, Abs_F_trans_u_list, F_ax_u_list, F_trans_u_list , D_u_min, Mass_u_att,Sigma_u= Attachment_design(P_x ,P_y ,P_z, D_xy_max , L  , 3 ,"Upper","H_Cylinder")
# L_mid_vec_list, Abs_F_ax_mid_list, Abs_F_trans_mid_list, F_ax_mid_list, F_trans_mid_list, D_mid_min, Mass_mid_att,Sigma_mid= Attachment_design(P_x ,P_y ,P_z, D_xy_max , L  , 3 ,"Middle","H_Cylinder")
# L_d_vec_list, Abs_F_ax_d_list, Abs_F_trans_d_list, F_ax_d_list, F_trans_d_list, D_d_min, Mass_d_att,Sigma_d= Attachment_design(P_x ,P_y ,P_z, D_xy_max , L , 3 ,"Bottom","H_Cylinder")


# print("-----------------------------------------")
# print("Total reaction forces")
# print("-----------------------------------------\n")

# F_mid_total =  (np.array(F_ax_mid_list) + np.array(F_trans_mid_list)).sum(axis=0)
# F_d_total = (np.array(F_ax_d_list) + np.array(F_trans_d_list)).sum(axis=0)

# print(f"{'Result force from mid attachment : ':<35}")
# print(F_mid_total)
# print(f"{'Result force from bottom attachment : ':<35}")
# print(F_d_total, "\n")

# print("-----------------------------------------")
# print("Mid attachment properties")
# print("-----------------------------------------\n")

# print(f"{'Limit design size: ':<35}{D_xy_max:<8.5f}{'[m]':<}")
# print(f"{'Thickness: ':<35}{D_xy_max - D_mid_min:<8.5f}{'[m]':<}")
# print(f"{'Beam length: ':<35}{L:<8.5f}{'[m]':<}")
# print(f"{'Beam mass: ':<35}{ Mass_mid_att:<8.5f}{'[kg]':<}")
# print(f"{'Maximum normal stress: ':<35}{Sigma_mid*10**(-6):<8.5f}{'[Mpa]':<}")


#----------------- DEFINE THE FORCES APPLIED TO THE ATTACHMENTS


    
#Assume that the side bars do not apply any z force
#Decompose forces on bottom and top bars by dividing by number of elements

# F_ax_d_list = [] 
# Abs_F_ax_d_list = []
# F_trans_d_list = []
# Abs_F_trans_d_list = []

# for attachment in L_d_vec_list:
#   F_ax_d = attachment * np.dot(F_z_d,attachment)/np.dot(attachment,attachment)
#   F_trans_d = F_z_d - F_ax_d

#   F_ax_d_list.append(F_ax_d)
#   F_trans_d_list.append(F_trans_d)

#   Abs_F_ax_d_list.append(np.linalg.norm(F_ax_d))
#   Abs_F_trans_d_list.append(np.linalg.norm(F_trans_d))

# F_ax_u_list = []
# Abs_F_ax_u_list = []
# F_trans_u_list = []
# Abs_F_trans_u_list = []

# for attachment in L_u_vec_list:
#   F_ax_u = attachment * np.dot(F_z_u,attachment)/np.dot(attachment,attachment)
#   F_trans_u = F_z_u - F_ax_u

#   F_ax_u_list.append(F_ax_u)
#   F_trans_u_list.append(F_trans_u)

#   Abs_F_trans_u_list.append(np.linalg.norm(F_trans_u))
#   Abs_F_ax_u_list.append(np.linalg.norm(F_ax_u))

#Assume that the side bars take all the xy forces
#It is assumed that each bar will take the same force in the direction of the load
#The consequence is that the transversal stiffness is assumed to be the same as the axial
#This understimates the load taken by the attachments that are more aligned to the load
#To account for this and be conservative, each mid attachment will be designed to take all
#The axial load of the other attachments minus their load multiplied by the cosine with the angle of load application

# F_ax_mid_list= []
# F_trans_mid_list = []
# Abs_F_ax_mid_list = []
# Abs_F_trans_mid_list = []



# for attachment in L_mid_vec_list:
#   F_ax_mid = attachment * np.dot(F_x_mid,attachment)/np.dot(attachment,attachment) + attachment * np.dot(F_y_mid,attachment)/np.dot(attachment,attachment)
#   F_trans_mid = F_x_mid + F_y_mid - F_ax_mid

#   F_ax_mid_list.append(F_ax_mid)
#   F_trans_mid_list.append(F_trans_mid)
#   Abs_F_ax_mid_list.append(np.linalg.norm(F_ax_mid))
#   Abs_F_trans_mid_list.append(np.linalg.norm(F_trans_mid))


# cosine_factor = 0

# for i in range (num_mid):
#   Alpha_i = i * Alpha_mid
#   Delta_alpha = Alpha_P - Alpha_i
  
#   cosine_factor += 1 - abs(np.cos(Delta_alpha))


#----------------- Set the design loads
# F_ax_u_design = max(Abs_F_ax_u_list)
# F_trans_u_design = max(Abs_F_trans_u_list)

# F_ax_mid_design = max(Abs_F_ax_mid_list)*(1+cosine_factor)
# F_trans_mid_design = max(Abs_F_ax_mid_list)

# F_ax_d_design = max(Abs_F_ax_d_list)
# F_trans_d_design = max(Abs_F_trans_d_list)






# print("-----------------------------------------")
# print("Design loads")
# print("-----------------------------------------\n")

# print(f"{'Axial force upper att: ':<35}{F_ax_u_design:<8.0f}{'[N]':<15}{'SF:':<4}{SF_z:<}")
# print(f"{'Transversal force upper att: ':<35}{F_trans_u_design:<8.0f}{'[N]':<15}{'SF:':<4}{SF_z:<}")
# print(f"{'Axial force midle att: ':<35}{F_ax_mid_design:<8.0f}{'[N]':<15}{'SF:':<4}{SF_xy*cosine_factor:<.2f}")
# print(f"{'Transversal force midle att: ':<35}{F_trans_mid_design:<8.0f}{'[N]':<15}{'SF:':<4}{SF_xy:<}")
# print(f"{'Axial force bottom att: ':<35}{F_ax_d_design:<8.0f}{'[N]':<15}{'SF:':<4}{SF_z:<}")
# print(f"{'Transversal force bottom att: ':<35}{F_trans_d_design:<8.0f}{'[N]':<15}{'SF:':<4}{SF_z:<}", "\n")





# print("-----------------------------------------")
# print("Minimal cross section")
# print("-----------------------------------------\n")
# print("Defined maximum caractestic dimension for bending")
# print("Obtained dimension for variable")

