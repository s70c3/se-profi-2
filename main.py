from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from typing import List, Dict

app = FastAPI()

# Создание базы данных
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost/vm_logs"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Модель для запроса на создание виртуальной машины
class VirtualMachineRequest(Base):
    __tablename__ = "vm_requests"

    id = Column(Integer, primary_key=True, index=True)
    size = Column(Integer)
    task = Column(String)

# Модель для учета утилизации серверов
class ServerUtilization(Base):
    __tablename__ = "server_utilization"

    id = Column(Integer, primary_key=True, index=True)
    server_id = Column(Integer)
    utilization = Column(Float)

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

def get_servers_utilization() -> List[Dict[str, float]]:
    db = SessionLocal()
    servers_utilization = db.query(ServerUtilization).all()
    db.close()
    return [{"server_id": server.server_id, "utilization": server.utilization} for server in servers_utilization]

def get_server_utilization(server_id: int) -> Dict[str, float]:
    db = SessionLocal()
    server_utilization = db.query(ServerUtilization).filter(ServerUtilization.server_id == server_id).first()
    db.close()
    if not server_utilization:
        raise HTTPException(status_code=404, detail="Server utilization not found")
    return {"server_id": server_utilization.server_id, "utilization": server_utilization.utilization}

def is_memory_available(size: int) -> bool:
    # Проверяем, достаточно ли памяти на сервере для размещения виртуальной машины
    return any(server["memory"] - server["utilization"] >= size for server in get_servers_utilization())

@app.post("/create_vm/")
async def create_vm(vm_request: VirtualMachineRequest):
    # Проверяем, достаточно ли памяти на сервере для создания виртуальной машины
    if not is_memory_available(vm_request.size):
        raise HTTPException(status_code=400, detail="Not enough memory on the server")

    # Выбираем сервер с наименьшей загрузкой
    target_server = min(get_servers_utilization(), key=lambda x: x["utilization"])

    # Обновляем утилизацию выбранного сервера
    db = SessionLocal()
    server_utilization = db.query(ServerUtilization).filter(ServerUtilization.server_id == target_server["server_id"]).first()
    server_utilization.utilization += vm_request.size
    db.commit()
    db.close()

    return {"result": "OK", "host_id": target_server["server_id"]}

@app.get("/servers_utilization/")
async def read_servers_utilization():
    return get_servers_utilization()

@app.get("/server_utilization/{server_id}")
async def read_server_utilization(server_id: int):
    return get_server_utilization(server_id)
