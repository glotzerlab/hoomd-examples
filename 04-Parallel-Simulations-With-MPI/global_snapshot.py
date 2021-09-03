import hoomd
import numpy

device = hoomd.device.CPU()
sim = hoomd.Simulation(device=device)
sim.create_state_from_gsd(filename='random.gsd')

snapshot = sim.state.get_snapshot()

# can only access particle data on rank 0
if snapshot.communicator.rank == 0:
    total_mass = numpy.sum(snapshot.particles.mass)
    print(total_mass)
