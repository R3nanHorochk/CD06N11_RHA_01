import random
import threading
import time

N = 10_000_000
THREADS = 4
pontos_por_thread = N // THREADS
resultados_parciais = [0] * THREADS


def calcular_monte_carlo(indice, total_pontos):
    contagem_local = 0
    for _ in range(total_pontos):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1.0:
            contagem_local += 1
    resultados_parciais[indice] = contagem_local


inicio = time.time()

threads = []
for t in range(THREADS):
    # A última thread absorve eventuais restos de divisão
    qtd = N - (THREADS - 1) * pontos_por_thread if t == THREADS - 1 else pontos_por_thread
    th = threading.Thread(target=calcular_monte_carlo, args=(t, qtd))
    threads.append(th)
    th.start()

for th in threads:
    th.join()

total_dentro = sum(resultados_parciais)
pi_estimado = 4.0 * total_dentro / N
fim = time.time()

print(f"PI aproximado: {pi_estimado:.6f}")
print(f"Tempo com threads: {(fim - inicio) * 1000:.2f} ms")