import json
import os
from modelos.cliente import Cliente
from modelos.medicamento import Medicamento
from modelos.venta import Venta

_BASE = os.path.dirname (os.path.dirname(os.path.abspath(__file__)))

ARCHIVO_CLIENTES  = os.path.join(_BASE, "datos_clientes.json")
ARCHIVO_MEDICAMENTOS  = os.path.join(_BASE, "datos_medicamentos.json")
ARCHIVO_VENTAS  = os.path.join(_BASE, "datos_ventas.json")

#GUARDAR CLIENTE
def guardar_clientes(cdao):
    datos = [c.to_dict() for c in cdao.obtener_todos()]
    with open(ARCHIVO_CLIENTES, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)
    print(f" OK Clientes guardados en '{ARCHIVO_CLIENTES}'")
#CARGAR CLIENTE        
def cargar_clientes(cdao):
    try:
        with open(ARCHIVO_CLIENTES, "r", encoding="utf-8") as f:
            datos = json.load(f)
            for d in datos:
                cliente = Cliente.from_dict(d)
                cdao._ClienteDAO__bd.append(cliente)
                if cliente.id >= cdao._ClienteDAO__cid:
                    cdao.__ClienteDAO__cid = cliente.id + 1
            print(f" OK {len(datos)} clientes cargados desde '{ARCHIVO_CLIENTES}'")
    except FileNotFoundError:
        print(f" AVISO: No existe '{ARCHIVO_CLIENTES}', se empieza desde cero")
        
        
#GUARDAR MEDICAMENTO
def guardar_medicamentos(mdao):
    datos = [m.to_dict() for m in mdao.obtener_todos()]
    with open(ARCHIVO_MEDICAMENTOS, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)
    print(f" OK Medicamentos guardados en '{ARCHIVO_MEDICAMENTOS}'")
#CARGAR MEDICAMENTO 
def cargar_medicamentos(mdao):
    try:
        with open(ARCHIVO_MEDICAMENTOS, "r", encoding="utf-8") as f:
            datos = json.load(f)
            for d in datos:
                medicamento = Medicamento.from_dict(d)
                mdao._MedicamentoDAO__bd.append(medicamento)
                if medicamento.id >= mdao._MedicamentoDAO__cid:
                    mdao.__MedicamentoDAO__cid = medicamento.id + 1
            print(f" OK {len(datos)} medicamentos cargados desde '{ARCHIVO_MEDICAMENTOS}'")
    except FileNotFoundError:
        print(f" AVISO: No existe '{ARCHIVO_MEDICAMENTOS}', se empieza desde cero")
        
        
#GUARDAR VENTA
def guardar_ventas(vdao):
    datos = [v.to_dict() for v in vdao.obtener_todos()]
    with open(ARCHIVO_VENTAS, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)
    print(f" OK Ventas guardadas en '{ARCHIVO_VENTAS}'")
#CARGAR VENTA
def cargar_ventas(vdao):
    try:
        with open(ARCHIVO_VENTAS, "r", encoding="utf-8") as f:
            datos = json.load(f)
            for d in datos:
                venta = Venta.from_dict(d)
                vdao._VentaDAO__bd.append(venta)
                if venta.id >= vdao._VentaDAO__cid:
                    vdao.__VentaDAO__cid = venta.id + 1
            print(f" OK {len(datos)} ventas cargadas desde '{ARCHIVO_VENTAS}'")
    except FileNotFoundError:
        print(f" AVISO: No existe '{ARCHIVO_VENTAS}', se empieza desde cero")