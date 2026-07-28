import re
from pydantic import BaseModel, field_validator
from typing import Optional

class ClienteCrear(BaseModel):
    nomb_cli: str
    ape_cli: str
    dni: str
    telefono: str

    @field_validator("dni")
    @classmethod
    def validar_dni(cls, valor):
        if not re.fullmatch(r"\d{8}", valor):
            raise ValueError("El DNI debe tener exactamente 8 dígitos numéricos")
        return valor

class ClienteActualizar(BaseModel):
    nomb_cli: Optional[str] = None
    ape_cli: Optional[str] = None
    telefono: Optional[str] = None

class ClienteRespuesta(BaseModel):
    id_cliente: int
    nomb_cli: str
    ape_cli: str
    dni: str
    telefono: str