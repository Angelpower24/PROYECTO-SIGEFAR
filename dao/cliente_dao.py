from config.logger import Logger

# EXCEPCIONES PERSONALIZADAS

class ClienteNoEncontradoError(Exception):
    def __init__(self, cliente_id):
        super().__init__(f"Cliente ID={cliente_id} no encontrado")

class DNIDuplicadoError(Exception):
    def __init__(self, dni):
        super().__init__(f"El DNI {dni} ya existe")


# DAO CLIENTE

class ClienteDAO:
    def __init__(self):
        self.__bd = []
        self.__cid = 1
        self.__log = Logger()

    # Insertar cliente

    def insertar(self, cliente):
        if self.buscar_por_dni(cliente.dni):
            self.__log.warning(f"DNI duplicado: {cliente.dni}")
            raise DNIDuplicadoError(cliente.dni)
        cliente.id = self.__cid
        self.__cid += 1
        self.__bd.append(cliente)
        self.__log.info(
            f"Cliente agregado: {cliente.nomb_cli} {cliente.ape_cli}")
        return cliente

    # Buscar por DNI
    
    def buscar_por_dni(self, dni):
        for c in self.__bd:
            if c.dni == dni:
                return c
        return None

    # Buscar por ID

    def buscar_por_id(self, cliente_id):
        for c in self.__bd:
            if c.id == cliente_id:
                return c
        return None

    # Listar clientes

    def obtener_todos(self):
        return sorted(self.__bd, key=lambda c: c.nomb_cli)

    # Actualizar cliente

    def actualizar(self,cliente_id,nomb_cli=None,ape_cli=None,telefono=None):
        c = self.buscar_por_id(cliente_id)
        if not c:
            self.__log.error(f"Cliente ID={cliente_id} no encontrado")
            raise ClienteNoEncontradoError(cliente_id)
        if nomb_cli: c.nomb_cli = nomb_cli
        if ape_cli:  c.ape_cli  = ape_cli
        if telefono: c.telefono = telefono
        self.__log.info(f"Cliente actualizado ID={cliente_id}")
        return c

    # Eliminar cliente

    def eliminar(self, cliente_id):
        c = self.buscar_por_id(cliente_id)
        if not c:
            self.__log.error(f"Cliente ID={cliente_id} no encontrado")
            raise ClienteNoEncontradoError(cliente_id)
        self.__bd.remove(c)
        self.__log.info(
            f"Cliente eliminado ID={cliente_id}")
        return True

    # Total de clientes

    def total(self): return len(self.__bd)