from pydantic import BaseModel, field_validator

class VentaCrear(BaseModel):
    id_cliente: int
    id_medicamento: int
    cantidad: int

    @field_validator("cantidad")
    @classmethod
    def validar_cantidad(cls, valor):
        if valor <= 0:
            raise ValueError("La cantidad debe ser mayor que cero")
        return valor

class VentaRespuesta(BaseModel):
    id_venta: int
    id_cliente: int
    id_medicamento: int
    nomb_cli: str
    nomb_med: str
    cantidad: int
    fecha_venta: str
    total: float