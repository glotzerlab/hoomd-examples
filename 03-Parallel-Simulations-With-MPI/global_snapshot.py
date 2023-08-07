import hoomd
import numpy

# Initialize the simulation.
device = hoomd.device.CPU()
simulation = hoomd.Simulation(device=device)
simulation.create_state_from_gsd(filename='random.gsd')

# Call get_snapshot on all ranks.
snapshot = simulation.state.get_snapshot()

# Access particle data on rank 0 only.
if snapshot.communicator.rank == 0:
    total_mass = numpy.sum(snapshot.particles.mass)
    print(total_mass)
