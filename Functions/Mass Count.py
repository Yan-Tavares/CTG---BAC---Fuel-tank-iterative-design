import math as m
import numpy as np
#import Failure_Check as fc
import WP5_ParisV2 as Paris

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

stepsize = 0.0005 
total_mass = 374-26.654 

mass_list = [0.05,0.15, 10, 3,5.65,4.54,4.25] ### Data from Yan, to be updated

def Mass_count(mass_list): #should get the mass of the attachments as a list, 5.4, talk to Yan. 
    # Iterate in 5.3, talk to Paris. 
    sum_from_list = sum(mass_list)  
    total_mass = 374-26.654 + sum_from_list
    return total_mass 
print('The inital thickness is', t1, '[m],', t1*1000, '[mm]')  

# def Check_failure(t):  
#     return fc.failure1 

# Compare t1 and t2 with internal pressure  

biggest_t1= Paris.t1 

while not Paris.Check_failure(t1)[0] and Paris.t1 >= 0: 
    if t1 < 0.001 + stepsize: 
        break 

    if Paris.t1 - stepsize > 0: 
        t1 -=  stepsize # stepsize 

    if Paris.t1 > biggest_t1:
        biggest_t1 = t1

if Paris.Check_failure(t1)[0]:
    while not Paris.Check_failure(t1)[0]: 
        t1 += stepsize # stepsize 

t1 = round(t1, 9)

print('The final thickness is', t1, '[m],' , t1*1000, '[mm]')  

print("Total mass is", Mass_count(mass_list), '[kg]') 


