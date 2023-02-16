class Instruccion:

    def __init__(self):
        self.tipo = ""  # Tipo de instruccion
        self.operacion = ""  # operacion a realizar
        self.rDestino = "zero"  # Registro destino, al poner zero cuando llamemos a registros se pondra a 0 el valor
        self.rFuente1 = "zero"  # Registro fuente 1
        self.rFuente2 = "zero"  # Registro fuente 2
        self.etiqueta = ""  # Etiqueta de la instruccion, si no tiene etiqueta sera vacio
        self.desplazamiento = -1  # Para desplazar instrucciones LW y SW
        self.inmediato = -1  # si la instruccion tiene inmediato
        self.etapa = "ID"  # ID sera la etapa inicial

    # Con esta funcion podremos leer los atributos tipicos de una instruccion
    def obtenerInstruccion(self, instruccion):
        operandos = instruccion.split(",")  # Separo la lista para identificar las operaciones y los registros
        operacion = operandos[0].split(" ")  # Separo la primera parte de la lista anterior para separa el primer registro de la operacion
        if operacion[0] == "add" or operacion[0] == "sub" or operacion[0] == "mul" or operacion[0] == "div":
            self.tipo = "R"
            self.operacion = operacion[0]
            self.rDestino = operacion[1].replace("$", "")  # Quito el $ de los registros para solo trabajar con la letra y num
            self.rFuente1 = operandos[1].replace("$", "")
            self.rFuente2 = operandos[2].replace("$", "")
        elif operacion[0] == "lw":
            self.tipo = "I"
            self.operacion = operacion[0]
            self.rDestino = operacion[1].replace("$", "")
            aux = operandos[1].split("(")  # Separo la lista en 2 para obtener desplazamiento y en otra lista el registro
            self.rFuente1 = aux[1].replace("$","").replace(")","")  # El registro aparece con un ) al final por lo que lo quito
            self.desplazamiento = int(aux[0])/4  # Divido por 4 para saber cuantas palabras esta desplazado
        elif operacion[0] == "sw":
            self.tipo = "I"
            self.operacion = operacion[0]
            self.rFuente1 = operacion[1].replace("$", "")
            aux = operandos[1].split("(")
            self.rDestino = aux[1].replace("$", "").replace(")","")
            self.desplazamiento = int(aux[0]) / 4

        elif operacion[0] == "li":
            self.tipo = "I"
            self.operacion = operacion[0]
            self.rDestino = operacion[1].replace("$", "")
            self.inmediato = int(operandos[1])
        elif operacion[0] == "addi":
            self.tipo = "I"
            self.operacion = operacion[0]
            self.rDestino = operacion[1].replace("$", "")
            self.rFuente1 = operandos[1].replace("$", "")
            self.inmediato = int(operandos[2])
        elif operacion[0] == "j":
            self.tipo = "J"
            self.operacion = operacion[0]
            self.etiqueta = operacion[1]
        elif operacion[0] == "bgt" or operacion[0] == "bet" or operacion[0] == "beq" or operacion[0] == "bne" or operacion[0] == "blt" or operacion[0] == "ble":
            self.tipo = "J"
            self.operacion = operacion[0]
            self.rFuente1 = operacion[1].replace("$","")
            self.rFuente2 = operandos[1].replace("$","")
            self.etiqueta = operandos[2]

    # Definicion de todos los getters y setters para modificar los atributos de la clase
    def getOperacion(self):
        return self.operacion

    def setOperacionIns(self, op):
        self.operacion = op

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo = tipo

    def getRegistroDestino(self):
        return self.rDestino

    def setRegistroDestino(self, registro):
        self.rDestino = registro

    def getRegistroFuente1(self):
        return self.rFuente1

    def setRegistroFuente1(self, registro):
        self.rFuente1 = registro

    def getRegistroFuente2(self):
        return self.rFuente2

    def setRegistroFuente2(self, registro):
        self.rFuente2 = registro

    def getEtiqueta(self):
        return self.etiqueta

    def setEtiqueta(self, etiqueta):
        self.etiqueta = etiqueta

    def getDesplazamiento(self):
        return int(self.desplazamiento)

    def setDesplazamiento(self, des):
        self.desplazamiento = des

    def getInmediato(self):
        return self.inmediato

    def setInmediato(self, inm):
        self.inmediato = inm

    def getEtapa(self):
        return self.etapa

    def setEtapa(self, etapa):
        self.etapa = etapa

    def __str__(self):
        return "tipo ", self.tipo, " operacion ", self.operacion, "destino ", self.rDestino, "fuente1",\
               self.rFuente1, "Fuente 2", self.rFuente2, "etiqueta ", self.etiqueta,"Desplazamiento",self.desplazamiento,\
               "inmediato ", self.inmediato, "etapa ", self.etapa

