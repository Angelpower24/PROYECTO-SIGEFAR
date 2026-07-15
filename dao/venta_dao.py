from config.logger import Logger

# EXCEPCIONES VENTA

class VentaNoEncontradaError(Exception):
    def __init__(self, venta_id):
        super().__init__(f"Venta ID={venta_id} no encontrada")
            
# DAO VENTA

class VentaDAO:
    def __init__(self):
        self.__bd = []
        self.__cid = 1
        self.__log = Logger()

    # Insertar venta

    def insertar(self, venta):
        venta.id = self.__cid
        self.__cid += 1
        self.__bd.append(venta)
        self.__log.info(f"Venta registrada ID={venta.id}")
        return venta

    # Buscar venta

    def buscar_por_id(self, venta_id):
        for v in self.__bd:
            if v.id == venta_id:
                return v
        return None
    
    # Obtener todas las ventas

    def obtener_todos(self):
        return sorted(self.__bd, key=lambda v: v.id)

    # Eliminar venta

    def eliminar(self, venta_id):
        v = self.buscar_por_id(venta_id)
        if not v:
            self.__log.error(f"Venta ID={venta_id} no encontrada")
            raise VentaNoEncontradaError(venta_id)
        self.__bd.remove(v)
        self.__log.info(f"Venta eliminada ID={venta_id}")
        return True

    # Total de ventas

    def total(self): return len(self.__bd)