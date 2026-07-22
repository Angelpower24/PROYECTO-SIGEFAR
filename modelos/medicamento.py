# CLASE MEDICAMENTO

class Medicamento:
    def __init__(self, nomb_med, precio, stock):
        self.id_medicamento = None
        self.nomb_med = nomb_med
        self.precio = precio
        self.stock = stock

    def __str__(self):
        return f"[{self.id_medicamento}] {self.nomb_med} | Precio: S/. {self.precio:.2f} | Stock: {self.stock}"
    
    
    def to_dict(self):
        return {
            "id_medicamento": self.id_medicamento,
            "nomb_med": self.nomb_med,
            "precio": self.precio,
            "stock": self.stock,
        }
        
    @classmethod
    def from_dict(cls,datos):
        m = cls(datos["nomb_med"], datos["precio"], datos["stock"])
        m.id_medicamento = datos["id_medicamento"]
        return m