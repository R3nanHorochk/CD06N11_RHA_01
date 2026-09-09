from mpi4py import MPI
import random

# Inicialização do MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Função para gerar logs simulados
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
    # 200 adicionado para simular requisições bem-sucedidas
    status = ["200", "200", "200", "404", "500"]
    logs = []
    
    for _ in range(qtd):
        ip = random.choice(ips)
        metodo = random.choice(metodos)
        endpoint = random.choice(endpoints)
        st = random.choice(status)
        # Correção: Adicionado o f antes das aspas
        log_string = f"{ip} {metodo} {endpoint} {st}"
        logs.append(log_string)
        
    return logs

# Processo 0 gera o dataset
logs_divididos = None
TOTAL_LOGS = 100  # Ajuste para 100000 conforme o enunciado

if rank == 0:
    print("\nGerando dataset de logs...\n")
    logs = gerar_logs(TOTAL_LOGS)
    
    # Divisão do dataset em fatias iguais entre os processos
    chunk_size = len(logs) // size
    logs_divididos = []

    for i in range(size):
        inicio = i * chunk_size
        fim = inicio + chunk_size
        fatia = logs[inicio:fim]
        logs_divididos.append(fatia)

# Distribuição usando Scatter
logs_locais = comm.scatter(logs_divididos, root=0)

# Processamento local em cada nó
erros = 0
for linha in logs_locais:
    partes = linha.split()
    st = partes[3]
    if st in ("404", "500"):
        erros += 1

# Mensagem formatada conforme o roteiro
mensagem = f"Processo {rank} analisou {len(logs_locais)} linhas e encontrou {erros} erros."

# Exibição no Nó Master
if rank != 0:
    # Workers enviam seus resultados formatados para o Master
    comm.send(mensagem, dest=0, tag=rank)
else:
    # Master imprime o próprio resultado
    print(mensagem)
    
    # Master recebe e imprime o resultado de cada worker em ordem
    for worker in range(1, size):
        msg_recebida = comm.recv(source=worker, tag=worker)
        print(msg_recebida)