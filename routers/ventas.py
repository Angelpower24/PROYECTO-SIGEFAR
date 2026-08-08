from fastapi import APIRouter, HTTPException
from dao.venta_dao import VentaDAO, VentaNoEncontradaError
from dao.medicamento_dao import MedicamentoDAO, MedicamentoNoEncontradoError
from dao.cliente_dao import ClienteDAO, ClienteNoEncontradoError
from modelos.venta import Venta
from schemas.venta_schema import VentaCrear, VentaRespuesta

router = APIRouter(prefix="/ventas", tags=["Ventas"])

vdao = VentaDAO()
cdao = ClienteDAO()
mdao = MedicamentoDAO()

@router.get("/", response_model=list[VentaRespuesta])
def listar_ventas():
    return vdao.obtener_todos()

@router.post("/", response_model=VentaRespuesta)
def registrar_venta(datos: VentaCrear):

    # VERIFICAR CLIENTE
    cliente = cdao.buscar_por_id(datos.id_cliente)

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail=f"Cliente ID={datos.id_cliente} no encontrado"
        )

    # VERIFICAR MEDICAMENTO
    medicamento = mdao.buscar(datos.id_medicamento)

    if not medicamento:
        raise HTTPException(
            status_code=404,
            detail=f"Medicamento ID={datos.id_medicamento} no encontrado"
        )

    # VERIFICAR STOCK
    if datos.cantidad > medicamento.stock:
        raise HTTPException(
            status_code=400,
            detail=f"Stock insuficiente. Stock disponible: {medicamento.stock}"
        )

    # CALCULAR TOTAL
    total = round(
        medicamento.precio * datos.cantidad,
        2
    )

    # CREAR OBJETO VENTA
    venta = Venta(
        datos.id_cliente,
        datos.id_medicamento,
        datos.cantidad,
        total
    )

    # REGISTRAR UTILIZANDO TU DAO EXISTENTE
    vdao.registrar(venta)

    # OBTENER LA VENTA COMPLETA
    return vdao.buscar_por_id(venta.id_venta)

@router.get("/{venta_id}", response_model=VentaRespuesta)
def obtener_venta(venta_id: int):
    v = vdao.buscar_por_id(venta_id)
    if not v:
        raise HTTPException(status_code=404, detail=f"Venta ID={venta_id} no encontrada")
    return v

@router.get("/cliente/{cliente_id}", response_model=list[VentaRespuesta])
def ventas_por_cliente(cliente_id: int):
    c = cdao.buscar_por_id(cliente_id)
    if not c:
        raise HTTPException(status_code=404, detail=f"Cliente ID={cliente_id} no encontrado")
    return vdao.buscar_por_cliente(cliente_id)
