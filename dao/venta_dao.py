from config.logger import Logger
from datetime import datetime
from config.base_datos import obtener_conexion
from modelos.venta import Venta

# EXCEPCIONES
class VentaNoEncontradaError(Exception):
    def __init__(self, venta_id):
        super().__init__(f"Venta ID={venta_id} no encontrada")

# CLASE VENTA DAO
class VentaDAO:
    def __init__(self):
        self.__log = Logger()

    # REGISTRAR
    def registrar(self, venta):
        
        venta.fecha_venta = datetime.now().strftime("%Y-%m-%d")
        venta.total = round(venta.total, 2)
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO venta (fecha_venta, id_cliente, id_medicamento, cantidad, total) VALUES (?, ?, ?, ?, ?)""",
            (venta.fecha_venta, venta.id_cliente, venta.id_medicamento, venta.cantidad, venta.total))
        cursor.execute("""UPDATE medicamento SET stock = stock - ? WHERE id_medicamento = ? """,
           (venta.cantidad, venta.id_medicamento))
        conn.commit()
        venta.id_venta = cursor.lastrowid
        conn.close()
        self.__log.info(f"Venta registrada: ID={venta.id_venta}")
        return venta
    
    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(""" 
            SELECT v.id_venta, v.fecha_venta, c.nomb_cli, c.ape_cli, m.nomb_med, v.cantidad, v.total
            FROM venta v
            JOIN cliente c ON v.id_cliente = c.id_cliente
            JOIN medicamento m ON v.id_medicamento = m.id_medicamento
            ORDER BY v.fecha_venta DESC
        """)
        filas = cursor.fetchall()
        conn.close()
        return filas
    
    # BUSCAR POR CLIENTE
    def buscar_por_cliente(self, id_cliente):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.id_venta, v.fecha_venta, c.nomb_cli, c.ape_cli, m.nomb_med, v.cantidad, v.total
            FROM venta v
            JOIN cliente c ON v.id_cliente = c.id_cliente
            JOIN medicamento m ON v.id_medicamento = m.id_medicamento
            WHERE v.id_cliente = ?
            ORDER BY v.fecha_venta DESC
        """, (id_cliente,))
        filas = cursor.fetchall()
        conn.close()
        return filas
   
    # TOTAL
    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM venta")
        total = cursor.fetchone()[0]
        conn.close()
        return total