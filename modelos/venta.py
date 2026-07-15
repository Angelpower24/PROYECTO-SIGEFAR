# CLASE VENTA

class Venta:
    def __init__(self, fecha_venta, id_cliente, id_medicamento):
        self.id = None
        self.fecha_venta    = fecha_venta
        self.id_cliente     = id_cliente
        self.id_medicamento = id_medicamento

    def __str__(self):
        return f"[{self.id}] Fecha: {self.fecha_venta} | Cliente ID: {self.id_cliente} | Medicamento ID: {self.id_medicamento}"
    
    
    def to_dict(self):
        return {
            "id": self.id,
            "fecha_venta": self.fecha_venta,
            "id_cliente": self.id_cliente,
            "id_medicamento": self.id_medicamento,
        }
        
    @classmethod
    def from_dict(cls,datos):
        v = cls(datos["fecha_venta"], datos["id_cliente"], datos["id_medicamento"])
        v.id = datos["id"]
        return v