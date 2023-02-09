import hoomd

# Initialize the simulation.
device = hoomd.device.CPU()
sim = hoomd.Simulation(device=device, seed=1)
sim.create_state_from_gsd(filename='random.gsd')

# Set the operations for a Lennard-Jones particle simulation.
integrator = hoomd.md.Integrator(dt=0.005)
cell = hoomd.md.nlist.Cell(buffer=0.4)
lj = hoomd.md.pair.LJ(nlist=cell)
lj.params[('A', 'A')] = dict(epsilon=1, sigma=1)
lj.r_cut[('A', 'A')] = 2.5
integrator.forces.append(lj)
nvt = hoomd.md.methods.ConstantVolume(
    filter=hoomd.filter.All(),
    thermostat=hoomd.md.methods.thermostats.Bussi(kT=1.5))
integrator.methods.append(nvt)
sim.operations.integrator = integrator

# Run a short time before measuring performance.
sim.run(100)

# Run the simulation and print the performance.
sim.run(1000)
device.notice(f'{sim.tps}')
