
import ply.yacc as yacc
from lexeer import tokens
from direccionfunc import DirectorioFunciones
# Instancia global del directorio de funciones
directorio = DirectorioFunciones()
stack_funciones = []  # Pila para manejar el contexto de funciones
stack_vars={}

# Lista para almacenar los cuádruplos
cuadruplos = []

# Contador de temporales
temp_count = 0
def printpatotriste(error):
    print(
        f'''     
░░░░░▄█████▄░░░╔═════
░░░█▀█▄▄█▄▄█▀█░║ {error}
░░░▐▄███▒███▄▌═╩═════
░░░░▀██▀▀▀██▀░░░░░░░░
░░░░░▐█████▌░░░░░░░░░

'''
    )
def printpato():
    print(
        '''     __
 ___( o)> cuack bien 
 \ <_. )
  `---'                     
                                                  
                                                  
'''
    )
def new_temp():
    global temp_count
    temp = f't{temp_count}'
    temp_count += 1
    return temp

direcciones_memoria = {
    'int': 1000,
    'float': 2000,
    'bool': 3000,
    
}

def get_direccion_memoria(tipo):
    direccion = direcciones_memoria[tipo]
    direcciones_memoria[tipo] += 1
    return direccion

def hashMap(var,tipo,dir_memoria,assign):
    tvar = {
        "var":var,
        "tipo":tipo,
        "direccion de memoria": dir_memoria,
        "assign":assign
    }    
    return tvar

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    
)
# ME FALTA VARS
def p_empezar(p):
    'empezar : PROGRAM ID SEMICOMMA  var_or_func  END'
    
    printpato()
    # p[0]=(p[1],p[2],p[3],p[4],p[5],p[6],p[7])
    
#  AQUI AGREGAMOS PARA PODER ASSIGNAR LA VARIABLES GLOBALES
# def p_var_global(p):
#     '''var_global : vars var_global
#                   | EMPTY'''

def p_var_or_func(p):
    # '''var_or_func : vars func_create'''    
    '''var_or_func : vars func_create
                   | func_create'''
    # if len(p) == 3 :
    #     p[0]=(p[1],p[2])
    # else:
    #     p[0]=p[1]
    
def p_func_create(p):
    '''func_create : funcs func_create
                   | EMPTY'''
    # if len(p) == 3 :
    #     p[0]=(p[1],p[2])
    # else:
    #     p[0]=p[1]
        
def p_body(p):
    'body : LBRACE statment RBRACE '
    # p[0]=p[2]
def p_statement(p):
    '''statment : assign statment
                 | assign
                 | conditions
                 | conditions statment             
                 | fcall
                 | fcall statment             
                 | imprimir statment
                 | imprimir
                 | cycle statment
                 | cycle
                 | vars
                 | vars statment'''
    # p[0] = p[1]


def p_assign(p):
    '''assign : ID EQ expression SEMICOMMA
              | ID EQ cte SEMICOMMA'''
    nombre_variable = p[1]
    expresion = p[3]
    # Primero verificamos que la variable si haya sido declarada y no spawneada de la nada
    if stack_vars[nombre_variable]:
        stack_vars[nombre_variable]["assign"] = expresion
    else:
        raise Exception(f"Variable {nombre_variable} no ha sido declarada linea ")
    # AQUI ASIGNAMOS EL PRIMER CUADRUPLO , SIN EMBARGO ESTE NO TIENE PREDESEZOR AL DECLARAR VARIABLES
    
    cuadruplos.append(('=',p[3],None,p[1]))
    
    
    

def p_cte(p):
    '''cte : CTE_INT
           | CTE_FLOAT'''
# Asignamos el valor al token 
    p[0] = p[1]


def p_funcs(p):
    'funcs : VOID ID LPAR func_vars RPAR   body  SEMICOMMA'
    # p[0]=(p[4],p[7],p[8])
    nombre_funcion = p[2]
    tipo_retorno = p[1]
    parametros = p[4]
    directorio.agregar_funcion(nombre_funcion, tipo_retorno, parametros)
    
    for key in stack_vars:
  
        variable = stack_vars[key]
        
        if variable['var'] != None:    
            tipo = variable['tipo']
            dir = variable['direccion de memoria']
            assign = variable['assign']
            if assign == None:
                print(f"Variable {variable['var']} declarada pero no usada\t ")
            directorio.agregar_variable(nombre_funcion, variable['var'], tipo, dir,assign)
            
    stack_vars.clear()
    stack_funciones.append(nombre_funcion)
    directorio.funciones[nombre_funcion]['cuadruplos_inicio'] = cuadruplos
    # limpeamos los cuadruplos para poder continuar con las funciones
    cuadruplos.clear
    
    
    
    
  

def p_func_vars(p):
    '''func_vars : ID DOUBLEPOINT type    func_vars
                 | COMMA func_vars
                 | EMPTY '''
    if len(p) == 6:
        p[0] = [(p[1], p[3])] + p[5]
    else:
        p[0] = []




