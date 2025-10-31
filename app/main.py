from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from app.services import fetch_tor_ips, get_filtered_ips
from app.database import engine, SessionDep
from app import models, schemas
from app.users.routers import users_router, verify_token
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TOR IP Filter API",
    description="Uma API para buscar, excluir e filtrar IPs da rede TOR.",
    version="1.0.0",
)
seguranca_jwt = [{"HTTPBearer": []}]
app.include_router(users_router)

@app.get("/tor-ips", tags=["IPs"], openapi_extra={"security": seguranca_jwt})
def get_tor_ips(user_info: dict = Depends(verify_token)):
    """
    Busca e retorna a lista completa de IPs de saída da rede TOR.
    """
    return fetch_tor_ips()


@app.post("/exclude-ip", tags=["Exclusão"])
def exclude_ip(ip: schemas.ExcludeIP, session: SessionDep, user_info: dict = Depends(verify_token)):
    """
    Adiciona um endereço IP à lista de exclusão.
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
def get_filtered_tor_ips(session: SessionDep, user_info: dict = Depends(verify_token)):
    """
    Retorna a lista de IPs da rede TOR, removendo quaisquer IPs
    que estejam na lista de exclusão do banco de dados.
    """
    return get_filtered_ips(session)


