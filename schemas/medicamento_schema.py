from pydantic import BaseModel, field_validator
from typing import Optional

class MedicamentoCrear(BaseModel):
    nomb_med: str
    precio: float
    stock: int

    @field_validator("precio")
    @classmethod
    def validar_precio(cls, valor):
        if valor <= 0:
            raise ValueError("El precio debe ser mayor que cero")
        return valor

    @field_validator("stock")
    @classmethod
    def validar_stock(cls, valor):
        if valor < 0:
            raise ValueError("El stock no puede ser negativo")
        return valor

class MedicamentoActualizar(BaseModel):
    nomb_med: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None

    @field_validator("precio")
    @classmethod
    def validar_precio(cls, valor):
        if valor is not None and valor <= 0:
            raise ValueError("El precio debe ser mayor que cero")
        return valor

    @field_validator("stock")
    @classmethod
    def validar_stock(cls, valor):
        if valor is not None and valor < 0:
            raise ValueError("El stock no puede ser negativo")
        return valor

class MedicamentoRespuesta(BaseModel):
    id_medicamento: int
    nomb_med: str
    precio: float
    stock: int