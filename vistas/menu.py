from modelos.cliente import Cliente
from modelos.medicamento import Medicamento
from modelos.venta import Venta
from dao.cliente_dao import DNIDuplicadoError, ClienteNoEncontradoError
from dao.medicamento_dao import MedicamentoNoEncontradoError
import json

# MENU PRINCIPAL
def mostrar_menu(cfg):
    print(f"\n{'=' * 70}")
    print(f"  {cfg.nombre} v{cfg.version}")
    print(f"  {cfg.empresa}")
    print(f"  {cfg.autor}")
    print(f"{'=' * 70}")
    print("  1. Agregar cliente")
    print("  2. Agregar medicamento")
    print("  3. Registrar venta")
    print("  4. Listar todo cliente")
    print("  5. Listar todo medicamento")
    print("  6. Listar ventas")
    print("  7. Eliminar cliente")
    print("  8. Eliminar medicamento")
    print("  9. Actualizar cliente")
    print("  10. Actualizar medicamento")
    print("  11. Ventas por cliente")
    print("  12. Ver clientes en JSON")
    print("  13. Ver medicamentos en JSON")
    print("  14. Ver ventas JSON")
    print("  15. Ver historial de logs")
    print("  16. Limpiar historial de logs")
    print("  0. Salir")
    print(f"{'=' * 70}")
    
# AGREGAR CLIENTE
def agregar_cliente(cdao):
    print("\n--- AGREGAR CLIENTE ---")
    nomb_cli = input("  Nombre    : ")
    ape_cli  = input("  Apellido  : ")
    dni      = input("  DNI       : ")
    telefono = input("  Telefono  : ")
    try:
        c = cdao.insertar(Cliente(nomb_cli, ape_cli, dni, telefono))
        print(f" OK Cliente agregado con ID = {c.id_cliente}")
    except DNIDuplicadoError as ex:
        print(f" ERROR: {ex}")

# AGREGAR MEDICAMENTO       
def agregar_medicamento(mdao):
    print("\n--- AGREGAR MEDICAMENTO ---")
    nomb_med = input("  Nombre : ")
    try:
        precio = float(input("  Precio : "))
        stock  = int(input("  Stock  : "))
        m = mdao.insertar(Medicamento(nomb_med, precio, stock))
        print(f" OK Medicamento agregado con ID = {m.id_medicamento}")
    except ValueError:
        print(" ERROR: El precio y el stock deben ser números.") 
    
# REGISTRAR VENTA  
def registrar_venta(cdao, mdao, vdao):
    print("\n--- REGISTRAR VENTA ---")

    listar_todocliente(cdao)
    listar_todomedicamento(mdao)

    try:
        cliente_id = int(input("  ID del cliente      : "))
        medicamento_id = int(input("  ID del medicamento  : "))
        cantidad = int(input("  Cantidad            : "))
        
        c = cdao.buscar_por_id(cliente_id)
        m = mdao.buscar(medicamento_id)
        
        if not c:
            print(f" ERROR: Cliente ID={cliente_id} no existe.")
            return
        if not m:
            print(f" ERROR: Medicamento ID={medicamento_id} no existe.")
            return
        
        if cantidad <= 0:
            print(" ERROR: La cantidad debe ser mayor que cero.")
            return

        if cantidad > m.stock:
            print(f" ERROR: Stock insuficiente. Stock disponible: {m.stock}")
            return
        
        total = round(m.precio * cantidad, 2)
        
        v = vdao.registrar(Venta(cliente_id, medicamento_id, cantidad, total))
        print(f" OK Venta registrada con ID={v.id_venta}")
        print(f" Total de la venta: s/. {total:.2f}")
    except ValueError:
        print(" ERROR: Los datos ingresados son inválidos.")

# LISTARTODO CLIENTE 

def listar_todocliente(cdao):
    print("\n--- CLIENTES ---")
    clientes = cdao.obtener_todos()
    if clientes:
        for c in clientes:
            print(f" {c}")
    else:
        print(" (No hay clientes registrados.)")
    
# LISTARTODO MEDICAMENTO     
def listar_todomedicamento(mdao):
    print("\n--- MEDICAMENTOS ---")
    medicamentos = mdao.obtener_todos()
    if medicamentos:
        for m in medicamentos:
            print(f" {m}")
    else:
        print(" (No hay medicamentos registrados.)")
        
