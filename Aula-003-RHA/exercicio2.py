import random
import time
from mpi4py import MPI

# Inicialização do MPI
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

N = 10_000_000

if rank == 0:
    inicio = time.time()

n_local = N // size

dentro_local = 0
for _ in range(n_local):
    x = random.random()
    y = random.random()
    if x * x + y * y <= 1.0:
        dentro_local += 1

total_dentro = comm.reduce(dentro_local, op=MPI.SUM, root=0)

if rank == 0:
    pi_estimado = 4.0 * total_dentro / (n_local * size)
    fim = time.time()
    print(f"PI aproximado: {pi_estimado:.6f}")
    print(f"Tempo distribuído MPI: {(fim - inicio) * 1000:.2f} ms")