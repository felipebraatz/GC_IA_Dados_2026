# API da Casa de Sucos 🍹

Minha primeira API em Python, criada como atividade para praticar rotas, métodos HTTP, JSON e consumo de APIs.

O projeto usa **FastAPI** e consulta a API pública **Fruityvice** para obter as calorias e a quantidade de açúcar das frutas.

## Tecnologias utilizadas

- Python
- FastAPI
- Requests
- Fruityvice

## Como executar

**1.** Abra a pasta do projeto no VS Code. Os arquivos devem estar organizados assim:

```text
casa-de-sucos/
├── main.py
├── requirements.txt
└── README.md
```

**2.** No terminal, instale as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

**3.** Inicie a API:

```bash
uvicorn main:app --reload
```

**4.** Com a API em execução, abra no navegador:

http://127.0.0.1:8000/docs

Essa página é a documentação automática do FastAPI. Nela é possível testar as rotas.

## Rotas da API

| Método | Rota | O que faz |
| --- | --- | --- |
| GET | `/frutas/{nome}` | Consulta as calorias e o açúcar de uma fruta. |
| POST | `/sucos` | Cadastra um suco e calcula seus valores nutricionais. |
| GET | `/sucos` | Lista todos os sucos cadastrados. |
| PUT | `/sucos/{suco_id}` | Atualiza as frutas de um suco e refaz os cálculos. |

### Consultar uma fruta

Exemplo de endereço:

```text
http://127.0.0.1:8000/frutas/banana
```

O nome da fruta deve estar em **inglês**, como `banana`, `apple` ou `strawberry`.

### Cadastrar um suco

Na rota `POST /sucos`, envie um JSON como este:

```json
{
  "nome": "Vitamina Tropical",
  "frutas": ["banana", "strawberry"],
  "tem_gosto_de": "Tamarindo"
}
```

A API consulta as frutas na Fruityvice, soma as calorias e o açúcar e salva o suco com um ID.

### Listar os sucos

Use a rota `GET /sucos` para ver os sucos que foram cadastrados.

### Atualizar um suco (bônus)

Na rota `PUT /sucos/1`, por exemplo, envie:

```json
{
  "frutas": ["apple", "mango"]
}
```

As frutas do suco de ID 1 serão alteradas e os valores nutricionais serão calculados novamente.

## Observações

- Os valores nutricionais são calculados considerando **100 g de cada fruta**.
- Quando uma fruta não é encontrada, a API retorna o erro **404**.
- Os sucos ficam armazenados em um **dicionário na memória**. Ao reiniciar a aplicação, os cadastros são perdidos.
- É necessário ter conexão com a internet para consultar a Fruityvice.
