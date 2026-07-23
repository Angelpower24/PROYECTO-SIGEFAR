import sqlite3

ARCHIVO_BD = "farmacia.db"

def obtener_conexion():
    conn = sqlite3.connect(ARCHIVO_BD)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn

def inicializar():

    conn = obtener_conexion()
    cursor = conn.cursor()

    # TABLA CLIENTE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cliente(
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nomb_cli TEXT NOT NULL,
            ape_cli TEXT NOT NULL,
            dni TEXT UNIQUE NOT NULL,
            telefono TEXT
        )
    """)

    # TABLA MEDICAMENTO
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicamento(
            id_medicamento INTEGER PRIMARY KEY AUTOINCREMENT,
            nomb_med TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

    # TABLA VENTA
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS venta(
            id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_venta TEXT NOT NULL,
            id_cliente INTEGER NOT NULL,
            id_medicamento INTEGER NOT NULL
            cantidad INTEGER NOT NULL,
            total REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()