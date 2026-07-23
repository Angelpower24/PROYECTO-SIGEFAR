from config.logger import Logger
from config.base_datos import obtener_conexion
import sqlite3
from modelos.cliente import Cliente

# EXCEPCIONES
class ClienteNoEncontradoError(Exception):
    def __init__(self, cliente_id):
        super().__init__(f"Cliente ID={cliente_id} no encontrado")

class DNIDuplicadoError(Exception):
    def __init__(self, dni):
        super().__init__(f"DNI '{dni}' ya registrado")

class ClienteConVentasError(Exception):
    def __init__(self, cliente_id):
        super().__init__(f"Cliente ID={cliente_id} no se puede eliminar: tiene ventas asociadas")

#  CLASE CLIENTE DAO
class ClienteDAO:
    def __init__(self):
        self.__log = Logger()
        
    # INSERTAR
    def insertar(self, cliente):
        if self.buscar_por_dni(cliente.dni):
            self.__log.warning(f"DNI duplicado: {cliente.dni}")
            raise DNIDuplicadoError(cliente.dni)

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO cliente (nomb_cli, ape_cli, dni, telefono) VALUES (?, ?, ?, ?)",
            (cliente.nomb_cli, cliente.ape_cli, cliente.dni, cliente.telefono)
        )
        conn.commit()
        cliente.id_cliente = cursor.lastrowid
        conn.close()

        self.__log.info(f"Cliente agregado: {cliente.nomb_cli} (ID={cliente.id_cliente})")

        return cliente
    
    # BUSCAR POR DNI
    def buscar_por_dni(self, dni):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cliente WHERE dni = ?", (dni,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_cliente(fila) if fila else None

    # BUSCAR POR ID
    def buscar_por_id(self, cliente_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cliente WHERE id_cliente = ?", (cliente_id,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_cliente(fila) if fila else None

    # OBTENER TODOS
    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cliente ORDER BY nomb_cli")
        filas = cursor.fetchall()
        conn.close()
        return [self.__fila_a_cliente(f) for f in filas]

    # ACTUALIZAR
    def actualizar(self, cliente_id, nomb_cli=None, ape_cli=None, telefono=None):
        c = self.buscar_por_id(cliente_id)
        if not c:
            self.__log.error(f"Actualizar fallido: Cliente ID={cliente_id} no existe")
            raise ClienteNoEncontradoError(cliente_id)

        nuevo_nombre = nomb_cli if nomb_cli is not None else c.nomb_cli
        nuevo_apellido = ape_cli if ape_cli is not None else c.ape_cli
        nuevo_telefono = telefono if telefono is not None else c.telefono
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE cliente SET nomb_cli=?, ape_cli=?, telefono=? WHERE id_cliente=?",
            (nuevo_nombre, nuevo_apellido, nuevo_telefono, cliente_id)
        )

        conn.commit()
        conn.close()
        c.nomb_cli = nuevo_nombre
        c.ape_cli = nuevo_apellido
        c.telefono = nuevo_telefono
        
        self.__log.info(f"Cliente actualizado: {c.nomb_cli} (ID={cliente_id})")
        
        return c

    # ELIMINAR
    def eliminar(self, cliente_id):
        c = self.buscar_por_id(cliente_id)
        if not c:
            self.__log.error(f"Eliminar fallido: Cliente ID={cliente_id} no existe")
            raise ClienteNoEncontradoError(cliente_id)
        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM cliente WHERE id_cliente = ?", (cliente_id,))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            self.__log.warning(f"Eliminar fallido: Cliente ID={cliente_id} tiene ventas asociadas")
            raise ClienteConVentasError(cliente_id)
        conn.close()
        
        self.__log.info(f"Cliente eliminado: {c.nomb_cli} (ID={cliente_id})")

    # TOTAL
    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM cliente")
        total = cursor.fetchone()[0]
        conn.close()
        return total

    # FILA A CLIENTE
    def __fila_a_cliente(self, fila):
        c = Cliente(
            fila["nomb_cli"],
            fila["ape_cli"],
            fila["dni"],
            fila["telefono"]
        )
        c.id_cliente = fila["id_cliente"]
        return c