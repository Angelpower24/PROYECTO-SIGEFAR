from fastapi import APIRouter, HTTPException
from dao.medicamento_dao import MedicamentoDAO, MedicamentoNoEncontradoError, MedicamentoConVentasError
from modelos.medicamento import Medicamento
from schemas.medicamento_schema import MedicamentoCrear, MedicamentoActualizar, MedicamentoRespuesta

router = APIRouter(prefix="/medicamentos", tags=["Medicamentos"])
dao = MedicamentoDAO()

@router.get("/", response_model=list[MedicamentoRespuesta])
def listar_medicamentos():
    return [m.to_dict() for m in dao.obtener_todos()]

@router.get("/{med_id}", response_model=MedicamentoRespuesta)
def obtener_medicamento(med_id: int):
    m = dao.buscar(med_id)
    if not m:
        raise HTTPException(status_code=404, detail=f"Medicamento ID={med_id} no encontrado")
    return m.to_dict()

@router.post("/", response_model=MedicamentoRespuesta, status_code=201)
def crear_medicamento(datos: MedicamentoCrear):
    m = dao.insertar(Medicamento(datos.nomb_med, datos.precio, datos.stock))
    return m.to_dict()

@router.put("/{med_id}", response_model=MedicamentoRespuesta)
def actualizar_medicamento(med_id: int, datos: MedicamentoActualizar):
    try:
        m = dao.actualizar(med_id, datos.nomb_med, datos.precio, datos.stock)
        return m.to_dict()
    except MedicamentoNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))

@router.delete("/{med_id}")
def eliminar_medicamento(med_id: int):
    try:
        dao.eliminar(med_id)
        return {"mensaje": f"Medicamento ID={med_id} eliminado"}
    except MedicamentoNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except MedicamentoConVentasError as ex:
        raise HTTPException(status_code=409, detail=str(ex))