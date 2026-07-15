from modelos.cliente import Cliente
from dao.cliente_dao import DNIDuplicadoError,ClienteNoEncontradoError
from modelos.medicamento import Medicamento
from dao.medicamento_dao import MedicamentoNoEncontradoError
from modelos.venta import Venta
from dao.venta_dao import VentaNoEncontradaError
import json

# MENÚ PRINCIPAL

def mostrar_menu(cfg):

    print(f"\n{'=' * 70}")
    print(f"     {cfg.nombre}   v{cfg.version}")
    print(f"     {cfg.empresa}")
    print(f"     Autor: {cfg.autor}")
    print(f"{'=' * 70}")
    print(" 1. Agregar cliente")
    print(" 2. Agregar medicamento")
    print(" 3. Registrar venta")
    print(" 4. Listar clientes")
    print(" 5. Listar medicamentos")
    print(" 6. Listar ventas")
    print(" 7. Actualizar cliente")
    print(" 8. Actualizar medicamento")
    print(" 9. Eliminar cliente")
    print("10. Eliminar medicamento")
    print("11. Eliminar venta")  
    print("12. Ver clientes en JSON")
    print("13. Ver medicamentos en JSON")
    print("14. Ver ventas en JSON")
    print("15. Guardar datos en JSON")  
    print("16. Ver historial de logs")
    print("17. Limpiar historial")
    print(" 0. Salir")
    print(f"{'=' * 70}")  
    
def agregar_cliente(cdao):
    print("\n--- AGREGAR CLIENTE ---")
    nomb_cli = input("Nombre: ")
    ape_cli = input("Apellido: ")
    dni = input("DNI: ")
    telefono = input("Teléfono: ")
    try:
        cliente = Cliente(nomb_cli, ape_cli, dni, telefono)
        cdao.insertar(cliente)
        print(f"Cliente agregado con ID={cliente.id}")
    except DNIDuplicadoError as ex:
        print(ex)
          
def agregar_medicamento(mdao):
    print("\n--- AGREGAR MEDICAMENTO ---")
    nomb_med = input("Nombre: ")

    try:
        precio = float(input("Precio: "))
        stock = int(input("Stock: "))
        medicamento = Medicamento(nomb_med,precio,stock)
        mdao.insertar(medicamento)
        print(f"Medicamento agregado con ID={medicamento.id}")
    except ValueError:
        print("Precio o Stock inválido.")   
        
def registrar_venta(vdao):
    print("\n--- REGISTRAR VENTA ---")
    fecha = input("Fecha (AAAA-MM-DD): ")
    try:
        id_cliente = int(input("ID Cliente: "))
        id_medicamento = int(input("ID Medicamento: "))
        venta = Venta(fecha,id_cliente,id_medicamento)
        vdao.insertar(venta)
        print(f"Venta registrada con ID={venta.id}")
    except ValueError:
        print("Datos incorrectos.")  
        
def listar_clientes(cdao):
    print("\n------ CLIENTES ------")
    clientes = cdao.obtener_todos()
    if clientes:
        for c in clientes: print(c)
    else:
        print("No existen clientes.")
         
def listar_medicamentos(mdao):
    print("\n------ MEDICAMENTOS ------")
    medicamentos = mdao.obtener_todos()
    if medicamentos:
        for m in medicamentos: print(m)
    else:
        print("No existen medicamentos.")
             
def listar_ventas(vdao):
    print("\n------ VENTAS ------")
    ventas = vdao.obtener_todos()
    if ventas:
        for v in ventas: print(v)
    else:
        print("No existen ventas.")
           
# ==========================================================
# ACTUALIZAR CLIENTE
# ==========================================================

