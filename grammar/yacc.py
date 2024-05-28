
import ply.yacc as yacc
from lexeer import tokens
from direccionfunc import DirectorioFunciones
# Instancia global del directorio de funciones
directorio = DirectorioFunciones()
from duckast import *
from vm import *
            
            
def get_direccion_memoria(tipo):
    direccion = direcciones_memoria[tipo]
    direcciones_memoria[tipo] += 1
    return direccion

def get_variable_direccion(nombre, tipo):
    if nombre not in tabla_variables:
        tabla_variables[nombre] = get_direccion_memoria(tipo)
    return tabla_variables[nombre]

# Función para mapear una constante a su dirección de memoria
tabla_constantes = {}           

direcciones_memoria = {
    'int': 1000,
    'float': 2000,
    'bool': 3000,
    
    
}


def get_constante_direccion(valor, tipo):
    if valor not in tabla_constantes:
        tabla_constantes[valor] = get_direccion_memoria(tipo)
    return tabla_constantes[valor]

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
# GUARDAR QUADS EN TXT
def write_cuadruplos_to_file(filename,quads):
    with open(filename, 'w') as f:
        for idx, cuad in enumerate(quads):
            f.write(f'{idx}: {cuad}\n')

def p_empezar(p):
    'empezar : PROGRAM ID SEMICOMMA  var_or_func  END'
    p[0] = programNode(p[2],p[4],p[4])
    quads = p[0].generate_code()
    write_cuadruplos_to_file("cuadruplo.txt",quads)
    run_virtual_machine(quads)
    printpato()

def p_var_or_func(p):
    
    '''var_or_func : vars func_create
                   | func_create'''
    if len(p) == 3:
        p[0] = (p[1],p[2])
    else:
        p[0] = p[1]

    
def p_func_create(p):
    '''func_create : funcs func_create
                   | EMPTY'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []
        
def p_funcs(p):
    'funcs : VOID ID LPAR func_vars RPAR   body  SEMICOMMA'
    p[0] = funcsNode(p[1],p[2],p[4],p[6])
        
def p_body(p):
    'body : LBRACE statment RBRACE '
    p[0] = BodyNode(p[2])
    
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
                 | vars statment
                 | EMPTY'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]


def p_assign(p):
    '''assign : ID EQ expression SEMICOMMA'''
              
    # id_mem = get_variable_direccion(p[1], 'int')  # Asumimos tipo 'int' para simplicidad
    
    p[0] = AssignNode(p[1], p[3])
    
    
    
    

def p_cte(p):
    '''cte : CTE_INT
           | CTE_FLOAT PUNTO CTE_INT'''
    if len(p)>2:
        p[0] = LiteralNode(f'{p[1]}{p[2]}{p[3]}')
    else:
        p[0] = LiteralNode(p[1])



def p_func_vars(p):
    '''func_vars : ID DOUBLEPOINT type   func_vars
                 | COMMA func_vars
                 | EMPTY '''
    if len(p) == 6:
        p[0] = [FuncParams(p[1], p[3])] + p[5]
    elif len(p) == 4:
        p[0] = [FuncParams(p[1], p[3])]
    else:
        p[0] = []



def p_expression(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression GT expression
                  | expression GTE expression
                  | expression LT expression
                  | expression LTE expression
                  | expression NT expression
                  | factor
                  | cte'''
    if len(p) == 4:
        p[0] = ExpressionNode(p[1], p[2], p[3])
    else:
        p[0] = p[1]

def p_factor(p):
    '''factor : LPAR expression RPAR
              | ID
              | cte'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        if p.slice[1].type == 'ID':
            p[0] = IdNode(p[1])
        else:
            p[0] = p[1]


def p_cycle(p):
    'cycle : WHILE LPAR expression RPAR  DO  body  SEMICOMMA'
    p[0] = WhileNode(p[3],p[6])
############
def p_fcall(p):
    'fcall : ID LPAR list_exp RPAR SEMICOMMA'
    
    ############ OJO AQUI

def p_list_exp(p):
    '''list_exp : expression list_exp
                | EMPTY
                | COMMA list_exp'''
############    

    
def p_id_cte(p):
    '''id_cte : ID
              | cte'''

def p_conditions(p):
    '''conditions : IF LPAR expression RPAR body haselse SEMICOMMA'''
    p[0]= IfNode(p[3],p[5],p[6])

def p_haselse(p):
    '''haselse : ELSE body
               | EMPTY'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None
    
def p_imprimir(p):
    'imprimir : PRINT LPAR lst_printing_options RPAR SEMICOMMA'
    p[0] = PrintNode(p[3])



def p_lst_printing_options(p):
    '''lst_printing_options : CTE_STRING  COMMA lst_printing_options
                            | expression 
                            | expression COMMA lst_printing_options
                            | vars
                            | vars COMMA lst_printing_options
                            | CTE_STRING'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_vars(p):
    '''vars : VAR lst_var ''' 
    p[0] = p[2]

    
    
    
def p_lst_var(p):
    
    '''lst_var : lst_id DOUBLEPOINT type SEMICOMMA '''
    p[0] = VarListNode(p[1],p[3])           

        


def p_lst_id(p):
    '''lst_id : ID lst_id
              | COMMA lst_id
              | EMPTY'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
 
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        pass

        
def p_type(p):
    '''type : INT
            | FLOAT '''
    p[0]=p[1]
    

def p_empty(p):
    'EMPTY :'
    p[0]=emptyNode()

def p_error(p):
    if p:
        
        printpatotriste(f"Error de sintaxis en el token {p.value}")
    else:
        print("Error de sintaxis en EOF")


# Construir el parser


        
namef = "test.txt"
file = open(namef,'r')
s = file.read()
file.close()
yacc.yacc()
yacc.parse(s)




# vm.run_virtual_machine(cuadruplos,tabla_constantes)



    