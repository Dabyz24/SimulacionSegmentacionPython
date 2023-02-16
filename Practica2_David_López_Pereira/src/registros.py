class Registros:

    registros = {}

    # Inicializo los 32 registros de Mips
    def __init__(self):
        self.registros["zero"] = 0  # $zero constante para el cero
        self.registros["at"] = 0    # $at temporal para el ensamblador
        for i in range(2):
            self.registros["v" + str(i)] = 0  # $v0 - $v1  valores para resultados
        for i in range(4):
            self.registros["a" + str(i)] = 0  # $a0 - $a3  argumentos
        for i in range(8):
            self.registros["s" + str(i)] = 0  # $s0 - $s7  temporales guardados
        for i in range(10):
            self.registros["t" + str(i)] = 0  # $t0 - $t9  temporales
        for i in range(2):
            self.registros["k" + str(i)] = 0   # $k0 - k1 reservados para el kernel
        self.registros["gp"] = 0  # $gp puntero global
        self.registros["sp"] = 0  # $sp puntero de pila
        self.registros["fp"] = 0  # $fp puntero de marco
        self.registros["ra"] = 0  # $ra direccion de retorno

    # Getters y setters para modificar los atributos de la clase
    def getRegistro(self, registro):
        return self.registros[registro]

    def setRegistro(self, registro, valor):
        self.registros[registro] = valor

    def getRegistros(self):
        return self.registros

    def __str__(self):
        return self.registros

