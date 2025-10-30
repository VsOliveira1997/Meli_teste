from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.services import fetch_tor_ips, get_filtered_ips
from app.database import engine, SessionDep
from app import models, schemas

models.Base.metadata.create_all(bind=engine)

# Você pode adicionar metadados gerais para a API
app = FastAPI(
    title="TOR IP Filter API",
    description="Uma API para buscar, excluir e filtrar IPs da rede TOR.",
    version="1.0.0",
)


# Use 'tags' para agrupar endpoints na documentação
@app.get("/tor-ips", tags=["IPs"])
def get_tor_ips():
    """
    Busca e retorna a lista completa de IPs de saída da rede TOR.
    """
    return fetch_tor_ips()


@app.post("/exclude-ip", tags=["Exclusão"])
def exclude_ip(ip: schemas.ExcludeIP, session: SessionDep):
    """
    Adiciona um endereço IP à lista de exclusão.

    - **ip**: O IP a ser excluído.

    Retorna uma mensagem de sucesso ou um erro se o IP já existir.
    """
    try:
        db_ip = models.ExcludedIP(ip=ip.ip)
        session.add(db_ip)
        session.commit()
        session.refresh(db_ip)
        return {"message": f"IP {ip.ip} excluído com sucesso"}
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="IP já está na lista de exclusão")


@app.get("/filtered-tor-ips", tags=["IPs"])
def get_filtered_tor_ips(session: SessionDep):
    """
    Retorna a lista de IPs da rede TOR, removendo quaisquer IPs
    que estejam na lista de exclusão do banco de dados.
    """
    return get_filtered_ips(session)