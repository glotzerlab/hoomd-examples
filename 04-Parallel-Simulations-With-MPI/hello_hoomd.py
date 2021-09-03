import os

import hoomd

device = hoomd.device.CPU()
rank = device.communicator.rank
pid = os.getpid()
print(f'Hello HOOMD-blue rank {rank} from process id {pid}')
