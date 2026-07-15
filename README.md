# 💊 SIGEFAR - Sistema Integral de Gestión de Farmacia

## Descripción

SIGEFAR es una aplicación desarrollada en Python que simula un Sistema Integral de Gestión de Farmacia. El proyecto fue elaborado aplicando los principios de Programación Orientada a Objetos (POO), utilizando el patrón DAO (Data Access Object) para la administración de la información.

El sistema permite administrar clientes, medicamentos y ventas mediante un menú interactivo en consola. Además, incorpora persistencia de datos en archivos JSON, un historial de eventos mediante un Logger y una estructura organizada en módulos para facilitar su mantenimiento.

---

## Funcionalidades

### Gestión de Clientes
- Agregar clientes.
- Listar clientes registrados.
- Actualizar información de un cliente.
- Eliminar clientes.
- Visualizar clientes en formato JSON.

### Gestión de Medicamentos
- Agregar medicamentos.
- Listar medicamentos.
- Actualizar precio o información del medicamento.
- Eliminar medicamentos.
- Visualizar medicamentos en formato JSON.

### Gestión de Ventas
- Registrar ventas.
- Listar ventas realizadas.
- Eliminar ventas.
- Visualizar ventas en formato JSON.

### Persistencia de Datos
- Guardar toda la información en archivos JSON.
- Cargar automáticamente la información almacenada.

### Historial del Sistema
- Registrar automáticamente todas las operaciones realizadas.
- Mostrar el historial de eventos.
- Limpiar el historial cuando sea necesario.

---

## Tecnologías utilizadas

- Python 3
- Programación Orientada a Objetos (POO)
- Patrón DAO (Data Access Object)
- Archivos JSON para persistencia
- Manejo de excepciones personalizadas
- Singleton para la configuración y el Logger

---

## Estructura del proyecto

```
SIGEFAR
│
├── config
│   ├── logger.py
│   ├── persistencia.py
│   └── sistema_config.py
│
├── dao
│   ├── cliente_dao.py
│   ├── medicamento_dao.py
│   └── venta_dao.py
│
├── modelos
│   ├── cliente.py
│   ├── medicamento.py
│   └── venta.py
│
├── vistas
│   └── menu.py
│
├── main.py
└── README.md
```

---

## Menú principal

El sistema permite realizar las siguientes operaciones:

1. Agregar cliente.
2. Agregar medicamento.
3. Registrar venta.
4. Listar clientes.
5. Listar medicamentos.
6. Listar ventas.
7. Actualizar cliente.
8. Actualizar medicamento.
9. Eliminar cliente.
10. Eliminar medicamento.
11. Eliminar venta.
12. Ver clientes en JSON.
13. Ver medicamentos en JSON.
14. Ver ventas en JSON.
15. Guardar datos en JSON.
16. Ver historial de logs.
17. Limpiar historial.
0. Salir del sistema.

---

## Base de datos del proyecto

El diseño del sistema está basado en la base de datos **DB_FARMACIA**, conformada por tres entidades principales:

- Cliente
- Medicamento
- Venta

La aplicación implementa las operaciones CRUD (Crear, Leer, Actualizar y Eliminar) sobre dichas entidades.

---

## Autor

**Angel Flores**

Instituto de Educación Superior Tecnológico Público Argentina

Proyecto desarrollado para el curso de Programación Orientada a Objetos.