def p_expression(p):
    'expression : exp op'
    
    # ponemos la condicion de que p[2] no sea cero para poder asignarle el token y si no le asignamos la expresion a otro token
    if len(p) == 3 and p[2] is not None:
        p[0] = p[2]
    else:
        p[0] = p[1]


def p_op(p):
    '''op : GT exp
          | GTE exp
          | LT exp
          | LTE exp
          | NT exp
          | EMPTY'''
    # si no es empty generamos un nuevo cuadruplo
    if len(p) == 3:
        temp = new_temp()
        cuadruplos.append((p[1], p[2], None, temp))
        p[0] = temp
    else:
        p[0] = None

def p_exp(p):
    'exp : termino lopb'
    # ausi el token ta tiene termino 
    if len(p) == 3 and p[2] is not None:
        temp = new_temp()
        cuadruplos.append((p[2][0], p[1], p[2][1], temp))
        p[0] = temp
    else:
        p[0] = p[1]

def p_lopb(p):
    '''lopb : PLUS termino
            | MINUS termino
            | EMPTY'''
    if len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = None

def p_termino(p):
    'termino : factor lopa'
    if len(p) == 3 and p[2] is not None:
        temp = new_temp()
        cuadruplos.append((p[2][0], p[1], p[2][1], temp))
        p[0] = temp
    else:
        p[0] = p[1]

def p_lopa(p):
    '''lopa : TIMES factor
            | DIVIDE factor
            | EMPTY'''
    if len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = None

    
def p_cycle(p):
    'cycle : WHILE body DO LPAR expression RPAR SEMICOMMA'
    # p[0] = (p[2],p[5])

def p_fcall(p):
    'fcall : ID LPAR list_exp RPAR SEMICOMMA'
    # p[0] = (p[1],p[2],p[3],p[4],p[5])

def p_list_exp(p):
    '''list_exp : expression list_exp
                | EMPTY
                | COMMA list_exp'''
    # if len(p) == 3:
    #         p[0] = (p[1],p[2])
    # else:
    #     pass

def p_factor(p):
    '''factor : LPAR expression RPAR
              | lopb id_cte
              | id_cte'''
    if len(p) == 4:
            p[0] = p[2]
    elif len(p) == 3:
        temp = new_temp()
        cuadruplos.append((p[1][0], p[1][1], p[2], temp))
        p[0] = temp
    else:
        p[0] = p[1]
    
def p_id_cte(p):
    '''id_cte : ID
              | cte'''
    p[0]=p[1]

def p_conditions(p):
    '''conditions : IF LPAR expression RPAR body haselse SEMICOMMA'''
    # p[0] = (p[1],p[2],p[3],p[4],p[5],p[6])
def p_haselse(p):
    '''haselse : ELSE body
               | EMPTY'''
    # if len(p) == 3:
    #         p[0] = (p[1],p[2])
    # else:
    #     pass
    
def p_imprimir(p):
    'imprimir : PRINT LPAR lst_printing_options RPAR SEMICOMMA'
    # p[0] = (p[1],p[2],p[3],p[4],p[5])

def p_lst_printing_options(p):
    '''lst_printing_options : CTE_STRING  COMMA lst_printing_options
                            | expression 
                            | expression COMMA lst_printing_options
                            | vars
                            | vars COMMA lst_printing_options
                            | CTE_STRING'''
                            
    # if len(p) == 3:
    #         p[0] = (p[1],p[2])
    # else:
    #     pass
def p_vars(p):
    '''vars : VAR lst_var''' 
    # p[0]=(p[1],p[2])
def p_lst_var(p):
    
    '''lst_var : lst_id DOUBLEPOINT type SEMICOMMA 
               | EMPTY'''
    tipo = p[3]
    for var in p[1]:
        if var != ",":
            direccion_memoria = get_direccion_memoria(tipo)
            hash = hashMap(var,tipo,direccion_memoria,None)
            stack_vars[var]=hash
        
        


def p_lst_id(p):
    '''lst_id : ID lst_id
              | COMMA lst_id
              | EMPTY'''

    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = []   
        
def p_type(p):
    '''type : INT
            | FLOAT
            | VOID '''
    p[0] = p[1]

def p_empty(p):
    'EMPTY :'
    pass

def p_error(p):
    if p:
        
        printpatotriste(f"Error de sintaxis en el token {p.value}")
    else:
        print("Error de sintaxis en EOF")


# Construir el parser

# Función para imprimir los cuádruplos
def print_cuadruplos():
    for idx, cuad in enumerate(cuadruplos):
        print(f'{idx}: {cuad}')
        
namef = "test.txt"
file = open(namef,'r')
s = file.read()
file.close()
yacc.yacc()
result = yacc.parse(s)
print_cuadruplos()
print(directorio.funciones)



    