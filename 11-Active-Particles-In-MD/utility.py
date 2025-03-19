import numpy as np
import matplotlib.pyplot as plt

def fibonacci_sphere(num_pts, R):
    '''
    Returns points on the surface of a sphere. 
    num_pts is the number of points on the sphere.
    R is the radius of my desired mesh. 
    '''

    indices = np.arange(0, num_pts, dtype=float) + 0.5

    phi = np.arccos(1 - 2*indices/num_pts)
    theta = np.pi * (1 + 5**0.5) * indices

    x, y, z = R * np.cos(theta) * np.sin(phi), R * np.sin(theta) * np.sin(phi), R * np.cos(phi)

    return x, y, z

'''
def get_active_pos_in_spherical(num_points, radius):

    #First generate random points in spherical coords and then convert to cartesian.

    # Radii:
    r = np.random.uniform(0, radius ** (1/3), num_points) 
    
    # Polar angles (theta):
    theta = np.random.uniform(0, 2 * np.pi, num_points)
    
    # Azimuthal angles (phi):
    phi = np.arccos(2 * np.random.uniform(0, 1, num_points) - 1)
    
    # Spherical coordinates to Cartesian coordinates
    x = r * np.sin(phi) * np.cos(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(phi)

    points = np.vstack((x, y, z)).T
    
    return points
'''

def get_active_pos_A(rho, radius):
    num_points = int(rho * (radius**3))
    points = []
    for i in range(num_points):
        # Generate random points in a cube of side length 2*radius
        x = np.linspace(-radius+(sigma/2), radius-(sigma/2), num_points)
        y = np.random.uniform(-radius+(sigma/2), radius-(sigma/2), num_points)
        z = np.random.uniform(-radius+(sigma/2), radius-(sigma/2), num_points)
        
        #Calculate the distance of the points from the origin
        distances = np.sqrt(x**2 + y**2 + z**2)
        
        # Select points that lie within the sphere
        mask = distances <= radius
        selected_points = np.vstack((x[mask], y[mask], z[mask])).T
        
        # Add selected points to the list
        points.extend(selected_points)
        points = np.array(points)
    
    #points = np.array(points[:num_points]) # Trim to the desired number of points
    
    return points

def calc_tether_bond_lengths(fmin,fmax,fc1,fc0,k_b):
    '''
    Calculate parameters for tether bond length.
    This function is not optimized right now -- work needs to be done to determine how to do this the best.
    '''
    l_min = global_min_edge*fmin
    l_max = global_max_edge*fmax 
    l_c1 = global_min_edge*fc1
    l_c0 = global_max_edge*fc0

    print('shortest edge length: ', global_min_edge)
    print('longest edge length: ', global_max_edge)
    print('l_max: ',l_max)
    print('l_c0: ',l_c0)
    print('l_c1: ',l_c1)
    print('l_min: ',l_min)
    print('k_bond: ',k_b)
    
    return(l_min,l_max,l_c1,l_c0)


def find_U_tether_bond(r,tether_bond_params):
    '''
    Find total energy of the tether bond given a particular r between two particles.
    Needed to plot the tether energies.
    '''
    l_min = tether_bond_params[0]
    l_c1 = tether_bond_params[1]
    l_c0 = tether_bond_params[2]
    l_max = tether_bond_params[3]
    k_bond = tether_bond_params[4]
    
    if r > l_c0:
        U_att = (k_bond*np.exp(1/(l_c0-r))) / (l_max-r)
    elif r <= l_c0:
        U_att = 0
    
    if r < l_c1:
        U_rep = (k_bond*np.exp(1/(r-l_c1))) / (r-l_min)
    elif r >= l_c1:
        U_rep = 0
    
    U_tot = U_att + U_rep

    return(U_att, U_rep, U_tot)

