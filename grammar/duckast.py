# ast.py

# custom_ast.py

temp_count = 0
label = 0
def new_temp():
    global temp_count
    temp = f't{temp_count}'
    temp_count += 1
    return temp
def new_label():
    global label
    newlabel = f'l{label}'
    label += 1
    return newlabel

class Node:

    def generate_code(self):
        pass

    def print(self, level=0):
        print(" " * level + self.__class__.__name__)

class programNode(Node):
    def __init__(self,identifier,vars,functions):
        self.identifier = identifier
        # CORREGIR VAR GLOBALES
        self.quads = []
        self.vars = vars
        self.functions = functions
        
    def print(self, level=0):
        print(" " * level + "Program")
        print(" " * (level + 2) + "Identifier:", self.identifier)
        print(" " * (level + 2) + "Declarations:")
        for var in self.vars:
            var.print(level + 4)
        print(" " * (level + 2) + "Statements:")
        for function in self.functions:
            function.print(level + 4)    
            
    def generate_code(self):
        quads = []
        quads.append(('PROGRAM',self.identifier,None,None))
        for function in self.functions:
            quads.extend(function.generate_code())
        quads.append(('END',None,None,new_temp()))
        print(quads)
        self.quads = quads
        return quads



class VarListNode(Node):
    def __init__(self, vars,typo):
        super().__init__()
        self.vars = vars
        self.typo = typo
        
    def generate_code(self):
        quads = []
        for var in self.vars:
            if var != ',' :
                if var != None:
                    quads.append(('DECL',var,self.typo,None))
        return quads

    def print(self, level=0):
        super().print(level)
        for var in self.vars:
            var.print(level + 2)


class funcsNode(Node):
    def __init__(self,returnType,id,params,body):
        self.returnType = returnType
        self.id = id
        self.params = params
        self.body = body
    def generate_code(self):
        code = [("FUNC", self.id, None, None)]
        for param in self.params:
            code.extend(param.generate_code())
        body_code = self.body.generate_code()  # Aquí self.body debe ser BodyNode
        if not any(instr[0] == 'RET' for instr in body_code):
            body_code.append(("RET", None,None,None))
        code.extend(body_code)
        return code

class BodyNode(Node):
    def __init__(self, statements):
        super().__init__()
        self.statements = statements

    def generate_code(self):
        quads = []
        for statement in self.statements:
            quads.extend(statement.generate_code())
        return quads

    def print(self, level=0):
        super().print(level)
        for statement in self.statements:
            statement.print(level + 2)

class funcExpression(Node):
    def __init__(self,expresion):
        self.returnType = expresion
    def generate_code(self):
        quads = []
        quads.extend(self.expression.generate_code())
        return quads
        
class FuncParams(Node):
    def __init__(self, id, type):
        super().__init__()
        self.id = id
        self.type = type

    def generate_code(self):
        quads = []
        if self.id == 'x' and self.type == 'x':
            return quads
        else:
            quads.append((self.id, self.type, None, None))
        return quads

    def print(self, level=0):
        super().print(level)
        print(" " * (level + 2) + f"ID: {self.id}")
        print(" " * (level + 2) + f"Type: {self.type}")

class AssignNode(Node):
    def __init__(self, id, expression):
        super().__init__()
        self.id = id
        self.expression = expression
        
    def generate_code(self):
        quads = []
        expr_code = self.expression.generate_code()
        assign_V=expr_code[-1]
        
        quads.extend(expr_code)
        if assign_V[0]  == 'VAL':
            quads.append(('=', self.id, assign_V[1], new_temp()))
        else:
            quads.append(('=', self.id, assign_V[-1], new_temp()))
        return quads
     
class emptyNode(Node):
    def  generate_code(self):
        quads=[('EMPTY',None,None)]
        return quads
        

class ExpressionNode(Node):
    def __init__(self, left, operator, right):
        
        self.left = left
        self.operator = operator
        self.right = right

    def generate_code(self):
        code = []
        left_code = self.left.generate_code()
        right_code = self.right.generate_code()
        code.extend(left_code)
        code.extend(right_code)
        temp = new_temp()
        left_temp = left_code[-1][-1] if isinstance(left_code[-1][-1], str) else left_code[-1][1]
        right_temp = right_code[-1][-1] if isinstance(right_code[-1][-1], str) else right_code[-1][1]
        code.append((self.operator, left_temp, right_temp, temp))
        return code


   
class PrintNode(Node):
    def __init__(self, expressions):
        super().__init__()
        self.expressions = expressions

    def generate_code(self):
        quads = []
        for expr in self.expressions:
            if isinstance(expr, str):
                quads.append(('PRINT', expr, None, None))
     
            else:
                expr_code = expr.generate_code()
                quads.extend(expr_code)
                quads.append(('PRINT', expr_code[0][1], None, None))
        return quads
 
        
class WhileNode(Node):
    def __init__(self, condition, body):
        super().__init__()
        self.condition = condition
        self.body = body

    def generate_code(self):
        quads = []
        start_label = new_label()
        end_label = new_label()
        
        quads.append(('LABEL', start_label, None, None))
        quads.extend(self.condition.generate_code())
        condition_temp = quads[-1][-1]  # Obtener el temporal del último cuádruplo generado
        
        quads.append(('GOTOF', condition_temp, None, end_label))
        quads.extend(self.body.generate_code())
        quads.append(('GOTO', None, None, start_label))
        
        quads.append(('LABEL', end_label, None, None))
        
        return quads

        
        
class IfNode(Node):
    def __init__(self, condition, body, else_body=None):
        super().__init__()
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def generate_code(self):
        quads = []
        else_label = new_label()
        end_label = new_label()
        
        quads.extend(self.condition.generate_code())
        condition_temp = quads[-1][-1]  # Obtener el temporal del último cuádruplo generado
        
        quads.append(('GOTOF', condition_temp, None, else_label))
        quads.extend(self.body.generate_code())
        quads.append(('GOTO', None, None, end_label))
        
        quads.append(('LABEL', else_label, None, None))
        if self.else_body:
            quads.extend(self.else_body.generate_code())
        
        quads.append(('LABEL', end_label, None, None))
        
        return quads

 

class LiteralNode(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def generate_code(self):
        return [("VAL",self.value,None,None)]
    
    
class FloatNode(Node):
    def __init__(self, value,value2):
        super().__init__()
        self.value = float(f'{value}.{value2}')

    def generate_code(self):
        return [("VALFLOAT",self.value,None,None)]


class IdNode(Node):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def generate_code(self):
        return [('LOAD', self.name,None,None)]

