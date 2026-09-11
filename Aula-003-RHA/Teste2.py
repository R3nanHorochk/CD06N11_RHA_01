import random
import time
from mpi4py import MPI
N = 300
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
A = [[random.random() for _ in range(N)] for _ in range(N)]
B = [[random.random() for _ in range(N)] for _ in range(N)]
C = [[0]*N for _ in range(N)]
MatrizC = []
dataA = comm.bcast(A,root = 0)
dataB = comm.bcast(B,root = 0)
def calcular(inicio, fim):
    for i in range(inicio, fim):
        for j in range(N):
            for k in range(N):
                C[i][j] += A[i][k] * B[k][j]
inicio = time.time()
linhas = N // size

if rank == 0:
    inicio = time.time()
    comm.gather(MatrizC,root = 0) 
    fim = time.time()
    print(f"Tempo : {(fim - inicio) * 1000:.2f} ms")
else:
    ini = rank * linhas
    fim = N if rank == size - 1 else (rank + 1) * linhas
    MatrizC = calcular(ini,fim)
  
