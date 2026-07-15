from config.logger import Logger

# EXCEPCIONES MEDICAMENTO

class MedicamentoNoEncontradoError(Exception):
    def __init__(self, medicamento_id):
        super().__init__(f"Medicamento ID={medicamento_id} no encontrado")
               
# DAO MEDICAMENTO

class MedicamentoDAO:
    def __init__(self):
        self.__bd = []
        self.__cid = 1
        self.__log = Logger()

    # Insertar medicamento

    def insertar(self, medicamento):
        medicamento.id = self.__cid
        self.__cid += 1
        self.__bd.append(medicamento)
        self.__log.info(f"Medicamento agregado: {medicamento.nomb_med}")
        return medicamento

    # Buscar por ID

    def buscar_por_id(self, medicamento_id):
        for m in self.__bd:
            if m.id == medicamento_id:
                return m
        return None
    
    # Obtener todos

    def obtener_todos(self):
        return sorted(self.__bd, key=lambda m: m.nomb_med)

    # Actualizar medicamento

    def actualizar(self,medicamento_id,nomb_med=None,precio=None,stock=None):
        m = self.buscar_por_id(medicamento_id)
        if not m:
            self.__log.error(f"Medicamento ID={medicamento_id} no encontrado")
            raise MedicamentoNoEncontradoError(medicamento_id)
        if nomb_med:           m.nomb_med = nomb_med
        if precio is not None: m.precio   = precio
        if stock is not None:  m.stock    = stock
        self.__log.info(f"Medicamento actualizado ID={medicamento_id}")
        return m

    # Eliminar medicamento

    def eliminar(self, medicamento_id):
        m = self.buscar_por_id(medicamento_id)
        if not m:
            self.__log.error(f"Medicamento ID={medicamento_id} no encontrado")
            raise MedicamentoNoEncontradoError(medicamento_id)
        self.__bd.remove(m)
        self.__log.info(f"Medicamento eliminado ID={medicamento_id}")
        return True

    # Total de medicamentos

    def total(self): return len(self.__bd)