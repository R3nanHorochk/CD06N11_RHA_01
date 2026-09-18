import random
import time
from mpi4py import MPI

N = 1000
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

A = None
B = None

if rank == 0:
    inicio = time.time()
    A = [[random.random() for _ in range(N)] for _ in range(N)]
    B = [[random.random() for _ in range(N)] for _ in range(N)]

A = comm.bcast(A, root=0)
B = comm.bcast(B, root=0)

linhas = N // size
ini = rank * linhas
if rank == size - 1:
    fim = N
else:
    fim = (rank + 1) * linhas

fatia_local = []

for i in range(ini, fim):
    linha_c = [0.0] * N
    for j in range(N):
        soma = 0.0
        for k in range(N):
            soma += A[i][k] * B[k][j]
        linha_c[j] = soma
    fatia_local.append(linha_c)

pedacos_coletados = comm.gather(fatia_local, root=0)

if rank == 0:
    C = []
    for pedaco in pedacos_coletados:
        for linha in pedaco:
            C.append(linha)
    fim_tempo = time.time()
    print(f"Tempo distribuído MPI: {(fim_tempo - inicio) * 1000:.2f} ms")