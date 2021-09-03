import hoomd

communicator = hoomd.communicator.Communicator(ranks_per_partition=2)

# Pass the communicator to the device.
device = hoomd.device.CPU(communicator=communicator)
sim = hoomd.Simulation(device=device)
sim.create_state_from_gsd(filename='random.gsd')

# Set the seed based on the partition
sim.seed = communicator.partition

integrator = hoomd.md.Integrator(dt=0.005)
cell = hoomd.md.nlist.Cell()
lj = hoomd.md.pair.LJ(nlist=cell)
lj.params[('A', 'A')] = dict(epsilon=1, sigma=1)
lj.r_cut[('A', 'A')] = 2.5
integrator.forces.append(lj)
langevin = hoomd.md.methods.Langevin(kT=1.5, filter=hoomd.filter.All())
integrator.methods.append(langevin)
sim.operations.integrator = integrator

# Use the partition id in the output file name.
gsd_writer = hoomd.write.GSD(filename=f'trajectory{communicator.partition}.gsd',
                             trigger=hoomd.trigger.Periodic(1000),
                             mode='xb')
sim.operations.writers.append(gsd_writer)

sim.run(1000)
