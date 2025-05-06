import hoomd


def create_simulation(job, communicator):
    """Create a Simulation object based on the signac job."""
    cpu = hoomd.device.CPU(communicator=communicator)

    # Set the simulation seed from the state point.
    simulation = hoomd.Simulation(device=cpu, seed=job.statepoint.seed)
    mc = hoomd.hpmc.integrate.ConvexPolyhedron()
    mc.shape["octahedron"] = dict(
        vertices=[
            (-0.5, 0, 0),
            (0.5, 0, 0),
            (0, -0.5, 0),
            (0, 0.5, 0),
            (0, 0, -0.5),
            (0, 0, 0.5),
        ]
    )
    simulation.operations.integrator = mc

    return simulation
