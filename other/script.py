import hoomd
import hoomd.md

hoomd.context.initialize()
kT = float(hoomd.option.get_user()[0])

system = hoomd.init.create_lattice(unitcell=hoomd.lattice.sc(a=2.0), n=5)
nl = hoomd.md.nlist.cell()
lj = hoomd.md.pair.lj(r_cut=3.0, nlist=nl)
lj.pair_coeff.set('A', 'A', epsilon=1.0, sigma=1.0)
all = hoomd.group.all();
hoomd.md.integrate.mode_standard(dt=0.001)
hoomd.md.integrate.langevin(group=all, kT=kT, seed=987)

hoomd.run(10000)
