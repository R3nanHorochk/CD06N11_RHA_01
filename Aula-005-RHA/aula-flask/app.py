from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

produtos_fiscais = {
    "1": {"preco": 2500.0, "categoria": "Laptops"},
    "2": {"preco": 1200.0, "categoria": "Monitores"}
}
produtos_tecnicos = {}

def id_invalido(id_str):
    """Retorna True se o ID contiver letras/símbolos ou for menor/igual a zero."""
    if not id_str.isdigit():
        return True
    return int(id_str) <= 0

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({
        "mensagem": "Olá do Flask!",
        "status": "sucesso",
        "tecnologia": "Python"
    })

@app.route('/detalhes/<id>', methods=['GET'])
def get_detalhes(id):
    if id_invalido(id):
        return jsonify({
            "error": "INVALID_ID",
            "message": "O ID deve ser um inteiro positivo"
        }), 400

    produto = produtos_fiscais.get(str(id)) or produtos_tecnicos.get(str(id))
    if not produto:
        return jsonify({"error": "NOT_FOUND", "message": "Produto fiscal não encontrado"}), 404
        
    return jsonify(produto), 200

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({
        "service": "Flask-Fiscal",
        "status": "online",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }), 200

@app.route('/fiscal/cadastrar', methods=['POST'])
def cadastrar_fiscal():
    dados = request.get_json() or {}
    item_id = str(dados.get("id"))
    preco_base = float(dados.get("preco_base", 0.0))
    categoria = dados.get("categoria", "")

    # Cálculo fiscal: 20% de imposto
    preco_calculado = round(preco_base * 1.20, 2)
    produtos_tecnicos[item_id] = {
        "preco": preco_calculado,
        "categoria": categoria
    }

    return jsonify({
        "mensagem": "Registro fiscal criado com sucesso",
        "id": item_id,
        "dados": produtos_tecnicos[item_id]
    }), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)