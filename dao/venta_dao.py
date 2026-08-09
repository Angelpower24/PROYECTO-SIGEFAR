import psycopg2
from config.logger import Logger
from datetime import datetime
from config.base_datos import obtener_conexion

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
        cursor.execute("""INSERT INTO venta (fecha_venta, id_cliente, id_medicamento, cantidad, total) VALUES (%s, %s, %s, %s, %s) RETURNING id_venta""",
            (venta.fecha_venta, venta.id_cliente, venta.id_medicamento, venta.cantidad, venta.total))
        venta.id_venta = cursor.fetchone()["id_venta"]
        cursor.execute("""UPDATE medicamento SET stock = stock - %s WHERE id_medicamento = %s AND stock >= %s""",
           (venta.cantidad, venta.id_medicamento, venta.cantidad))
        conn.commit()
        conn.close()
        
        self.__log.info(
                        f"Venta registrada: "
                        f"ID={venta.id_venta} | "
                        f"Cliente ID={venta.id_cliente} | "
                        f"Medicamento ID={venta.id_medicamento} | "
                        f"Cantidad: {venta.cantidad} | "
                        f"Total: S/.{venta.total:.2f}"
                    )
        
        return venta
    
    # OBTENER TODOS
    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(""" 
            SELECT v.id_venta, v.fecha_venta, c.nomb_cli, c.ape_cli, m.nomb_med, v.cantidad, v.total,
            v.id_cliente, v.id_medicamento
            FROM venta v
            JOIN cliente c ON v.id_cliente = c.id_cliente
            JOIN medicamento m ON v.id_medicamento = m.id_medicamento
            ORDER BY v.fecha_venta DESC
        """)
        filas = cursor.fetchall()
        conn.close()
        return filas
    
      #BUSCAR POR ID
    def buscar_por_id(self, venta_id):

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT v.id_venta, v.id_cliente, v.id_medicamento, c.nomb_cli, c.ape_cli, m.nomb_med,v.cantidad,
            v.fecha_venta, v.total
            FROM venta v
            JOIN cliente c
                ON v.id_cliente = c.id_cliente
            JOIN medicamento m
                ON v.id_medicamento = m.id_medicamento
            WHERE v.id_venta = %s
        """, (venta_id,))

        fila = cursor.fetchone()

        conn.close()

        return fila
    
    # BUSCAR POR CLIENTE
    def buscar_por_cliente(self, id_cliente):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.id_venta, v.fecha_venta, c.nomb_cli, c.ape_cli, m.nomb_med, v.cantidad, v.total,
            v.id_cliente, v.id_medicamento
            FROM venta v
            JOIN cliente c ON v.id_cliente = c.id_cliente
            JOIN medicamento m ON v.id_medicamento = m.id_medicamento
            WHERE v.id_cliente = %s
            ORDER BY v.fecha_venta DESC
        """, (id_cliente,))
        filas = cursor.fetchall()
        conn.close()
        return filas
   
    # TOTAL
    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM venta")
        total = cursor.fetchone()["total"]
        conn.close()
        return total