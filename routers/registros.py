from fastapi import APIRouter
from config.logger import Logger

router = APIRouter(prefix="/registros", tags=["Registros"])

logger = Logger()


@router.get("/")
def obtener_registros():

    registros = []

    for log in logger._logs:

        mensaje = log["msg"]

        modulo = "Sistema"
        accion = "Información"
        informacion = mensaje

        # CLIENTES
        if mensaje.startswith("Cliente agregado:"):
            modulo = "Clientes"
            accion = "Registrar"
            informacion = mensaje.replace("Cliente agregado:", "").strip()

        elif mensaje.startswith("Cliente actualizado:"):
            modulo = "Clientes"
            accion = "Actualizar"
            informacion = mensaje.replace("Cliente actualizado:", "").strip()

        elif mensaje.startswith("Cliente eliminado:"):
            modulo = "Clientes"
            accion = "Eliminar"
            informacion = mensaje.replace("Cliente eliminado:", "").strip()

        # MEDICAMENTOS
        elif mensaje.startswith("Medicamento agregado:"):
            modulo = "Medicamentos"
            accion = "Registrar"
            informacion = mensaje.replace("Medicamento agregado:", "").strip()

        elif mensaje.startswith("Medicamento actualizado:"):
            modulo = "Medicamentos"
            accion = "Actualizar"
            informacion = mensaje.replace("Medicamento actualizado:", "").strip()

        elif mensaje.startswith("Medicamento eliminado:"):
            modulo = "Medicamentos"
            accion = "Eliminar"
            informacion = mensaje.replace("Medicamento eliminado:", "").strip()

        # VENTAS
        elif mensaje.startswith("Venta registrada:"):
            modulo = "Ventas"
            accion = "Registrar"
            informacion = mensaje.replace("Venta registrada:", "").strip()

        registros.append({
            "hora": log["hora"],
            "nivel": log["nivel"],
            "modulo": modulo,
            "accion": accion,
            "informacion": informacion
        })

    return registros