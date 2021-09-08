import hoomd

# Initialize the system.
device = hoomd.device.CPU()
sim = hoomd.Simulation(device=device)
sim.create_state_from_gsd(filename='random.gsd')

# Print the domain decomposition.
domain_decomposition = sim.state.domain_decomposition
if device.communicator.rank == 0:
    print(domain_decomposition)

# Print the location of the split planes.
split_fractions = sim.state.domain_decomposition_split_fractions
if device.communicator.rank == 0:
    print(split_fractions)

# Print the number of particles on each rank.
with sim.state.cpu_local_snapshot as snap:
    N = len(snap.particles.position)
    print(f'{N} particles on rank {device.communicator.rank}')
