# SIGEFAR — API REST

## Descripción

API REST desarrollada con FastAPI para el Sistema Integral de Gestión de Farmacia (SIGEFAR).

La API permite gestionar clientes, medicamentos y ventas, además de consultar y eliminar el historial de actividades del sistema.

La aplicación utiliza PostgreSQL como base de datos y sigue una estructura separada por modelos, esquemas, DAO y routers.

---

## Tecnologías utilizadas

- Python
- FastAPI
- Pydantic
- PostgreSQL
- psycopg2
- Uvicorn
- JSON para almacenamiento de algunos datos auxiliares

---

## Requisitos

Antes de ejecutar la API se necesita tener instalado:

- Python
- PostgreSQL
- pip
- Uvicorn

También se debe tener disponible una base de datos PostgreSQL para el sistema.

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone URL_DEL_REPOSITORIO
```

### 2. Entrar a la carpeta de la API

```bash
cd "PROYECTO SIGEFAR FINAL 14"
```

### 3. Instalar las dependencias

Instalar las principales dependencias utilizadas por el proyecto:

```bash
pip install fastapi uvicorn psycopg2-binary pydantic
```

---

## Configuración de PostgreSQL

La conexión con PostgreSQL se encuentra en:

```text
config/base_datos.py
```

La API utiliza los siguientes valores de configuración:

```text
Host: localhost
Puerto: 5432
Base de datos: db_farmacia
Usuario: postgres
Contraseña: ""
```

Estos valores pueden ser modificados mediante las siguientes variables de entorno:

```text
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD
```

Si no se establecen estas variables, el sistema utiliza los valores definidos por defecto en `config/base_datos.py`.

La base de datos debe estar creada y PostgreSQL debe encontrarse ejecutándose antes de iniciar la API.

---

## Base de datos

Al iniciar la aplicación se ejecuta la función `inicializar()` de:

```text
config/base_datos.py
```

Esta función crea las tablas necesarias si todavía no existen.

### Tablas principales

#### Cliente

Contiene la información de los clientes:

- `id_cliente`
- `nomb_cli`
- `ape_cli`
- `dni`
- `telefono`

#### Medicamento

Contiene la información de los medicamentos:

- `id_medicamento`
- `nomb_med`
- `precio`
- `stock`

#### Venta

Contiene la información de las ventas:

- `id_venta`
- `fecha_venta`
- `id_cliente`
- `id_medicamento`
- `cantidad`
- `total`

La tabla `venta` mantiene relaciones mediante claves foráneas con `cliente` y `medicamento`.

---

## Ejecución

Para iniciar la API con Uvicorn:

```bash
uvicorn main:app --reload
```

La API estará disponible normalmente en:

```text
http://localhost:8000
```

---

## Documentación de la API

FastAPI genera automáticamente la documentación interactiva.

### Swagger UI

```text
http://localhost:8000/docs
```

### Documentación alternativa

```text
http://localhost:8000/redoc
```

Desde Swagger UI se pueden consultar y probar los diferentes endpoints de la API.

---

## Endpoint principal

### Inicio

```http
GET /
```

Devuelve información básica de la API:

```json
{
    "mensaje": "API Sistema Integral de Gestión de Farmacia (SIGEFAR)",
    "version": "1.0",
    "docs": "/docs"
}
```

---

# Endpoints

## Clientes

Ruta base:

```text
/clientes
```

### Listar clientes

```http
GET /clientes/
```

Obtiene todos los clientes registrados.

### Obtener cliente

```http
GET /clientes/{cliente_id}
```

Obtiene un cliente mediante su ID.

### Registrar cliente

```http
POST /clientes/
```

Registra un nuevo cliente.

Datos principales:

```json
{
    "nomb_cli": "Angel",
    "ape_cli": "Flores",
    "dni": "12345678",
    "telefono": "999999999"
}
```

El DNI debe contener exactamente 8 dígitos numéricos.

### Actualizar cliente

```http
PUT /clientes/{cliente_id}
```

Permite actualizar el nombre, apellido y teléfono de un cliente.

### Eliminar cliente

```http
DELETE /clientes/{cliente_id}
```

El cliente no puede eliminarse si tiene ventas asociadas.

---

## Medicamentos

Ruta base:

```text
/medicamentos
```

### Listar medicamentos

```http
GET /medicamentos/
```

Obtiene todos los medicamentos registrados.

### Obtener medicamento

```http
GET /medicamentos/{med_id}
```

Obtiene un medicamento mediante su ID.

### Registrar medicamento

```http
POST /medicamentos/
```

Registra un nuevo medicamento.

Ejemplo:

```json
{
    "nomb_med": "Paracetamol",
    "precio": 3.50,
    "stock": 20
}
```

El precio debe ser mayor que cero y el stock no puede ser negativo.

### Actualizar medicamento

```http
PUT /medicamentos/{med_id}
```

Permite actualizar nombre, precio y stock.

### Eliminar medicamento

```http
DELETE /medicamentos/{med_id}
```

El medicamento no puede eliminarse si tiene ventas asociadas.

---

## Ventas

Ruta base:

```text
/ventas
```

### Listar ventas

```http
GET /ventas/
```

Obtiene las ventas registradas junto con información del cliente y medicamento.

### Registrar venta

```http
POST /ventas/
```

Registra una nueva venta.

Ejemplo:

```json
{
    "id_cliente": 1,
    "id_medicamento": 1,
    "cantidad": 2
}
```

Antes de registrar la venta, la API verifica:

- Que el cliente exista.
- Que el medicamento exista.
- Que exista stock suficiente.
- Que la cantidad sea mayor que cero.

El total se calcula utilizando el precio del medicamento y la cantidad solicitada.

Al registrar la venta también se descuenta la cantidad correspondiente del stock del medicamento.

### Obtener venta

```http
GET /ventas/{venta_id}
```

Obtiene una venta mediante su ID.

### Ventas por cliente

```http
GET /ventas/cliente/{cliente_id}
```

Obtiene las ventas asociadas a un cliente específico.

---

## Registros

Ruta base:

```text
/registros
```

### Obtener historial

```http
GET /registros/
```

Obtiene el historial de actividades realizadas en el sistema.

El historial identifica el módulo y la acción realizada, como:

- Clientes — Registrar
- Clientes — Actualizar
- Clientes — Eliminar
- Medicamentos — Registrar
- Medicamentos — Actualizar
- Medicamentos — Eliminar
- Ventas — Registrar

### Eliminar historial

```http
DELETE /registros/
```

Elimina todos los registros almacenados actualmente en el historial del sistema.

---

# Validaciones

La API utiliza Pydantic mediante los archivos de `schemas/` para validar los datos recibidos.

### Clientes

- DNI de exactamente 8 dígitos.
- Campos requeridos para el registro.
- No se permite registrar un DNI duplicado.

### Medicamentos

- Precio mayor que cero.
- Stock igual o mayor que cero.

### Ventas

- Cantidad mayor que cero.
- Cliente existente.
- Medicamento existente.
- Stock suficiente.

---

# Manejo de errores

La API utiliza excepciones personalizadas y `HTTPException` para informar errores.

Algunos ejemplos:

```text
404 — Recurso no encontrado
400 — Datos inválidos o stock insuficiente
409 — Conflicto al eliminar un medicamento con ventas asociadas
```

Entre las excepciones personalizadas se encuentran:

- `ClienteNoEncontradoError`
- `DNIDuplicadoError`
- `ClienteConVentasError`
- `MedicamentoNoEncontradoError`
- `MedicamentoConVentasError`
- `VentaNoEncontradaError`

---

# Estructura del proyecto

```text
PROYECTO SIGEFAR FINAL 14/
│
├── config/
│   ├── base_datos.py
│   ├── logger.py
│   └── sistema_config.py
│
├── dao/
│   ├── cliente_dao.py
│   ├── medicamento_dao.py
│   └── venta_dao.py
│
├── modelos/
│   ├── cliente.py
│   ├── medicamento.py
│   └── venta.py
│
├── routers/
│   ├── clientes.py
│   ├── medicamentos.py
│   ├── registros.py
│   └── ventas.py
│
├── schemas/
│   ├── cliente_schema.py
│   ├── medicamento_schema.py
│   └── venta_schema.py
│
├── vistas/
│   └── menu.py
│
├── main.py
├── pruebas.py
│
├── datos_clientes.json
├── datos_medicamentos.json
└── datos_ventas.json
```

---

## Organización de la API

El proyecto separa sus responsabilidades en diferentes capas:

```text
Router
   ↓
