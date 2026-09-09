from mpi4py import MPI
import random

# Inicialização do MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Função para gerar logs

def gerar_logs(qtd):
    ips = [f"192.168.1.{i}" for i in range(2, 254)]
    endpoints = [
        "/",
        "/login",
        "/products",
        "/cart",
        "/checkout",
        "/api/users",
        "/api/orders"
    ]
    metodos = ["GET", "POST"]
    status = ["200", "200", "200","404", "500"]
    logs = []
    
    for i in range(qtd):
        ip = random.choice(ips)
        metodo = random.choice(metodos)
        endpoint = random.choice(endpoints)
        st = random.choice(status)
        linha_log = f"{ip} {metodo} {endpoint} {st}"
        logs.append(linha_log)
        
    return logs

logs_divididos = None
TOTAL_LOGS = 100000

if rank == 0:
    print("\nGerando dataset de logs...\n")
    logs = gerar_logs(TOTAL_LOGS)
    
    chunk = TOTAL_LOGS // size
    chunk_size = len(logs) // size
    logs_divididos = []

    for i in range(size):
        inicio = i * chunk_size
        fim = inicio + chunk_size
        fatia = logs[inicio:fim]
        logs_divididos.append(fatia)

logs_locais = comm.scatter(logs_divididos, root=0)

erros = 0
for i in logs_locais:
    linha = i.split()
    st = linha[3]
    if st in ("404", "500"):
        erros += 1

mensagem = f"Processo {rank} analisou {len(logs_locais)} linhas e encontrou {erros} erros."

# Filho
if rank != 0:
    comm.send(mensagem, dest=0, tag=rank)
# Master
else:
    print(mensagem)
    for worker in range(1, size):
        msg_recebida = comm.recv(source=worker, tag=worker)
        print(msg_recebida)