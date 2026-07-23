from config.logger import Logger
from config.sistema_config import SistemaConfig
from config.base_datos import inicializar
from dao.cliente_dao import ClienteDAO
from dao.medicamento_dao import MedicamentoDAO
from dao.venta_dao import VentaDAO

from vistas.menu import (
    mostrar_menu,
    agregar_cliente,
    agregar_medicamento,
    listar_todocliente,
    listar_todomedicamento,
    eliminar_cliente,
    eliminar_medicamento,
    actualizar_cliente,
    actualizar_medicamento,
    registrar_venta,
    listar_ventas,
    ventas_por_cliente,
    ver_clientes_json,
    ver_medicamentos_json,
    ver_ventas_json
)

# PROGRAMA PRINCIPAL
def main():

    inicializar()

    cfg = SistemaConfig()
    cdao = ClienteDAO()
    mdao = MedicamentoDAO()
    vdao = VentaDAO()

    while True:
        mostrar_menu(cfg)
        opcion = input("  Elige una opción: ").strip()

        match opcion:
            
            case "1": agregar_cliente(cdao)
            case "2": agregar_medicamento(mdao)
            case "3": registrar_venta(cdao, mdao, vdao)
            case "4": listar_todocliente(cdao)
            case "5": listar_todomedicamento(mdao)
            case "6": listar_ventas(vdao)
            case "7": eliminar_cliente(cdao)
            case "8": eliminar_medicamento(mdao)
            case "9": actualizar_cliente(cdao)
            case "10": actualizar_medicamento(mdao)
            case "11": ventas_por_cliente(cdao, vdao)
            case "12": ver_clientes_json(cdao)
            case "13": ver_medicamentos_json(mdao)
            case "14": ver_ventas_json(vdao)
            case "15": Logger().mostrar_logs()
            case "16": Logger().limpiar()
            case "0":
                Logger().info("Sistema cerrado por el usuario")
                print("\nHasta luego.")
                break
            case _:
                print("Opción no válida.")


main()