Schema
   ↓
DAO
   ↓
Modelo
   ↓
Base de datos PostgreSQL
```

### Routers

Definen los endpoints de la API y reciben las solicitudes HTTP.

### Schemas

Definen y validan la información que recibe y devuelve la API mediante Pydantic.

### DAO

Se encargan de realizar las operaciones de acceso a la base de datos.

### Modelos

Representan las entidades principales del sistema:

- Cliente
- Medicamento
- Venta

### Config

Contiene la configuración de la conexión a la base de datos y el sistema de registros.

---

## CORS

La API permite solicitudes desde los siguientes orígenes:

```text
http://localhost:5173
http://localhost:3000
```

Esto permite que el frontend desarrollado con Vite pueda comunicarse con la API durante el desarrollo.

---

## Prueba de funcionamiento

Una vez iniciada la API, se puede acceder a:

```text
http://localhost:8000/docs
```

Desde Swagger UI se pueden probar los endpoints de clientes, medicamentos, ventas y registros.

---

## Relación con el frontend

El frontend de SIGEFAR utiliza esta API para:

- Consultar clientes.
- Registrar, actualizar y eliminar clientes.
- Consultar medicamentos.
- Registrar, actualizar y eliminar medicamentos.
- Registrar ventas.
- Consultar ventas.
- Consultar el historial de actividades.
- Eliminar el historial.

La conexión del frontend se realiza mediante Axios.

---

## Autor

Proyecto académico desarrollado para el Sistema Integral de Gestión de Farmacia (SIGEFAR).