from config.logger import Logger
from config.sistema_config import SistemaConfig
from config.persistencia import guardar_clientes, guardar_medicamentos, guardar_ventas, cargar_clientes, cargar_medicamentos, cargar_ventas
from dao.cliente_dao import ClienteDAO
from dao.medicamento_dao import MedicamentoDAO
from dao.venta_dao import VentaDAO
from vistas.menu import mostrar_menu, agregar_cliente, agregar_medicamento, registrar_venta, listar_clientes, listar_medicamentos, listar_ventas, eliminar_cliente, eliminar_medicamento, actualizar_cliente, actualizar_medicamento, eliminar_venta, ver_clientes_json, ver_medicamentos_json, ver_ventas_json


# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================

def main():
    cfg = SistemaConfig()
    cdao = ClienteDAO()
    mdao = MedicamentoDAO()
    vdao = VentaDAO()
    
    cargar_clientes(cdao)
    cargar_medicamentos(mdao)
    cargar_ventas(vdao)
    
    while True:
        mostrar_menu(cfg)
        opcion = input("Seleccione una opción: ")
        
        match opcion:

            case "1": agregar_cliente(cdao)
            case "2": agregar_medicamento(mdao)
            case "3": registrar_venta(vdao)
            case "4": listar_clientes(cdao)
            case "5": listar_medicamentos(mdao)
            case "6": listar_ventas(vdao)
            case "7": actualizar_cliente(cdao)
            case "8": actualizar_medicamento(mdao)
            case "9": eliminar_cliente(cdao)
            case "10": eliminar_medicamento(mdao)
            case "11": eliminar_venta(vdao)
            case "12": ver_clientes_json(cdao)
            case "13": ver_medicamentos_json(mdao)
            case "14": ver_ventas_json(vdao)
            case "15": guardar_clientes(cdao); guardar_medicamentos(mdao); guardar_ventas(vdao)
            case "16": Logger().mostrar_logs()
            case "17": Logger().limpiar()
            case "0":
                guardar_clientes(cdao)
                guardar_medicamentos(mdao)
                guardar_ventas(vdao)
                Logger().info("Sistema cerrado")
                print("\nHasta luego.")
                break
            case _:
                print("Opción inválida.")
                
main()