def plot_tether_energies(tether_bond_params):
    '''
    Reformat U_att, U_rep, and U_tot to be plotted as a function of r
    '''
    l_min = tether_bond_params[0]
    l_c1 = tether_bond_params[1]
    l_c0 = tether_bond_params[2]
    l_max = tether_bond_params[3]
    k_bond = tether_bond_params[4]

    r_values = np.linspace(0, 2, 200)

    U_att_values = []
    U_rep_values = []
    U_tot_values = []
    for r in r_values:
        U_att, U_rep, U_tot = find_U_tether_bond(r, tether_bond_params)
        U_att_values.append(U_att)
        U_rep_values.append(U_rep)
        U_tot_values.append(U_tot)

    plt.figure(figsize=(5, 4))
    plt.plot(r_values, U_att_values, label='U_att', color='blue')
    plt.plot(r_values, U_rep_values, label='U_rep', color='red')
    plt.plot(r_values, U_tot_values, label='U_tot', color='green')
    plt.xlabel('r')
    plt.ylabel('Potential')
    plt.title('Mesh Bond Potential vs. Distance r')
    plt.legend()
    plt.gca().set_facecolor('white') 
    plt.grid(True, color='lightgrey', linestyle =':')
    plt.axvline(x=l_min, color='grey',linestyle ='--',linewidth=1,label='l_min')
    plt.axvline(x=l_max, color='grey',linestyle ='--',linewidth=1,label='l_max')
    plt.text(l_max-0.03,max(U_tot_values)+5,'l_max',color='grey')
    plt.text(l_min-0.03,max(U_tot_values)+5,'l_min',color='grey')
    plt.axvline(x=l_c0, color='grey',linestyle ='--',linewidth=1,label='l_min')
    plt.axvline(x=l_c1, color='grey',linestyle ='--',linewidth=1,label='l_max')
    plt.text(l_c0-0.03,max(U_tot_values)+5,'l_c0',color='grey')
    plt.text(l_c1-0.03,max(U_tot_values)+5,'l_c1',color='grey')
    plt.xlim(l_min-0.1,l_max+0.1)
    plt.ylim(-5,max(U_tot_values)+10)
    plt.show()
    
'''
def plot_tether_energies():
    plt.figure(figsize=(5, 4))
    plt.plot(r_values, U_att_values, label='U_att', color='blue')
    plt.plot(r_values, U_rep_values, label='U_rep', color='red')
    plt.plot(r_values, U_tot_values, label='U_tot', color='green')
    plt.xlabel('r')
    plt.ylabel('Potential')
    plt.title('Mesh Bond Potential vs. Distance r')
    plt.legend()
    plt.gca().set_facecolor('white') 
    plt.grid(True, color='lightgrey', linestyle =':')
    plt.axvline(x=l_min, color='grey',linestyle ='--',linewidth=1,label='l_min')
    plt.axvline(x=l_max, color='grey',linestyle ='--',linewidth=1,label='l_max')
    plt.text(l_max-0.03,max(U_tot_values)+5,'l_max',color='grey')
    plt.text(l_min-0.03,max(U_tot_values)+5,'l_min',color='grey')
    plt.axvline(x=l_c0, color='grey',linestyle ='--',linewidth=1,label='l_min')
    plt.axvline(x=l_c1, color='grey',linestyle ='--',linewidth=1,label='l_max')
    plt.text(l_c0-0.03,max(U_tot_values)+5,'l_c0',color='grey')
    plt.text(l_c1-0.03,max(U_tot_values)+5,'l_c1',color='grey')
    plt.xlim(l_min-0.1,l_max+0.1)
    plt.ylim(-5,max(U_tot_values)+10)
    plt.show()
'''   

def find_mesh_radius_avg_and_std(sim):
    '''
    Given: pos, a numpy.ndarray with each particles catersian coordinates:
    Outputs:
        AVGrad: average radius of flexicle if assume spherical.
        STDrad: standard deviation of mesh points from the avg radius value.
    '''   
    snap = sim.state.get_snapshot()
    pos = snap.particles.position    
    
    rad = np.zeros(len(pos))
    for j in range(len(pos)):
        for i in list([0,1,2]):
            rad[j] += pos[j][i]**2
        rad[j] = np.sqrt(rad[j])
    AVGrad = np.mean(rad)
    STDrad = np.std(rad)
    return AVGrad, STDrad
