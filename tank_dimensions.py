import math

#Constants
R       = 0.3                    #tank radius, [m]
L       = 0.3 + 2 * R                  #tank length, [m]
nu      = 1/3                    #Poisson's ratio
SF      = 2                      #safety factor 2 as in Intro to Aero II
p_int   = 30 * 10**5             #internal pressure of tank, [Pa]
Y       = 1                      #some constant or whatever from the Materials book

#Material properties
Ti6Al4V = ["Ti-6Al-4V Titanium Alloy","metal",786*10**6,4450,84*10**6,25.2] #material name, material class, yield strength [Pa]
A286 = ["A286 Stainless Steel","metal",590*10**6,7980,180*10**6,9.51]       #density [kg/m^3], fracture toughness [Pa*m^0.5], price [€/kg]
AISI3140 = ["3140 Low Alloy Steel","metal",380*10**6,7900,77*10**6,1.61]
Al2219 = ["2219 Aluminium Alloy","metal",421*10**6,2870,20.9*10**6,4.17]
#Al2024 = ["2024 Aluminium Alloy", "metal",317*10**6,2780,37*10**6,4.03]
#Al7075  = ["7075 Aluminium Alloy","metal",460*10**6,2830,26.6*10**6,7.48]
Material_list = [Ti6Al4V, A286, AISI3140, Al2219]                           #from: ArianeGroup, material chart, material chart, ArianeGroup

for Material in Material_list:
    #Material properties of current material
    type_identifier = Material[1]
    Sigma_y = Material[2]
    rho = Material[3]
    K_1c = Material[4]
    price = Material[5]

    #Iterated variables
    t_cylinder = 0.01 * 10**(-3)     #[m]
    t_max      = 5 * 10**(-3)        #[m]
    dt         = 0.01 * 10**(-3)     #[m]

    Sigma_max  = 10**9        #just some very high value to start the loop, [Pa]

    while Sigma_max > Sigma_y:
    
        t_sphere = ((1 - nu) / (2 - nu)) * t_cylinder

        c_lim = min(t_cylinder, t_sphere)           #maximum crack size = thinnest thickness (leak-before-break)

        #Check stresses
        Sigma_circ   = (SF * p_int * R) / (t_cylinder)
        Sigma_long   = (SF * p_int * R) / (2 * t_cylinder)
        p_max_1 = (t_cylinder * K_1c) / (R * math.sqrt(math.pi * c_lim)) #yield-before-break condition to avoid explosions        
        
        Sigma_sphere = (SF * p_int * R) / (2 * t_sphere)
        p_max_2 = (t_sphere * K_1c) / (R * math.sqrt(math.pi * c_lim))   #yield-before-break condition to avoid explosions

        p_max_3 = (K_1c**2) / (Y**2 * R * math.pi * Sigma_y)             #leak-before-break condition to avoid explosions

        Sigma_max = max(Sigma_circ, Sigma_long, Sigma_sphere)
        p_max = max(p_max_1, p_max_2, p_max_3)
        
        if Sigma_max > Sigma_y or p_int > p_max:
            t_cylinder = t_cylinder + dt

    mass = rho * (2 * math.pi * R * t_cylinder * (L - 2*R) + 4/3 * math.pi * (R**3 - (R - t_sphere)**3))
    cost = mass * price
    
    print("t_ratio = ",(t_sphere/t_cylinder)) #should be about 0.4

    print(f"{' Material: ':<50}{Material[0]:<12}{'':<}")
    print(f"{' t_sphere: ':<50}{t_sphere*10**3:<12.3f}{'[mm]':<}")
    print(f"{' t_cylinder: ':<50}{t_cylinder*10**3:<12.3f}{'[mm]':<}")
    print(f"{' Tank mass: ':<50}{mass:<12.3f}{'[kg]':<}")
    print(f"{' Tank cost: ':<50}{cost:<12.3f}{'[€]':<}","\n")
        
