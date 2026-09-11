from mpi4py import MPI
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# -------------------------------------------------------------------------
# STEP 1: Broadcast configuration from root (Rank 0) to all processes
# -------------------------------------------------------------------------
if rank == 0:
    # Root defines the multiplier or task config
    config = {"multiplier": 5, "description": "Parallel Matrix Scaling"}
    print(f"[Rank 0] Broadcasting config: {config}\n")
else:
    config = None

# All processes receive the config dictionary
config = comm.bcast(config, root=0)


# -------------------------------------------------------------------------
# STEP 2: Local computation using the broadcasted data
# -------------------------------------------------------------------------
# Each process performs its own task using the shared config parameter
my_factor = config["multiplier"]
local_result = rank * my_factor

print(f"Process {rank} computed: {rank} * {my_factor} = {local_result}")


# -------------------------------------------------------------------------
# STEP 3: Gather all individual results back to the root (Rank 0)
# -------------------------------------------------------------------------
# Ensure all processes have finished printing for cleaner output
comm.Barrier() 

# Collect local_result from every process into a list on Rank 0
all_results = comm.gather(local_result, root=0)


# -------------------------------------------------------------------------
# STEP 4: Root processes the collected data
# -------------------------------------------------------------------------
if rank == 0:
    print(f"\n[Rank 0] All results gathered: {all_results}")
    print(f"[Rank 0] Final Sum: {sum(all_results)}")
