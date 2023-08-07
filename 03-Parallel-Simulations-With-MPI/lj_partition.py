import hoomd

# kT values to execute at:
kT_values = [1.5, 2.0]

# Instantiate a Communicator with 2 ranks in each partition.
communicator = hoomd.communicator.Communicator(ranks_per_partition=2)

# Pass the communicator to the device.
device = hoomd.device.CPU(communicator=communicator)

# Initialize the simulation.
simulation = hoomd.Simulation(device=device, seed=1)
simulation.create_state_from_gsd(filename='random.gsd')

# Choose system parameters based on the partition
simulation.seed = communicator.partition
kT = kT_values[communicator.partition]

# Set the operations for a Lennard-Jones particle simulation.
integrator = hoomd.md.Integrator(dt=0.005)
cell = hoomd.md.nlist.Cell(buffer=0.4)
lj = hoomd.md.pair.LJ(nlist=cell)
lj.params[('A', 'A')] = dict(epsilon=1, sigma=1)
lj.r_cut[('A', 'A')] = 2.5
integrator.forces.append(lj)
nvt = hoomd.md.methods.ConstantVolume(
    filter=hoomd.filter.All(),
    thermostat=hoomd.md.methods.thermostats.Bussi(kT=kT))
integrator.methods.append(nvt)
simulation.operations.integrator = integrator

# Use the partition id in the output file name.
gsd_writer = hoomd.write.GSD(filename=f'trajectory{communicator.partition}.gsd',
                             trigger=hoomd.trigger.Periodic(1000),
                             mode='xb')
simulation.operations.writers.append(gsd_writer)

# Run the simulation.
simulation.run(1000)
