from config.logger import Logger
from config.base_datos import obtener_conexion
import sqlite3
from modelos.medicamento import Medicamento

# EXCEPCIONES
class MedicamentoNoEncontradoError(Exception):
    def __init__(self, med_id):
        super().__init__(f"Medicamento ID={med_id} no encontrado")

class MedicamentoConVentasError(Exception):
    def __init__(self, med_id):
        super().__init__(f"Medicamento ID={med_id} no se puede eliminar: tiene ventas asociadas")

# CLASE MEDICAMENTO DAO
class MedicamentoDAO:
    def __init__(self):
        self.__log = Logger()
        
    # INSERTAR
    def insertar(self, m):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO medicamento (nomb_med, precio, stock) VALUES (?, ?, ?)",
        (m.nomb_med, m.precio, m.stock)
        )
        conn.commit()
        m.id_medicamento = cursor.lastrowid
        conn.close()

        self.__log.info(f"Medicamento agregado: {m.nomb_med} S/.{m.precio:.2f} (ID={m.id_medicamento})")
        return m

    # OBTENER TODOS
    def obtener_todos(self):

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM medicamento ORDER BY nomb_med")
        filas = cursor.fetchall()
        conn.close()
        return [self.__fila_a_medicamento(f) for f in filas]

    # BUSCAR
    def buscar(self, med_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM medicamento WHERE id_medicamento = ?",(med_id,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_medicamento(fila) if fila else None

    # ACTUALIZAR
    def actualizar(self, med_id, nomb_med=None, precio=None, stock=None):
        m = self.buscar(med_id)
        if not m:
            self.__log.error(f"Actualizar fallido: Medicamento ID={med_id} no existe")
            raise MedicamentoNoEncontradoError(med_id)
        nuevo_nombre = nomb_med if nomb_med is not None else m.nomb_med
        nuevo_precio = precio if precio is not None else m.precio
        nuevo_stock = stock if stock is not None else m.stock
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            UPDATE medicamento SET nomb_med=?, precio=?, stock=? WHERE id_medicamento=?
            """,
            (nuevo_nombre, nuevo_precio, nuevo_stock, med_id)
        )
        conn.commit()
        conn.close()

        m.nomb_med = nuevo_nombre
        m.precio = nuevo_precio
        m.stock = nuevo_stock

        self.__log.info(f"Medicamento actualizado: (ID={med_id})")
        return m

    # ELIMINAR
    def eliminar(self, med_id):
        m = self.buscar(med_id)
        if not m:
            self.__log.error(f"Eliminar fallido: Medicamento ID={med_id} no existe")
            raise MedicamentoNoEncontradoError(med_id)
        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM medicamento WHERE id_medicamento = ?",(med_id,))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            self.__log.warning(f"Eliminar fallido: Medicamento ID={med_id} tiene ventas asociadas")
            raise MedicamentoConVentasError(med_id)
        conn.close()
        self.__log.info(f"Medicamento eliminado: {m.nomb_med} (ID={med_id})")
        return True

    # TOTAL
    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM medicamento")
        total = cursor.fetchone()[0]
        conn.close()
        return total

    # FILA A MEDICAMENTOS
    def __fila_a_medicamento(self, fila):
        m = Medicamento(
            fila["nomb_med"],
            fila["precio"],
            fila["stock"]
        )
        m.id_medicamento = fila["id_medicamento"]
        return m