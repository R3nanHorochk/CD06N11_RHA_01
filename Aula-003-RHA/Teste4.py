from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    data = {"mensagem": "Olá do processo 0", "valores": [1, 2, 3]}
else:
    data = None

# O processo 0 envia e os outros recebem o valor de retorno
data = comm.bcast(data, root=0)
print(f"Processo {rank} recebeu: {data}")
