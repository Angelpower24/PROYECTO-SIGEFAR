# CLASE CLIENTE

class Cliente:
    def __init__(self, nomb_cli, ape_cli, dni, telefono):
        self.id = None
        self.nomb_cli = nomb_cli
        self.ape_cli = ape_cli
        self.dni = dni
        self.telefono = telefono

    def __str__(self):
        return f"[{self.id}] {self.nomb_cli} | {self.ape_cli} | DNI: {self.dni} | Teléfono: {self.telefono}"
        
    def to_dict(self):
        return {
            "id": self.id,
            "nomb_cli": self.nomb_cli,
            "ape_cli": self.ape_cli,
            "dni": self.dni,
            "telefono": self.telefono,
        }
        
    @classmethod
    def from_dict(cls,datos):
        c = cls(datos["nomb_cli"], datos["ape_cli"], datos["dni"], datos["telefono"])
        c.id = datos["id"]
        return c