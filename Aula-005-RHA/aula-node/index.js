const express = require('express');
const app = express();
const PORT = 3000;

app.use(express.json());

// Bases de dados de estoque
const produtos_estoque = {
  "1": { "nome": "Dell XPS 13", "estoque": 10 },
  "2": { "nome": "Monitor LG 29", "estoque": 5 }
};
const produtos_comerciais = {};

app.get('/api/data', (req, res) => {
  res.json({
    "mensagem": "Olá do Node.js!",
    "status": "sucesso",
    "tecnologia": "JavaScript"
  });
});

function isInvalido(id) {
  const n = Number(id);
  
  return isNaN(n) || !Number.isInteger(n) || n <= 0;
}

app.get('/estoque/:id', (req, res) => {
  const { id } = req.params;

  if (isInvalido(id)) {
    return res.status(400).json({
      "error": "INVALID_ID",
      "message": "O ID deve ser um inteiro positivo"
    });
  }

  const produto = produtos_estoque[id] || produtos_comerciais[id];
  if (!produto) {
    return res.status(404).json({ error: "NOT_FOUND", message: "Produto não encontrado no estoque" });
  }

  return res.json(produto);
});

app.get('/api/full-info/:id', async (req, res) => {
  const { id } = req.params;

  if (isInvalido(id)) {
    return res.status(400).json({
      "error": "INVALID_ID",
      "message": "O ID deve ser um inteiro positivo"
    });
  }

  const estoque = produtos_estoque[id] || produtos_comerciais[id];
  if (!estoque) {
    return res.status(404).json({ error: "NOT_FOUND", message: "Produto não encontrado no estoque local" });
  }

  try {
    const flaskRes = await fetch(`http://127.0.0.1:5000/detalhes/${id}`);
    if (!flaskRes.ok) {
      return res.status(flaskRes.status).json(await flaskRes.json());
    }
    const fiscal = await flaskRes.json();

    return res.json({
      id: id,
      nome: estoque.nome,
      estoque: estoque.estoque,
      preco: fiscal.preco,
      categoria: fiscal.categoria
    });
  } catch (error) {
    return res.status(502).json({ error: "GATEWAY_ERROR", message: "Falha ao contactar servidor Flask" });
  }
});


app.post('/cadastrar', async (req, res) => {
  const { id, nome, estoque, preco_base, categoria } = req.body;

  if (!id) {
    return res.status(400).json({ error: "INVALID_DATA", message: "ID obrigatório" });
  }

  const nomeEmCaixaAlta = String(nome).toUpperCase();

  try {
    const flaskResponse = await fetch('http://127.0.0.1:5000/fiscal/cadastrar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        id: String(id),
        preco_base: Number(preco_base),
        categoria: categoria
      })
    });

    if (flaskResponse.status === 201) {
      produtos_comerciais[String(id)] = {
        nome: nomeEmCaixaAlta,
        estoque: Number(estoque)
      };

      return res.status(201).json({
        mensagem: "Produto cadastrado com sucesso de forma distribuída",
        id: String(id),
        comercial: produtos_comerciais[String(id)]
      });
    } else {
      const erroFlask = await flaskResponse.json();
      return res.status(flaskResponse.status).json({
        error: "FLASK_REJECTED",
        detalhes: erroFlask
      });
    }
  } catch (err) {
    console.error("Erro no fetch para Flask:", err);
    return res.status(502).json({
      error: "GATEWAY_ERROR",
      message: "Falha ao sincronizar com o serviço Flask"
    });
  }
});


app.listen(PORT, () => {
  console.log(`Servidor Node rodando na porta ${PORT}`);
});