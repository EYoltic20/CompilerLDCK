
import ply.yacc as yacc
from lexeer import tokens
from direccionfunc import DirectorioFunciones
# Instancia global del directorio de funciones
directorio = DirectorioFunciones()
stack_funciones = ['global']  # Pila para manejar el contexto de funciones
direcciones_memoria = {
    'int': 1000,
    'float': 2000,
    'bool': 3000,
    'char': 4000
}

def get_direccion_memoria(tipo):
    direccion = direcciones_memoria[tipo]
    direcciones_memoria[tipo] += 1
    return direccion

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    
)
# ME FALTA VARS
def p_empezar(p):
    'empezar : PROGRAM ID SEMICOMMA var_or_func  END'
    print("Todo perfect")
    # p[0]=(p[1],p[2],p[3],p[4],p[5],p[6],p[7])
    

def p_var_or_func(p):
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
                 | vars
                 | vars statment'''
    # p[0] = p[1]


def p_assign(p):
    '''assign : ID EQ expression SEMICOMMA
              | ID EQ cte SEMICOMMA'''
    nombre_variable = p[1]
    expresion = p[3]
    # Aquí debes validar el tipo y hacer la asignación
    pass

def p_cte(p):
    '''cte : CTE_INT
           | CTE_FLOAT'''
    p[0] = p[1]

def p_funcs(p):
    'funcs : VOID ID LPAR func_vars RPAR   body  SEMICOMMA'
    # p[0]=(p[4],p[7],p[8])
    nombre_funcion = p[2]
    tipo_retorno = 'void'
    parametros = p[4]
    directorio.agregar_funcion(nombre_funcion, tipo_retorno, parametros)
    stack_funciones.append(nombre_funcion)
  

def p_func_vars(p):
    '''func_vars : ID DOUBLEPOINT type  COMMA  func_vars
                 |  EMPTY '''
    if len(p) == 6:
        p[0] = [(p[1], p[3])] + p[5]
    else:
        p[0] = []




def p_expression(p):
    'expression : exp op'
    # p[0]=(p[1],p[2])

def p_op(p):
    '''op : GT exp
          | GTE exp
          | LT exp
          | LTE exp
          | NT exp
          | EMPTY'''
    # p[0]=p[1]

def p_exp(p):
    'exp : termino lopb'
    # p[0]=(p[1],p[2])

def p_lopb(p):
    '''lopb : PLUS termino
            | MINUS termino
            | EMPTY'''
    # if(p[1] == '+'):p[0]= +p[2]
    # if(p[1] == '-'):p[0]= -p[2]
    # else:pass

def p_termino(p):
    'termino : factor lopa'
    # p[0]=(p[1],p[2])

def p_lopa(p):
    '''lopa : TIMES factor
            | DIVIDE factor
            | EMPTY'''
    # if(p[1] == '*'):p[0]= +p[2]
    # if(p[1] == '/'):p[0]= -p[2]
    # else:pass
    
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
    # if len(p) == 4:
    #     p[0] = (p[1],p[2],p[4])
    # elif(len(p)==3):
    #     p[0] = (p[1],p[2])
    # else:
    #     pass
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

    if len(p) == 6:
        nombre_funcion_actual = stack_funciones[-1]
        tipo = p[3]
        for var in p[1]:
            direccion_memoria = get_direccion_memoria(tipo)
            directorio.agregar_variable(nombre_funcion_actual, var, tipo, direccion_memoria)

def p_lst_id(p):
    '''lst_id : ID lst_id
              | COMMA lst_id
              | EMPTY'''
    # if len(p) == 3:
    #     p[0] = (p[1],p[2])
    # else:
    #     pass
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
        print(f"Error de sintaxis en el token {p.value}")
    else:
        print("Error de sintaxis en EOF")


# Construir el parser
try:
    namef = "test.txt"
    file = open(namef,'r')
    s = file.read()
    file.close()
    yacc.yacc()
    result = yacc.parse(s)
    print(stack_funciones)
except Exception as e:
    print(e.args)



    