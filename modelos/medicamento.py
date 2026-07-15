# CLASE MEDICAMENTO

class Medicamento:
    def __init__(self, nomb_med, precio, stock):
        self.id = None
        self.nomb_med = nomb_med
        self.precio = precio
        self.stock = stock

    def __str__(self):
        return f"[{self.id}] {self.nomb_med} | Precio: S/. {self.precio:.2f} | Stock: {self.stock}"
    
    
    def to_dict(self):
        return {
            "id": self.id,
            "nomb_med": self.nomb_med,
            "precio": self.precio,
            "stock": self.stock,
        }
        
    @classmethod
    def from_dict(cls,datos):
        m = cls(datos["nomb_med"], datos["precio"], datos["stock"])
        m.id = datos["id"]
        return m