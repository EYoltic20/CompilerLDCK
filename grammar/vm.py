class VirtualMachine:
    def __init__(self, cuadruplos):
        self.cuadruplos = cuadruplos
        self.memory = {}  # Diccionario para simular la memoria
        self.constantes = {}  # Diccionario para almacenar constantes
        self.labels = {}  # Diccionario para almacenar etiquetas de salto
        self.funciones = 'global'
    def execute(self):
        pc = 0  # Program counter
        self.prepare_labels()

        while pc < len(self.cuadruplos):
            cuad = self.cuadruplos[pc]
            op = cuad[0]
            arg1 = cuad[1]
            arg2 = cuad[2]
            result = cuad[3]

            # print(f'Executing: {cuad}')  # Depuración


            if op == '=':
                # Si se le asigno el valor a una var
                if(self.memory[self.funciones][arg1]):
                    self.memory[self.funciones][arg1]['value'] = self.get_value(arg2)
                
            elif op == '+':
                self.memory[self.funciones][result] = self.get_value(arg1) + self.get_value(arg2)
            elif op == '-':
                self.memory[self.funciones][result] = self.get_value(arg1) - self.get_value(arg2)
            elif op == '*':
                self.memory[self.funciones][result] = self.get_value(arg1) * self.get_value(arg2)
            elif op == '/':
                self.memory[self.funciones][result] = self.get_value(arg1) / self.get_value(arg2)
            elif op == '>':

                self.memory[self.funciones][result] = self.get_value(arg1) > self.get_value(arg2)
            elif op == '<':
                self.memory[self.funciones][result] = self.get_value(arg1) < self.get_value(arg2)
            elif op == '>=':
                self.memory[self.funciones][result] = self.get_value(arg1) >= self.get_value(arg2)
            elif op == '<=':
                self.memory[self.funciones][result] = self.get_value(arg1) <= self.get_value(arg2)  
                
  
    
            elif op == 'PRINT':
                if arg1 not in self.memory[self.funciones]:
                    if isinstance(arg1, str):
                        print(arg1)
                else:  
                    value = self.get_value(arg1)
                    print(value)
                    
            elif op == 'GOTOF':
                if not self.get_value(arg1):
                    pc = self.labels[result] - 1
            elif op == 'GOTOV':
                if self.get_value(arg1):
                    pc = self.labels[result] - 1
            elif op == 'GOTO':
                pc = self.labels[result] - 1
                
            elif op == 'LABEL':
                pass
            
            elif op == 'FUNC':
                self.memory[arg1]={}
                self.funciones =  arg1
            elif op == 'VAL':
                self.memory[self.funciones][arg1] = arg1
            elif op == 'DECL':
                self.memory[self.funciones][arg1] = {
                    "type":arg2,
                    "value":None
                }
            elif op == 'RET':
                break
            elif op == 'END':
                break
            elif op == 'PROGRAM':
                self.memory[self.funciones]={}
            pc += 1

    def prepare_labels(self):
        for idx, cuad in enumerate(self.cuadruplos):
            if cuad[0] == 'LABEL':
                self.labels[cuad[1]] = idx
            elif cuad[0] in {'GOTOF', 'GOTOV', 'GOTO'} and isinstance(cuad[3], str):
                # Asegúrate de que las etiquetas de salto estén en el diccionario
                if cuad[3] not in self.labels:
                    self.labels[cuad[3]] = None  # Inicializar con None para ser actualizado luego

        # Verifica que todas las etiquetas de salto se hayan definido
        for label in self.labels:
            if self.labels[label] is None:
                raise ValueError(f"Etiqueta de salto indefinida: {label}")

    
    def get_value(self, operand):
        if isinstance(operand, (int, float)):
            return operand
        
        if operand in self.constantes:
            return self.constantes[operand]
        # Si es un var
        
        if isinstance(operand, str) and operand.startswith('t'):
        # Handle the case where the operand is a temporary variable
            if operand in self.memory[self.funciones]:
                return self.memory[self.funciones][operand]
        
        if operand in self.memory[self.funciones]:
            return self.memory[self.funciones][operand]['value']
        

        
        if operand in self.memory['global']:
            return self.memory['global'][operand]['value']
        raise ValueError(f"Undefined operand: {operand}")


# Función para iniciar la ejecución de la máquina virtual
def run_virtual_machine(cuadruplos):
    vm = VirtualMachine(cuadruplos)
    vm.execute()
    print(vm.cuadruplos)