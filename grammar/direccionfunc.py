class DirectorioFunciones:
    def __init__(self):
        self.funciones = {}

    def agregar_funcion(self, nombre, tipo_retorno, parametros):
        if nombre in self.funciones:
            raise Exception(f"Función {nombre} ya declarada.")
        self.funciones[nombre] = {
            'tipo_retorno': tipo_retorno,
            'parametros': parametros,
            'tabla_variables': {},
            'cuadruplos_inicio': None
        }

    def agregar_variable(self, nombre_funcion, nombre_variable, tipo, direccion_memoria):
        if nombre_funcion not in self.funciones:
            raise Exception(f"Función {nombre_funcion} no existe.")
        if nombre_variable in self.funciones[nombre_funcion]['tabla_variables']:
            raise Exception(f"Variable {nombre_variable} ya declarada en función {nombre_funcion}.")
        self.funciones[nombre_funcion]['tabla_variables'][nombre_variable] = {
            'tipo': tipo,
            'direccion_memoria': direccion_memoria
        }


directorio = DirectorioFunciones()
