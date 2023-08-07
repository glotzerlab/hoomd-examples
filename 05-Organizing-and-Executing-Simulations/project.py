import math

import flow
import hoomd

# parameters
N_RANKS = 2
N_EQUIL_STEPS = 200000
CLUSTER_JOB_WALLTIME = 1
HOOMD_RUN_WALLTIME_LIMIT = CLUSTER_JOB_WALLTIME * 3600 - 10 * 60


def create_simulation(job):
    cpu = hoomd.device.CPU()
    simulation = hoomd.Simulation(device=cpu, seed=job.statepoint.seed)
    mc = hoomd.hpmc.integrate.ConvexPolyhedron()
    mc.shape['octahedron'] = dict(vertices=[
        (-0.5, 0, 0),
        (0.5, 0, 0),
        (0, -0.5, 0),
        (0, 0.5, 0),
        (0, 0, -0.5),
        (0, 0, 0.5),
    ])
    simulation.operations.integrator = mc

    return simulation


class Project(flow.FlowProject):
    pass


@Project.pre.true('initialized')
@Project.post.true('randomized')
@Project.operation
def randomize(job):
    simulation = create_simulation(job)
    simulation.create_state_from_gsd(filename=job.fn('lattice.gsd'))
    simulation.run(10e3)
    hoomd.write.GSD.write(state=simulation.state,
                          mode='xb',
                          filename=job.fn('random.gsd'))
    job.document['randomized'] = True


@Project.pre.after(randomize)
@Project.post.true('compressed_step')
@Project.operation
def compress(job):
    simulation = create_simulation(job)
    simulation.create_state_from_gsd(filename=job.fn('random.gsd'))

    a = math.sqrt(2) / 2
    V_particle = 1 / 3 * math.sqrt(2) * a**3

    initial_box = simulation.state.box
    final_box = hoomd.Box.from_box(initial_box)
    final_box.volume = (simulation.state.N_particles * V_particle
                        / job.statepoint.volume_fraction)
    compress = hoomd.hpmc.update.QuickCompress(
        trigger=hoomd.trigger.Periodic(10), target_box=final_box)
    simulation.operations.updaters.append(compress)

    periodic = hoomd.trigger.Periodic(10)
    tune = hoomd.hpmc.tune.MoveSize.scale_solver(moves=['a', 'd'],
                                                 target=0.2,
                                                 trigger=periodic,
                                                 max_translation_move=0.2,
                                                 max_rotation_move=0.2)
    simulation.operations.tuners.append(tune)

    while not compress.complete and simulation.timestep < 1e6:
        simulation.run(1000)

    if not compress.complete:
        raise RuntimeError("Compression failed to complete")

    hoomd.write.GSD.write(state=simulation.state,
                          mode='xb',
                          filename=job.fn('compressed.gsd'))
    job.document['compressed_step'] = simulation.timestep


@Project.pre.after(compress)
@Project.post(lambda job: job.document.get('timestep', 0) - job.document[
    'compressed_step'] >= N_EQUIL_STEPS)
# Cluster job directives.
@Project.operation(
    directives=dict(nranks=N_RANKS, walltime=CLUSTER_JOB_WALLTIME))
def equilibrate(job):
    end_step = job.document['compressed_step'] + N_EQUIL_STEPS

    simulation = create_simulation(job)

    simulation.operations.integrator.a = job.document.get('a', {})
    simulation.operations.integrator.d = job.document.get('d', {})

    if job.isfile('restart.gsd'):
        simulation.create_state_from_gsd(filename=job.fn('restart.gsd'))
    else:
        simulation.create_state_from_gsd(filename=job.fn('compressed.gsd'))

    gsd_writer = hoomd.write.GSD(filename=job.fn('trajectory.gsd'),
                                 trigger=hoomd.trigger.Periodic(10_000),
                                 mode='ab')
    simulation.operations.writers.append(gsd_writer)

    tune = hoomd.hpmc.tune.MoveSize.scale_solver(
        moves=['a', 'd'],
        target=0.2,
        trigger=hoomd.trigger.And([
            hoomd.trigger.Periodic(100),
            hoomd.trigger.Before(job.document['compressed_step'] + 5_000)
        ]))
    simulation.operations.tuners.append(tune)

    try:
        while simulation.timestep < end_step:
            simulation.run(min(100_000, end_step - simulation.timestep))

            if (simulation.device.communicator.walltime + simulation.walltime
                    >= HOOMD_RUN_WALLTIME_LIMIT):
                break
    finally:
        hoomd.write.GSD.write(state=simulation.state,
                              mode='wb',
                              filename=job.fn('restart.gsd'))

        job.document['timestep'] = simulation.timestep
        job.document['a'] = simulation.operations.integrator.a.to_base()
        job.document['d'] = simulation.operations.integrator.d.to_base()

        walltime = simulation.device.communicator.walltime
        simulation.device.notice(
            f'{job.id} ended on step {simulation.timestep} '
            f'after {walltime} seconds')


# Entrypoint.
if __name__ == '__main__':
    Project().main()
