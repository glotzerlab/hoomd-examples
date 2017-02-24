import hoomd
import hoomd.md

# initialize
hoomd.context.initialize()
kT = float(hoomd.option.get_user()[0])

# specify potential
nl = hoomd.md.nlist.cell()
lj = hoomd.md.pair.lj(r_cut=2.5, nlist=nl)
lj.pair_coeff.set('A', 'A', epsilon=1.0, sigma=1.0)

# define integrator
all = hoomd.group.all();
hoomd.md.integrate.mode_standard(dt=0.005)
hoomd.md.integrate.langevin(group=all, kT=kT, seed=42)

# write output
hoomd.analyze.log(filename="log-output.log", quantities=['potential_energy'], period=100, overwrite=True)
hoomd.dump.gsd("trajectory.gsd", period=2e3, group=all, overwrite=True)

# run simulation
hoomd.run(1e4)
