from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.base_datos import inicializar
from routers import clientes, medicamentos, ventas

app = FastAPI(
    title="Sistema Integral de Gestión de Farmacia (SIGEFAR)",
    version="1.0",
    description="Mi API REST para gestión de clientes, medicamentos y ventas",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

inicializar()

app.include_router(clientes.router)
app.include_router(medicamentos.router)
app.include_router(ventas.router)


@app.get("/")
def inicio():
    return {
        "mensaje": "API Sistema Integral de Gestión de Farmacia (SIGEFAR)",
        "version": "1.0",
        "docs": "/docs"
    }