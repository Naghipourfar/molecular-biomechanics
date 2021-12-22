import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation


def simulate_apple_fall(total_time: float = 10, mass: float = 0.3, initial_velocity: float = -0.1, height: float = 553, timestep: float = 0.05):
    """
    Parameters
    ----------
    total_time: float

    mass: float

    initial_velocity: float

    height: float

    timestep: float
    """
    # Setup the figure and axes...
    fig, ax = plt.subplots(figsize=(8,8))

    ## Adjust axes limits according to your problem. Here we don't need more than a couple of meters left or right, and 600 meters up
    ax.set(xlim=(-2, 2), ylim=(0, height + 50), xlabel='Position, meters', ylabel='Height, meters', title='Apple falling from CN tower')

    gravity = 9.8

    # setting a timestep to be 50 ms
    # dt = 0.05 #s
    num_timesteps = int(total_time // timestep)

    # Allocating arrays for 2D problem
    v = np.zeros((num_timesteps + 1, 2))
    r = np.zeros((num_timesteps + 1, 2))
    f = np.zeros((num_timesteps + 1, 2))

    # initial conditions:
    r[0] = np.array([0., height])
    v[0] = np.array([-initial_velocity, 0.])

    # the only force is gravity
    f[:] = np.array([0., -mass * gravity])

    ## Run dynamics:
    for n in range(num_timesteps):
        v[n+1] = v[n] + f[n] / mass * timestep
        r[n+1] = r[n] + v[n+1] * timestep

    ## drawing the first data point  
    scat = ax.scatter(r[0,0], r[0,1], marker='o', c='g', s=200)

    ## animating
    def animate(i):
        scat.set_offsets(r[i])

    ani = animation.FuncAnimation(fig, func=animate, frames=num_timesteps)
    plt.close()
    ani.save('apple_fall.mp4', fps=1//timestep)


def simulate_three_particles(total_time: float = 10, mass: float = 1.0, ks: int = 5, r0: float = 1.0, timestep: float = 0.05):
    # Setup the figure and axes...
    fig, ax = plt.subplots(figsize=(6,6))
    ax.set(xlim=(-3.5, 3.5), ylim=(-3.5, 3.5), ylabel='meters', xlabel='meters', title='3-Body problem')

    # parameters of the problem
    # T = 10. #s
    # m = 1.0 #kg
    # ks = 5 #N/m
    # r0 = 1. #m

    # setting a timestep to be 50 ms
    # dt = 0.05 #s
    num_timesteps = int(total_time / timestep)

    # Allocating arrays for 2D problem: first axis - time. second axis - particle's number. third - coordinate
    v = np.zeros((num_timesteps + 1, 3, 2))
    r = np.zeros((num_timesteps + 1, 3, 2))
    f = np.zeros((num_timesteps + 1, 3, 2))

    # initial conditions for 3 particles:
    r[0,0] = np.array([0., 2.])
    r[0,1] = np.array([2., 0.])
    r[0,2] = np.array([-1., 0.])

    def compute_forces(n):
        '''The function computes forces on each pearticle at time step n'''
        for i in range(3):
            for j in range(3):
                if i != j:
                    rij = r[n, i] - r[n, j]
                    rij_abs = np.linalg.norm(rij)
                    f[n, i] -= ks * (rij_abs - r0) * rij / rij_abs 
    
    ## Run dynamics:
    for n in range(num_timesteps):
        compute_forces(n)
        v[n+1] = v[n] + f[n] / mass * timestep
        r[n+1] = r[n] + v[n+1] * timestep

    ## drawing and animating 
    scat = ax.scatter(r[0,:,0], r[0,:,1], marker='o', c=['b', 'k', 'r'], s=1000)

    def animate(i):
        scat.set_offsets(r[i])

    ani = animation.FuncAnimation(fig, animate, frames=num_timesteps)
    plt.close()
    ## this function will create a lot of *.png files in a folder '3Body_frames'
    ani.save('3particles.mp4', fps=1 // timestep)
