from config.logger import Logger

# CONFIGURACION DEL SISTEMA (Singleton)

class SistemaConfig:
    _instancia = None
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.nombre = "SISTEMA INTEGRAL GESTIÓN DE FARMACIA"
            cls._instancia.version = "1.0"
            cls._instancia.empresa = "Instituto de Educación Superior Tecnológico Público ARGENTINA "
            cls._instancia.autor = "Angel Flores"
            Logger().info(
                f"Sistema iniciado: {cls._instancia.nombre} Version :{cls._instancia.version} Empresa :{cls._instancia.empresa} Autor :{cls._instancia.autor}")
        return cls._instancia