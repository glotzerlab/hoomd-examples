import math

import flow
import hoomd

N_EQUIL_STEPS = 200000
WALLTIME_LIMIT = 50 * 60


def create_simulation(job):
    cpu = hoomd.device.CPU()
    sim = hoomd.Simulation(device=cpu, seed=job.statepoint.seed)
    mc = hoomd.hpmc.integrate.ConvexPolyhedron()
    mc.shape['octahedron'] = dict(vertices=[
        (-0.5, 0, 0),
        (0.5, 0, 0),
        (0, -0.5, 0),
        (0, 0.5, 0),
        (0, 0, -0.5),
        (0, 0, 0.5),
    ])
    sim.operations.integrator = mc

    return sim


@flow.FlowProject.operation
@flow.FlowProject.pre(lambda job: job.document.get('initialized', False))
@flow.FlowProject.post(lambda job: job.document.get('randomized', False))
def randomize(job):
    sim = create_simulation(job)
    sim.create_state_from_gsd(filename=job.fn('lattice.gsd'))
    sim.run(10e3)
    hoomd.write.GSD.write(state=sim.state,
                          mode='xb',
                          filename=job.fn('random.gsd'))
    job.document['randomized'] = True


@flow.FlowProject.operation
@flow.FlowProject.pre.after(randomize)
@flow.FlowProject.post(lambda job: 'compressed_step' in job.document)
def compress(job):
    sim = create_simulation(job)
    sim.create_state_from_gsd(filename=job.fn('random.gsd'))

    a = math.sqrt(2) / 2
    V_particle = 1 / 3 * math.sqrt(2) * a**3

    initial_box = sim.state.box
    final_box = hoomd.Box.from_box(initial_box)
    final_box.volume = (sim.state.N_particles * V_particle
                        / job.statepoint.volume_fraction)
    compress = hoomd.hpmc.update.QuickCompress(
        trigger=hoomd.trigger.Periodic(10), target_box=final_box)
    sim.operations.updaters.append(compress)

    periodic = hoomd.trigger.Periodic(10)
    tune = hoomd.hpmc.tune.MoveSize.scale_solver(moves=['a', 'd'],
                                                 target=0.2,
                                                 trigger=periodic,
                                                 max_translation_move=0.2,
                                                 max_rotation_move=0.2)
    sim.operations.tuners.append(tune)

    while not compress.complete and sim.timestep < 1e6:
        sim.run(1000)

    if not compress.complete:
        raise RuntimeError("Compression failed to complete")

    hoomd.write.GSD.write(state=sim.state,
                          mode='xb',
                          filename=job.fn('compressed.gsd'))
    job.document['compressed_step'] = sim.timestep


@flow.FlowProject.operation
@flow.FlowProject.pre.after(compress)
@flow.FlowProject.post(lambda job: job.document.get('timestep', 0) - job.
                       document['compressed_step'] >= N_EQUIL_STEPS)
@flow.directives(nranks=1, walltime=1)
def equilibrate(job):
    end_step = job.document['compressed_step'] + N_EQUIL_STEPS

    sim = create_simulation(job)

    sim.operations.integrator.a = job.document.get('a', {})
    sim.operations.integrator.d = job.document.get('d', {})

    if job.isfile('restart.gsd'):
        sim.create_state_from_gsd(filename=job.fn('restart.gsd'))
    else:
        sim.create_state_from_gsd(filename=job.fn('compressed.gsd'))

    gsd_writer = hoomd.write.GSD(filename=job.fn('trajectory.gsd'),
                                 trigger=hoomd.trigger.Periodic(10_000),
                                 mode='ab')
    sim.operations.writers.append(gsd_writer)

    tune = hoomd.hpmc.tune.MoveSize.scale_solver(
        moves=['a', 'd'],
        target=0.2,
        trigger=hoomd.trigger.And([
            hoomd.trigger.Periodic(100),
            hoomd.trigger.Before(job.document['compressed_step'] + 5_000)
        ]))
    sim.operations.tuners.append(tune)

    try:
        while sim.timestep < end_step:
            sim.run(min(10_000, end_step - sim.timestep))

            if (sim.device.communicator.walltime + sim.walltime >=
                    WALLTIME_LIMIT):
                break
    finally:
        hoomd.write.GSD.write(state=sim.state,
                              mode='wb',
                              filename=job.fn('restart.gsd'))

        job.document['timestep'] = sim.timestep
        job.document['a'] = sim.operations.integrator.a.to_base()
        job.document['d'] = sim.operations.integrator.d.to_base()

        if sim.device.communicator.rank == 0:
            walltime = sim.device.communicator.walltime
            print(f'{job.id} ended on step {sim.timestep} '
                  f'after {walltime} seconds')


if __name__ == '__main__':
    flow.FlowProject().main()
