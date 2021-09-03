import hoomd

device = hoomd.device.CPU()
sim = hoomd.Simulation(device=device)
sim.create_state_from_gsd(filename='random.gsd')

with sim.state.cpu_local_snapshot as snapshot:
    N = len(snapshot.particles.position)

    # double the mass of every particle
    snapshot.particles.mass *= 2

    # look up the index of the particle with tag 100
    idx = snapshot.particles.rtag[100]

    # modify the particle, but only if it is found on our rank
    if idx < N:
        snapshot.particles.mass[idx] *= 2
