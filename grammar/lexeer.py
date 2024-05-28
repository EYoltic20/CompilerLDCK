# IMPORTAMOS LEX

__author__ = "EmilioY A01540484"
__version__ = "Version beta"
import ply.lex as lex

# importamos las listas de token con las palabras resevadas



RESERVED = {
    'var': 'VAR',
    'do': 'DO',
    'void': 'VOID',
    'end': 'END',
    # 'main': 'MAIN',
    'else': 'ELSE',
    'while': 'WHILE',
    'print': 'PRINT',
    'if': 'IF',
    'float': 'FLOAT',
    'int': 'INT',
    'program':'PROGRAM',
    # 'BOOL':'BOOL'x
}

tokens = [
    'RPAR',
    'LPAR',
    'PLUS',
    'MINUS',
    'GT',
    'LT',
    'GTE',
    'LTE',
    'SEMICOMMA',
    'COMMA',
    'DOUBLEPOINT',
    'LBRACE',
    'RBRACE',
    'NT',
    'EQ',
    'TIMES',
    'DIVIDE',
    'ID',
    'CTE_FLOAT',
    'CTE_INT',
    'CTE_STRING',
    'CTE_BOOL',
    'PUNTO'
] + list(RESERVED.values())

t_RPAR = r'\)'
t_LPAR = r'\('
t_PLUS = r'\+'
t_MINUS  = r'-'
t_GT = r'<'
t_LT = r'>'
t_GTE = r'<='
t_LTE = r'>='
t_SEMICOMMA = r'\;'
t_COMMA = r','
t_DOUBLEPOINT = r':'
t_LBRACE = r'\{'
t_RBRACE = r'}'
t_NT = r'!='
t_EQ = r'='
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_PUNTO=r'\.'


t_ignore = ' \t'
# Regular expression for identifiers
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = RESERVED.get(t.value,'ID')
    return t
def t_CTE_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    return t
# Regular expression for matching numbers
def t_CTE_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

# def t_CTE_STRING(t):
#     r'\"[a-zA-Z_][a-zA-Z0-9_]*"'
#     t.value = str(t.value)
#     return t

def t_CTE_FLOAT(t):
    r'\d+.\d+'
    t.value = float(t.value)
    return t


def t_newLine(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


        
    

#  de esta manera se genera la clase 
# m = DuckLexer()
# a = lex.lex(object=DuckLexer)

lexer = lex.lex()
# namef = "test.txt"
# file = open(namef,'r')
# s = file.read()
# lexer.input(s)


# # data = "print(cola)"
# # lexer.input(data)

# while True:
#     token = lexer.token()
#     if not token:
#         break
#     print(token)