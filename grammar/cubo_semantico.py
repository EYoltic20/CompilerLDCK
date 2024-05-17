# Definir los tipos
INT = 'int'
FLOAT = 'float'
BOOL = 'bool'

# Operaciones soportadas
PLUS = '+'
MINUS = '-'
TIMES = '*'
DIVIDE = '/'

cubo_semantico = {
    INT: {
        INT: {
            PLUS: INT, MINUS: INT, TIMES: INT, DIVIDE: FLOAT
        },
        FLOAT: {
            PLUS: FLOAT, MINUS: FLOAT, TIMES: FLOAT, DIVIDE: FLOAT
        }
    },
    FLOAT: {
        INT: {
            PLUS: FLOAT, MINUS: FLOAT, TIMES: FLOAT, DIVIDE: FLOAT
        },
        FLOAT: {
            PLUS: FLOAT, MINUS: FLOAT, TIMES: FLOAT, DIVIDE: FLOAT
        }
    }
    # Agregar más tipos y operaciones según sea necesario
}
def verificar_tipo(tipo1, tipo2, operador):
    try:
        return cubo_semantico[tipo1][tipo2][operador]
    except KeyError:
        raise TypeError(f"Operación no permitida entre {tipo1} y {tipo2} con el operador {operador}")