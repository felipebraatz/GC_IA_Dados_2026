
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

URL_BASE = "https://www.fruityvice.com/api/fruit"


# Modelo para cadastrar um suco
class Suco(BaseModel):
    nome: str
    frutas: list[str]
    tem_gosto_de: str


# Modelo para atualizar um suco
class AtualizarSuco(BaseModel):
    frutas: list[str]


# Dicionário que armazena os sucos
sucos = {}


# Função que consulta a Fruityvice
def consultar_fruta(nome):
    try:
        resposta = requests.get(f"{URL_BASE}/{nome}", timeout=10)

        if resposta.status_code == 200:
            dados = resposta.json()

            return {
                "nome": dados["name"],
                "calorias": dados["nutritions"]["calories"],
                "acucar": dados["nutritions"]["sugar"]
            }

        elif resposta.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail=f"Fruta '{nome}' não encontrada."
            )

        else:
            raise HTTPException(
                status_code=502,
                detail="Erro ao consultar a Fruityvice."
            )

    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=503,
            detail="Erro de conexão com a Fruityvice."
        )


# GET - Consultar uma fruta
@app.get("/frutas/{nome}")
def buscar_fruta(nome: str):
    return consultar_fruta(nome)


# POST - Cadastrar um suco
@app.post("/sucos")
def cadastrar_suco(suco: Suco):

    if len(suco.frutas) == 0:
        raise HTTPException(
            status_code=400,
            detail="Informe pelo menos uma fruta."
        )

    total_calorias = 0
    total_acucar = 0

    for fruta in suco.frutas:
        dados = consultar_fruta(fruta)

        total_calorias += dados["calorias"]
        total_acucar += dados["acucar"]

    novo_id = max(sucos.keys(), default=0) + 1

    sucos[novo_id] = {
        "id": novo_id,
        "nome": suco.nome,
        "frutas": suco.frutas,
        "tem_gosto_de": suco.tem_gosto_de,
        "total_calorias": round(total_calorias, 2),
        "total_acucar": round(total_acucar, 2)
    }

    return sucos[novo_id]


# GET - Listar todos os sucos
@app.get("/sucos")
def listar_sucos():
    return list(sucos.values())


# PUT - Atualizar as frutas de um suco
@app.put("/sucos/{suco_id}")
def atualizar_suco(suco_id: int, atualizacao: AtualizarSuco):

    if suco_id not in sucos:
        raise HTTPException(
            status_code=404,
            detail="Suco não encontrado."
        )

    if len(atualizacao.frutas) == 0:
        raise HTTPException(
            status_code=400,
            detail="Informe pelo menos uma fruta."
        )

    total_calorias = 0
    total_acucar = 0

    for fruta in atualizacao.frutas:
        dados = consultar_fruta(fruta)

        total_calorias += dados["calorias"]
        total_acucar += dados["acucar"]

    sucos[suco_id]["frutas"] = atualizacao.frutas
    sucos[suco_id]["total_calorias"] = round(total_calorias, 2)
    sucos[suco_id]["total_acucar"] = round(total_acucar, 2)

    return sucos[suco_id]