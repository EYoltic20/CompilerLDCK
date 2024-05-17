#---
# LittleDuck reglex and 
#---
import sys
import ply.lex as lex 
import ply.yacc as yacc

#Inicital tokens
tokens = [
    'PLUS','MINUS','TIMES','DIVIDE',
    'ID','EQUAL','GREATER_THAN','SMALLER_THAN',
    'DIFFERENT','LPARENT','RPARENT','LBRACE','RBRACE',
    'CTEI','CTEF','COMMA','SEMICOLON','COLON', 'STRING'
]

#Regular Expressions for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUAL = r'\='
t_DIFFERENT = r'<>'
t_GREATER_THAN = r'>'
t_SMALLER_THAN = r'<'
t_LPARENT = r'\('
t_RPARENT = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_SEMICOLON = r';'
t_COLON = r':'
t_CTEI = r'[0-9]+'
t_CTEF = r'[0-9]+\.[0-9]+'
t_STRING = r'"([^\\"\n]+|\\.)*"'

reserved = {
    'if' : 'COND_IF',
    'else' : 'COND_ELSE',
    'print' : 'PRINT',
    'var' : 'VAR',
    'program' : 'STARTPROGRAM',
    'int' : 'INT',
    'float':'FLOAT',
}

#Adding reserved words to tokens
tokens = tokens + list(reserved.values())

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

#To ignore whitespaces in code file
t_ignore = r' '

def t_error(t):
    print("Error en caracter '%s'" % t.value[0])
    t.lexer.skip(1)

# Building the lexer
lex.lex()

#Grammatic rules
def p_programa(p):
    ''' programa : STARTPROGRAM ID SEMICOLON bloque
                | STARTPROGRAM ID SEMICOLON vars bloque
    '''

def p_vars(p):
    ''' vars : VAR vars2
    '''

def p_vars2(p):
    ''' vars2 : vars3 COLON tipo SEMICOLON vars2
                | vars3 COLON tipo SEMICOLON 
    '''

def p_vars3(p):
    ''' vars3 : ID
            | ID COMMA vars3
    '''

def p_tipo(p):
    ''' tipo : INT
            | FLOAT
    '''

def p_bloque(p):
    ''' bloque : LBRACE estatuto2 RBRACE
                | LBRACE RBRACE
    '''

def p_estatuto2(p):
    ''' estatuto2 : estatuto
                | estatuto2 estatuto 
    '''

def p_estatuto(p):
    ''' estatuto : asignacion
                | condicion
                | escritura
    '''
def p_asignacion(p):
    ''' asignacion : ID EQUAL expresion SEMICOLON
    '''

def p_condicion(p):
    '''condicion : COND_IF LPARENT expresion RPARENT bloque SEMICOLON
                | COND_IF LPARENT expresion RPARENT bloque COND_ELSE bloque SEMICOLON
    '''

def p_escritura(p):
    ''' escritura : PRINT LPARENT escrituraGrammar RPARENT SEMICOLON
    '''

def p_escrituraGrammar(p):
    ''' escrituraGrammar : expresion
                        | expresion COMMA escrituraGrammar
                        | varcte
                        | varcte COMMA escrituraGrammar
    '''

def p_expresion(p):
    ''' expresion : exp
                | exp GREATER_THAN exp
                | exp SMALLER_THAN exp
                | exp DIFFERENT exp
    '''

def p_exp(p):
    ''' exp : termino
            | termino exp2
    '''

def p_exp2(p):
    '''exp2 : PLUS exp
            | MINUS exp
    '''

def p_termino(p):
    ''' termino : factor
            | factor termino2
    '''

def p_termino2(p):
    ''' termino2 : TIMES termino
                | DIVIDE termino
    '''

def p_factor(p):
    ''' factor : LPARENT expresion RPARENT
            | PLUS varcte
            | MINUS varcte
            | varcte
    '''

def p_varcte(p):
    ''' varcte : ID
            | CTEF
            | CTEI
            | STRING
    '''
def p_error(p):
    if p:
        print(f"Error de sintaxis en el token {p.value}")
    else:
        print("Error de sintaxis en EOF")


#Creating praser
yacc.yacc()

#to check if file exists
try:
    namef = "test.txt"
    file = open(namef,'r')
    s = file.read()
    file.close()
    result = yacc.parse(s)
except Exception as e:
    print(e.args)
#Prase file using own grammar

# print(result) 
print("El codigo fue admitido")