# LISTAR VENTAS    
def listar_ventas(vdao):
    print("\n--- VENTAS ---")
    filas = vdao.obtener_todos()
    if filas:
        for f in filas:
            print(f"[{f['id_venta']}] {f['nomb_cli']} | compró: {f['nomb_med']} | Cantidad: {f['cantidad']} | Total: S/. {f['total']:.2f} | Fecha: {f['fecha_venta']}")
    else:
        print(" (No hay ventas registradas)")
                      
# ELIMINAR CLIENTE
def eliminar_cliente(cdao):
    print("\n--- ELIMINAR CLIENTE ---")
    try:
        cliente_id = int(input("  ID del cliente a eliminar: "))
        cdao.eliminar(cliente_id)
        print(f" OK Cliente con ID = {cliente_id} eliminado.")
    except ClienteNoEncontradoError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: El ID debe ser un número entero.")
        
# ELIMINAR MEDICAMENTO
def eliminar_medicamento(mdao):
    print("\n--- ELIMINAR MEDICAMENTO ---")
    try:
        medicamento_id = int(input("  ID del medicamento a eliminar: "))
        mdao.eliminar(medicamento_id)
        print(f" OK Medicamento ID = {medicamento_id} eliminado.")
    except MedicamentoNoEncontradoError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: El ID debe ser un número entero.") 
             
# ACTUALIZAR CLIENTE
def actualizar_cliente(cdao):
    print("\n--- ACTUALIZAR CLIENTE ---")

    try:
        cliente_id = int(input("  ID del cliente a actualizar: "))
        nomb_cli = input("  Nuevo Nombre     (Enter para no cambiar): ").strip()
        ape_cli  = input("  Nuevo Apellido   (Enter para no cambiar): ").strip()
        telefono = input("  Nuevo Telefono   (Enter para no cambiar): ").strip()
        c = cdao.actualizar(cliente_id, nomb_cli or None, ape_cli or None, telefono or None)
        print(f" OK Cliente actualizado: {c}")
    except ClienteNoEncontradoError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: El ID debe ser un número entero.")
              
# ACTUALIZAR MEDICAMENTO
def actualizar_medicamento(mdao):
    print("\n--- ACTUALIZAR MEDICAMENTO ---")

    try:
        medicamento_id = int(input("  ID del medicamento a actualizar: "))
        nomb_med   = input("  Nuevo Nombre (Enter para no cambiar): ").strip()
        precio_str = input("  Nuevo Precio (Enter para no cambiar): ").strip()
        stock_str  = input("  Nuevo Stock  (Enter para no cambiar): ").strip()
        precio = float(precio_str) if precio_str else None
        stock = int(stock_str) if stock_str else None
        m = mdao.actualizar(medicamento_id, nomb_med or None, precio,stock)
        print(f" OK Medicamento actualizado: {m}")
    except MedicamentoNoEncontradoError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: El ID debe ser entero, el precio decimal y el stock entero.")
   
# VENTAS POR CLIENTE    
def ventas_por_cliente(cdao, vdao):
    print("\n--- VENTAS POR CLIENTE ---")

    listar_todocliente(cdao)
    try:
        cliente_id = int(input("  ID del cliente: "))
        filas = vdao.buscar_por_cliente(cliente_id)
        if filas:
            for f in filas:
                print(f" [{f['id_venta']}] Medicamento: {f['nomb_med']} | Cantidad: {f['cantidad']} | Total: {f['total']:.2f} | Fecha: {f['fecha_venta']} ")
        else:
            print(" (Este cliente no tiene ventas registradas)")
    except ValueError:
        print(" ERROR: El ID debe ser un número entero.")
 
# VER CLIENTES JSON
def ver_clientes_json(cdao):
    print("\n--- CLIENTES EN JSON ---")
    clientes = cdao.obtener_todos()
    if clientes:
        datos = [c.to_dict() for c in clientes]
        print(json.dumps(datos, indent=4, ensure_ascii=False))
    else:
        print(" (No hay clientes registrados.)")

# VER MEDICAMENTOS JSON
def ver_medicamentos_json(mdao):
    print("\n--- MEDICAMENTOS EN JSON ---")
    medicamentos = mdao.obtener_todos()
    if medicamentos:
        datos = [m.to_dict() for m in medicamentos]
        print(json.dumps(datos, indent=4, ensure_ascii=False))
    else:
        print(" (No hay medicamentos registrados.)")
        
# VER VENTAS JSON
def ver_ventas_json(vdao):
    print("\n--- VENTAS EN JSON ---")
    ventas = vdao.obtener_todos()
    if ventas:
        datos = [dict(v) for v in ventas]
        #datos = [v.to_dict() for v in ventas]
        print(json.dumps(datos, indent=4, ensure_ascii=False))
    else:
        print("  (No hay ventas registradas)")