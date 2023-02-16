class Alu:
    # Con esta clase simularemos el funcionamiento de la unidad aritmetico logica, asi como el control de la alu
    def __init__(self):
        self.primerOperando = 0
        self.segundoOperando = 0
        self.resultado = 0
        self.zero = 0
        self.controlOperacion = ""

    # En funcion de los valores de aluOp1 y aluOp2 y de la operacion de la instruccion establecemos la operacion a realizar
    def setOperacion(self, aluOp1, aluOp2, instruccion):
        if (aluOp1 == 0 and aluOp2 == 0) or ((aluOp1 == 1 and aluOp2 == 0) and instruccion.getOperacion() == "add"):
            # aluOp == "00" para lw y sw
            self.controlOperacion = "+"
        elif ((aluOp1 == 1 and aluOp2 == 0) and instruccion.getOperacion() == "sub") or (aluOp1 == 0 and aluOp2 == 1):
            # aluOp 10 para sub y aluOp 01 se realiza para operaciones beq donde la alu realizara una resta
            self.controlOperacion = "-"
        elif (aluOp1 == 1 and aluOp2 == 0) and instruccion.getOperacion() == "mul":
            self.controlOperacion = "*"
        elif (aluOp1 == 1 and aluOp2 == 0) and instruccion.getOperacion() == "div":
            self.controlOperacion = "/"
        return self.controlOperacion

    # Una vez obtenida la operacion en funcion de cual sea lo traduciomos a lenguaje python
    def calcular(self, primer, segundo, operacion):
        self.primerOperando = primer
        self.segundoOperando = segundo
        self.controlOperacion = operacion
        if self.controlOperacion == "+":
            self.resultado = primer + segundo
        elif self.controlOperacion == "-":
            self.resultado = primer - segundo
            if self.resultado == 0:
                # Si el resultado es 0 ponemos el valor de zero a 1 para indicar posible salto de beq
                self.zero = 1
        elif self.controlOperacion == "*":
            self.resultado = primer * segundo
        elif self.controlOperacion == "/":
            if segundo != 0:
                self.resultado = primer // segundo
        return self.resultado, self.zero


