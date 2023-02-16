class Control:
    # Control sera un diccionario con los 9 bits importantes que componen una instruccion
    def __init__(self):
        self.señales = dict(RegDst=3,AluSrc=3,MemtoReg=3,RegWrite=3,MemRead=3,MemWrite=3,Branch=3,AluOp1=3,AluOp2=3)
        # Inicializo con un valor distinto a 0, 1 o 2 para evitar problemas con condiciones

    # El 2 se refiere a que esos bits no se estan utilizando y en funcion del tipo de instruccion tendran unos valores u otros
    def getSeñales(self, instruccion):
        if instruccion.getTipo() == "R":
            self.señales["RegDst"] = 1
            self.señales["AluSrc"] = 0
            self.señales["MemtoReg"] = 0
            self.señales["RegWrite"] = 1
            self.señales["MemRead"] = 0
            self.señales["MemWrite"] = 0
            self.señales["Branch"] = 0
            self.señales["AluOp1"] = 1
            self.señales["AluOp2"] = 0
            # "100100010"

        elif instruccion.getOperacion() == "lw":
            self.señales["RegDst"] = 0
            self.señales["AluSrc"] = 1
            self.señales["MemtoReg"] = 1
            self.señales["RegWrite"] = 1
            self.señales["MemRead"] = 1
            self.señales["MemWrite"] = 0
            self.señales["Branch"] = 0
            self.señales["AluOp1"] = 0
            self.señales["AluOp2"] = 0
            #"011110000"

        elif instruccion.getOperacion() == "sw":
            self.señales["RegDst"] = 2
            self.señales["AluSrc"] = 1
            self.señales["MemtoReg"] = 2
            self.señales["RegWrite"] = 0
            self.señales["MemRead"] = 0
            self.señales["MemWrite"] = 1
            self.señales["Branch"] = 0
            self.señales["AluOp1"] = 0
            self.señales["AluOp2"] = 0
            # "212001000"

        elif instruccion.getOperacion() == "beq":
            self.señales["RegDst"] = 2
            self.señales["AluSrc"] = 0
            self.señales["MemtoReg"] = 2
            self.señales["RegWrite"] = 2
            self.señales["MemRead"] = 2
            self.señales["MemWrite"] = 2
            self.señales["Branch"] = 1
            self.señales["AluOp1"] = 0
            self.señales["AluOp2"] = 1
            # "202222101"

        elif instruccion.getOperacion() == "j":
            self.señales["RegDst"] = 2
            self.señales["AluSrc"] = 2
            self.señales["MemtoReg"] = 2
            self.señales["RegWrite"] = 0
            self.señales["MemRead"] = 0
            self.señales["MemWrite"] = 0
            self.señales["Branch"] = 2
            self.señales["AluOp1"] = 2
            self.señales["AluOp2"] = 2
            # "222000222"

        elif instruccion.getOperacion() == "addi":
            self.señales["RegDst"] = 0
            self.señales["AluSrc"] = 1
            self.señales["MemtoReg"] = 0
            self.señales["RegWrite"] = 1
            self.señales["MemRead"] = 0
            self.señales["MemWrite"] = 0
            self.señales["Branch"] = 0
            self.señales["AluOp1"] = 0
            self.señales["AluOp2"] = 0
            # "010100000"

        elif instruccion.getOperacion() == "li":
            self.señales["RegDst"] = 0
            self.señales["AluSrc"] = 2
            self.señales["MemtoReg"] = 0
            self.señales["RegWrite"] = 1
            self.señales["MemRead"] = 2
            self.señales["MemWrite"] = 2
            self.señales["Branch"] = 0
            self.señales["AluOp1"] = 2
            self.señales["AluOp2"] = 2
            # "020122022"
        return self.señales

    # Util para volver a 0 a los registros sin crear otro tipo control
    def resetearRegistros(self):
        self.señales["RegDst"] = 3
        self.señales["AluSrc"] = 3
        self.señales["MemtoReg"] = 3
        self.señales["RegWrite"] = 3
        self.señales["MemRead"] = 3
        self.señales["MemWrite"] = 3
        self.señales["Branch"] = 3
        self.señales["AluOp1"] = 3
        self.señales["AluOp2"] = 3
        return self.señales

    def getTipo(self):
        return self.señales

    def __str__(self):
        return "{'RegDst':"+ str(self.señales["RegDst"])+", 'AluSrc':"+ str(self.señales["AluSrc"])+", 'MemtoReg':"+ str(self.señales["MemtoReg"])\
        +", 'RegWrite':" +str(self.señales["RegWrite"])+", 'MemRead':"+ str(self.señales["MemRead"])+", 'MemWrite':" +str(self.señales["MemWrite"])\
        +", 'Branch': "+str(self.señales["Branch"])+", 'AluOp1': "+str(self.señales["AluOp1"])+", 'AluOp2': "+str(self.señales["AluOp2"])+"}"