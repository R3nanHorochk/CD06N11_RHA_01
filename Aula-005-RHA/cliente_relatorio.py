import requests

def gerar_relatorio():
    item_id = input("Digite o ID do produto: ").strip()

    url_flask = f"http://localhost:5000/detalhes/{item_id}"
    url_node = f"http://localhost:3000/estoque/{item_id}"

    try:
        res_flask = requests.get(url_flask)
        res_node = requests.get(url_node)

        if res_flask.status_code == 200 and res_node.status_code == 200:
            dados_fiscais = res_flask.json()
            dados_estoque = res_node.json()

            dados_completos = {**dados_estoque, **dados_fiscais}

            print(f"ID: {item_id} | Nome: {dados_completos['nome']} | Preço: R$ {dados_completos['preco']} | Estoque: {dados_completos['estoque']}")
        else:
            print(f"Erro: Produto com ID '{item_id}' não encontrado em um ou ambos os servidores.")
            print(f"Status Flask: {res_flask.status_code} | Status Node: {res_node.status_code}")

    except requests.exceptions.ConnectionError:
        print("Erro de conexão: Verifique se ambos os servidores (Flask na porta 5000 e Node na porta 3000) estão rodando.")

if __name__ == '__main__':
    gerar_relatorio()