def actualizar_cliente(cdao):

    print("\n--- ACTUALIZAR CLIENTE ---")
    try:
        cliente_id = int(input("ID del cliente: "))
        nomb_cli = input("Nuevo nombre (Enter para mantener): ").strip()
        ape_cli = input("Nuevo apellido (Enter para mantener): ").strip()
        telefono = input("Nuevo teléfono (Enter para mantener): ").strip()
        cliente = cdao.actualizar(cliente_id,nomb_cli or None,ape_cli or None,telefono or None)
        print("Cliente actualizado correctamente.")
        print(cliente)
    except ClienteNoEncontradoError as ex:
        print(ex)
    except ValueError:
        print("ID inválido.")
              
# ==========================================================
# ACTUALIZAR MEDICAMENTO
# ==========================================================

def actualizar_medicamento(mdao):
    print("\n--- ACTUALIZAR MEDICAMENTO ---")
    try:
        medicamento_id = int(input("ID del medicamento: "))
        nomb_med = input("Nuevo nombre (Enter para mantener): ").strip()
        precio_txt = input("Nuevo precio (Enter para mantener): ").strip()
        stock_txt = input("Nuevo stock (Enter para mantener): ").strip()
        precio = float(precio_txt) if precio_txt else None
        stock = int(stock_txt) if stock_txt else None
        medicamento = mdao.actualizar(medicamento_id,nomb_med or None,precio,stock)
        print("Medicamento actualizado correctamente.")
        print(medicamento)
    except MedicamentoNoEncontradoError as ex:
        print(ex)
    except ValueError:
        print("Datos incorrectos.")
           
# ==========================================================
# ELIMINAR CLIENTE
# ==========================================================

def eliminar_cliente(cdao):
    print("\n--- ELIMINAR CLIENTE ---")
    try:
        cliente_id = int(input("ID del cliente: "))
        cdao.eliminar(cliente_id)
        print("Cliente eliminado.")
    except ClienteNoEncontradoError as ex: 
        print(ex)
    except ValueError:
        print("ID inválido.") 
        
# ==========================================================
# ELIMINAR MEDICAMENTO
# ==========================================================

def eliminar_medicamento(mdao):
    print("\n--- ELIMINAR MEDICAMENTO ---")
    try:
        medicamento_id = int(input("ID del medicamento: "))
        mdao.eliminar(medicamento_id)
        print("Medicamento eliminado.")
    except MedicamentoNoEncontradoError as ex:
        print(ex)
    except ValueError:
        print("ID inválido.")
    
        
# ==========================================================
# ELIMINAR VENTA
# ==========================================================

def eliminar_venta(vdao):
    print("\n--- ELIMINAR VENTA ---")
    try:
        venta_id = int(input("ID de la venta: "))
        vdao.eliminar(venta_id)
        print("Venta eliminada.")
    except VentaNoEncontradaError as ex:
        print(ex)
    except ValueError:
        print("ID inválido.")
        
        
        
# ==========================================================
# VER CLIENTES JSON
# ==========================================================

def ver_clientes_json(cdao):
    print("\n--- CLIENTES EN JSON ---")
    clientes = cdao.obtener_todos()
    if clientes:
        datos = [c.to_dict() for c in clientes]
        print(json.dumps(datos, indent=4, ensure_ascii=False))
    else:
        print("  (No hay clientes registrados)")

# ==========================================================
# VER MEDICAMENTOS JSON
# ==========================================================

def ver_medicamentos_json(mdao):
    print("\n--- MEDICAMENTOS EN JSON ---")
    medicamentos = mdao.obtener_todos()
    if medicamentos:
        datos = [m.to_dict() for m in medicamentos]
        print(json.dumps(datos, indent=4, ensure_ascii=False))
    else:
        print("  (No hay medicamentos registrados)")
        
# ==========================================================
# VER VENTAS JSON
# ==========================================================

def ver_ventas_json(vdao):
    print("\n--- VENTAS EN JSON ---")
    ventas = vdao.obtener_todos()
    if ventas:
        datos = [v.to_dict() for v in ventas]
        print(json.dumps(datos, indent=4, ensure_ascii=False))
    else:
        print("  (No hay ventas registradas)")

