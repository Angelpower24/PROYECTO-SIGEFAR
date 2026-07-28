import os
import psycopg2
from psycopg2.extras import RealDictCursor

def obtener_conexion():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "db_farmacia"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
    )
    
    conn.cursor_factory = RealDictCursor
    return conn

def inicializar():

    conn = obtener_conexion()
    cursor = conn.cursor()

    # TABLA CLIENTE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cliente(
            id_cliente SERIAL PRIMARY KEY,
            nomb_cli   TEXT NOT NULL,
            ape_cli    TEXT NOT NULL,
            dni        TEXT UNIQUE NOT NULL,
            telefono   TEXT
        )
    """)

    # TABLA MEDICAMENTO
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicamento(
            id_medicamento SERIAL PRIMARY KEY,
            nomb_med TEXT NOT NULL,
            precio NUMERIC(10,2) NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

    # TABLA VENTA
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS venta(
            id_venta SERIAL PRIMARY KEY,
            fecha_venta TEXT NOT NULL,
            id_cliente INTEGER NOT NULL,
            id_medicamento INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            total NUMERIC(10,2) NOT NULL,   
            FOREIGN KEY (id_cliente)REFERENCES cliente(id_cliente),
            FOREIGN KEY (id_medicamento)REFERENCES medicamento(id_medicamento)
        )
    """)

    conn.commit()
    conn.close()