import hoomd

communicator = hoomd.communicator.Communicator(ranks_per_partition=2)
print(f'Hello from partition {communicator.partition} rank {communicator.rank}')
