import hoomd

# kT values to execute at:
kT_values = [1.5, 2.0]

# Instantiate a Communicator with 2 ranks in each partition.
communicator = hoomd.communicator.Communicator(ranks_per_partition=2)

# Pass the communicator to the device.
device = hoomd.device.CPU(communicator=communicator)

# Initialize the simulation.
sim = hoomd.Simulation(device=device)
sim.create_state_from_gsd(filename='random.gsd')

# Choose system parameters based on the partition
sim.seed = communicator.partition
kT = kT_values[communicator.partition]

# Set the operations for a Lennard-Jones particle simulation.
integrator = hoomd.md.Integrator(dt=0.005)
cell = hoomd.md.nlist.Cell(buffer=0.4)
lj = hoomd.md.pair.LJ(nlist=cell)
lj.params[('A', 'A')] = dict(epsilon=1, sigma=1)
lj.r_cut[('A', 'A')] = 2.5
integrator.forces.append(lj)
langevin = hoomd.md.methods.Langevin(kT=kT, filter=hoomd.filter.All())
integrator.methods.append(langevin)
sim.operations.integrator = integrator

# Use the partition id in the output file name.
gsd_writer = hoomd.write.GSD(filename=f'trajectory{communicator.partition}.gsd',
                             trigger=hoomd.trigger.Periodic(1000),
                             mode='xb')
sim.operations.writers.append(gsd_writer)

# Run the simulation.
sim.run(1000)
