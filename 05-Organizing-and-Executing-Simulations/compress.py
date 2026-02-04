import math

import hoomd
from create_simulation import create_simulation


def compress(*jobs):
    """Compress the simjlation to the target density."""
    for job in jobs:
        communicator = hoomd.communicator.Communicator()
        simulation = create_simulation(job, communicator)

        # Read `random.gsd` from the signac job directory.
        simulation.create_state_from_gsd(filename=job.fn("random.gsd"))

        a = math.sqrt(2) / 2
        V_particle = 1 / 3 * math.sqrt(2) * a**3

        initial_box = simulation.state.box
        final_box = hoomd.Box.from_box(initial_box)

        # Set the final box volume to the volume fraction for this signac job.
        final_box.volume = (
            simulation.state.N_particles * V_particle / job.statepoint.volume_fraction
        )
        compress = hoomd.hpmc.update.QuickCompress(
            trigger=hoomd.trigger.Periodic(10), target_box=final_box
        )
        simulation.operations.updaters.append(compress)

        # Tune trial move sizes during the compression.
        periodic = hoomd.trigger.Periodic(10)
        tune = hoomd.hpmc.tune.MoveSize.scale_solver(
            moves=["a", "d"],
            target=0.2,
            trigger=periodic,
            max_translation_move=0.2,
            max_rotation_move=0.2,
        )
        simulation.operations.tuners.append(tune)

        # Compress the system to the target box size.
        while not compress.complete and simulation.timestep < 1e6:
            simulation.run(1000)

        if not compress.complete:
            message = "Compression failed to complete."
            raise RuntimeError(message)

        # Write `compressed.gsd` to the job's directory
        hoomd.write.GSD.write(
            state=simulation.state, mode="xb", filename=job.fn("compressed.gsd")
        )
        # Save the timestep that compression completed
        job.document["compressed_step"] = simulation.timestep
