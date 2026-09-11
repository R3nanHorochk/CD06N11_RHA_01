from mpi4py import MPI

# Initialize the default communicator, rank, and size
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Each process calculates its own unique data
# For example, squaring its own process rank
local_data = rank 
print(f"Process {rank} generated local data: {local_data}")

# Gather data from all processes onto the root process (Rank 0)
# All ranks must execute this line!
gathered_data = comm.gather(local_data, root=0)

# Only the root process receives the compiled list
if rank == 0:
    print(f"\n[Root Process {rank}] successfully gathered all results!")
    print(f"Final List: {gathered_data}")
else:
    # On non-root processes, gathered_data evaluates to None
    assert gathered_data is None
