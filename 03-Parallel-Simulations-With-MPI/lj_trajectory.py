import hoomd

# Initialize the simulation.
device = hoomd.device.CPU()
simulation = hoomd.Simulation(device=device, seed=1)
simulation.create_state_from_gsd(filename='random.gsd')

# Set the operations for a Lennard-Jones particle simulation.
integrator = hoomd.md.Integrator(dt=0.005)
cell = hoomd.md.nlist.Cell(buffer=0.4)
lj = hoomd.md.pair.LJ(nlist=cell)
lj.params[('A', 'A')] = dict(epsilon=1, sigma=1)
lj.r_cut[('A', 'A')] = 2.5
integrator.forces.append(lj)
nvt = hoomd.md.methods.ConstantVolume(
    filter=hoomd.filter.All(), thermostat=hoomd.md.methods.thermostats.Bussi(kT=1.5)
)
integrator.methods.append(nvt)
simulation.operations.integrator = integrator

# Define and add the GSD operation.
gsd_writer = hoomd.write.GSD(
    filename='trajectory.gsd', trigger=hoomd.trigger.Periodic(1000), mode='xb'
)
simulation.operations.writers.append(gsd_writer)

# Run the simulation.
simulation.run(1000)
