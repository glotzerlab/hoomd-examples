import hoomd
from create_simulation import create_simulation


def randomize(*jobs):
    """Randomize the particle positions and orientations."""
    for job in jobs:
        communicator = hoomd.communicator.Communicator()
        simulation = create_simulation(job, communicator)

        # Read `lattice.gsd` from the signac job's directory.
        simulation.create_state_from_gsd(filename=job.fn("lattice.gsd"))

        # Apply trial moves to randomize the particle positions and orientations.
        simulation.run(10e3)

        # Write `random.gsd` to the signac job's directory.
        hoomd.write.GSD.write(
            state=simulation.state, mode="xb", filename=job.fn("random.gsd")
        )
