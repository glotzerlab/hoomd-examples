import os

import hoomd
from create_simulation import create_simulation

# Set simulation parameters.
N_EQUILIBRATION_STEPS = 200000

# Row passes the job's partition configuration and walltime via environment
# variables.
RANKS_PER_PARTITION = int(os.environ.get("ACTION_PROCESSES_PER_DIRECTORY", "1"))
CLUSTER_JOB_WALLTIME_MINUTES = int(os.environ.get("ACTION_WALLTIME_IN_MINUTES", "60"))

# Allow up to 10 minutes for Python to launch and files to be written at the end.
# You may need to increase this buffer time on HPC systems with slow filesystems.
HOOMD_RUN_WALLTIME_LIMIT_SECONDS = CLUSTER_JOB_WALLTIME_MINUTES * 60 - 600


def equilibrate(*jobs):
    # Execute N_PARTITIONS job(s) in parallel on N_PARTITIONS * RANKS_PER_PARTITION
    # MPI ranks.
    communicator = hoomd.communicator.Communicator(
        ranks_per_partition=RANKS_PER_PARTITION
    )
    job = jobs[communicator.partition]
    simulation = create_simulation(job, communicator)

    # Determine the final timestep of the equilibration process. Use the recorded value
    # of `compress_step` so that `end_step` is set consistently when continuing.
    end_step = job.document["compressed_step"] + N_EQUILIBRATION_STEPS

    # Restore tuned trial moves from a previous execution of equilibrate.
    simulation.operations.integrator.a = job.document.get("a", {})
    simulation.operations.integrator.d = job.document.get("d", {})

    # Continue from a previous `restart.gsd` or start from the end of the *compress*
    # action.
    if job.isfile("restart.gsd"):
        simulation.create_state_from_gsd(filename=job.fn("restart.gsd"))
    else:
        simulation.create_state_from_gsd(filename=job.fn("compressed.gsd"))

    # Append trajectory frames to `trajectory.gsd.in_progress`.
    gsd_writer = hoomd.write.GSD(
        filename=job.fn("trajectory.gsd.in_progress"),
        trigger=hoomd.trigger.Periodic(10_000),
        mode="ab",
    )
    simulation.operations.writers.append(gsd_writer)

    # Tune trial move sizes during the first 5,000 steps of the equilibration.
    tune = hoomd.hpmc.tune.MoveSize.scale_solver(
        moves=["a", "d"],
        target=0.2,
        trigger=hoomd.trigger.And(
            [
                hoomd.trigger.Periodic(100),
                hoomd.trigger.Before(job.document["compressed_step"] + 5_000),
            ]
        ),
    )
    simulation.operations.tuners.append(tune)

    # Run the simulation in chunks. After each call to `run` completes, continue
    # running only if the next run is expected to complete in within the allotted time.
    while simulation.timestep < end_step:
        simulation.run(min(10_000, end_step - simulation.timestep))

        if (
            simulation.device.communicator.walltime + simulation.walltime
            >= HOOMD_RUN_WALLTIME_LIMIT_SECONDS
        ):
            break

    # Save the current state of the simulation to the filesystem.
    hoomd.write.GSD.write(
        state=simulation.state, mode="wb", filename=job.fn("restart.gsd")
    )

    job.document["a"] = simulation.operations.integrator.a.to_base()
    job.document["d"] = simulation.operations.integrator.d.to_base()

    walltime = simulation.device.communicator.walltime
    simulation.device.notice(
        f"{job.id} ended on step {simulation.timestep} after {walltime} seconds"
    )

    # Row will mark the equilibrate action complete when the file `trajectory.gsd`
    # exists. To accomplish this, rename `trajectory.gsd.in_progress` when the
    # completion condition is met.
    if simulation.timestep >= end_step:
        os.rename(job.fn("trajectory.gsd.in_progress"), job.fn("trajectory.gsd"))
