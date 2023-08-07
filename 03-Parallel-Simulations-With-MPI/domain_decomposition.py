import hoomd

# Initialize the system.
device = hoomd.device.CPU()
simulation = hoomd.Simulation(device=device)
simulation.create_state_from_gsd(filename='random.gsd')

# Print the domain decomposition.
domain_decomposition = simulation.state.domain_decomposition
device.notice(f'domain_decomposition={domain_decomposition}')

# Print the location of the split planes.
split_fractions = simulation.state.domain_decomposition_split_fractions
device.notice(f'split_fractions={split_fractions}')

# Print the number of particles on each rank.
with simulation.state.cpu_local_snapshot as snap:
    N = len(snap.particles.position)
    print(f'{N} particles on rank {device.communicator.rank}')
