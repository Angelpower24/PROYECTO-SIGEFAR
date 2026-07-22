# CLASE VENTA

class Venta:

    def __init__(self, id_cliente, id_medicamento):
        self.id_venta = None
        self.fecha_venta = None
        self.id_cliente = id_cliente
        self.id_medicamento = id_medicamento

    def __str__(self):
        return f"[{self.id_venta}] Fecha: {self.fecha_venta} | Cliente ID: {self.id_cliente} | Medicamento ID: {self.id_medicamento}"

    def to_dict(self):
        return {
            "id_venta": self.id_venta,
            "fecha_venta": self.fecha_venta,
            "id_cliente": self.id_cliente,
            "id_medicamento": self.id_medicamento
        }

    @classmethod
    def from_dict(cls, datos):
        v = cls(datos["id_cliente"], datos["id_medicamento"])
        v.id_venta = datos["id_venta"]
        v.fecha_venta = datos["fecha_venta"]
        return v
    