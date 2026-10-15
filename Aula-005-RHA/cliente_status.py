import requests

def verificar_servicos(lista_urls):
    for url in lista_urls:
        try:
            resposta = requests.get(url, timeout=3)
            if resposta.status_code == 200:
                dados = resposta.json()
                # A função trata todas as respostas de forma genérica, baseando-se apenas no contrato
                print(f"Serviço: {dados['service']} | Status: {dados['status']} | Horário: {dados['timestamp']}")
            else:
                print(f"Erro em {url}: Status HTTP {resposta.status_code}")
        except Exception as e:
            print(f"Falha ao conectar em {url}: {e}")

if __name__ == '__main__':
    urls_monitoramento = [
        "http://localhost:5000/status",
        "http://localhost:3000/status"
    ]
    verificar_servicos(urls_monitoramento)