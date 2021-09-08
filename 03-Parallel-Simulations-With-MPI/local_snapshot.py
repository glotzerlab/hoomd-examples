import hoomd

# Initialize the simulation.
device = hoomd.device.CPU()
sim = hoomd.Simulation(device=device)
sim.create_state_from_gsd(filename='random.gsd')

# Access the local snapshot.
with sim.state.cpu_local_snapshot as snapshot:
    N = len(snapshot.particles.position)

    # Double the mass of every particle.
    snapshot.particles.mass *= 2

    # Look up the index of the particle with tag 100.
    idx = snapshot.particles.rtag[100]

    # Modify the particle, but only if it is found.
    # This condition will be true on one rank and false on the others.
    if idx < N:
        snapshot.particles.mass[idx] *= 2
