from instruccion import Instruccion


class RegAcoplamiento:

    # Los registros de acoplamiento son diccionarios que representan las entradas que reciben en el circuito
    def __init__(self, tipo):
        self.tipo = tipo   # Permite diferenciar el tipo de registro de acoplamiento

        if self.tipo == 0:  # IF/ID
            self.reg = ""  # Instruccion de memoria de instrucciones

        elif self.tipo == 1:  # ID/EX
            self.reg = dict(pc=0, controlIDEX=dict(),rDestino=0, rFuente1=0, rFuente2=0, instruccion=Instruccion()
                            , desplazamiento=0, inmediato=0)
        elif self.tipo == 2:  # EX/MEM
            self.reg = dict(pc=0, controlEXMEM=dict(), rDestino=0, rFuente2=0, instruccion=Instruccion(), resultado=0, zero=0)

        elif self.tipo == 3:  # MEM/WB
            self.reg = dict(pc=0, controlMEMWB=dict(), rDestino=0,instruccion=Instruccion(), resultadoAlu=0, resultadoMem=0)

    # getters y setters para cada tipo de registro
    def get(self, str=0):
        if self.tipo == 0 and str == 0:
            return self.reg
        if self.tipo > 0:
            return self.reg[str]

    def set(self, pos, valor):
        if self.tipo > 0:
            if pos == "controlMEMWB" or pos == "controlEXMEM" or pos == "controlIDEX":
                self.reg[pos].update(valor)
                # Con el metodo update actualizamos el valor deseado del diccionario
            else:
                self.reg[pos] = valor

    def setAcoplamientoIFID(self, instruccion):
        if self.tipo == 0:
            self.reg = instruccion

    # Para resetear los valores de los registros de acoplamiento
    def inicializarIFID(self):
        if self.tipo == 0:
            self.reg = ""

    def inicializarIDEX(self):
        if self.tipo == 1:
            self.reg["controlIDEX"] = dict()
            self.reg["pc"] = 0
            self.reg["rDestino"] = 0
            self.reg["rFuente1"] = 0
            self.reg["rFuente2"] = 0
            self.reg["instruccion"] = Instruccion()
            self.reg["desplazamiento"] = 0
            self.reg["inmediato"] = 0

    def inicializarEXMEM(self):
        if self.tipo == 2:
            self.reg["controlEXMEM"] = dict()
            self.reg["pc"] = 0
            self.reg["rDestino"] = 0
            self.reg["rFuente2"] = 0
            self.reg["instruccion"] = Instruccion()
            self.reg["resultado"] = 0
            self.reg["zero"] = 0

    def inicializarMEMWB(self):
        if self.tipo == 3:
            self.reg["controlMEMWB"] = dict()
            self.reg["pc"] = 0
            self.reg["rDestino"] = 0
            self.reg["instruccion"] = Instruccion()
            self.reg["resultadoAlu"] = 0
            self.reg["resultadoMem"] = 0

    def __str__(self):
        if self.tipo == 0:
            return self.reg
        elif self.tipo == 1:
            return "{'controlIDEX':"+ str(self.reg["control"])+", 'pc':"+ str(self.reg["pc"])+", 'rDestino':"+ str(self.reg["rDestino"])\
                    +", 'rFuente1':" +str(self.reg["rFuente1"])+", 'rFuente2':"+ str(self.reg["rFuente2"])+", 'instruccion':" +str(self.reg["instruccion"])\
                    +", 'desplazamiento': "+str(self.reg["desplazamiento"])+", 'inmediato': "+str(self.reg["inmediato"])+"}"
        elif self.tipo == 2:
            return "{'controlEXMEM':" + str(self.reg["control"]) + ", 'pc':" + str(self.reg["pc"]) + ", 'rDestino':" + str(self.reg["rDestino"])  + ", 'rFuente2':" + str(self.reg["rFuente2"]) + ", 'instruccion':" + str(self.reg["instruccion"]) \
                + ", 'resultado': " + str(self.reg["resultado"]) + ", 'zero': " + str(self.reg["zero"]) + "}"
        elif self.tipo == 3:
            return "{'controlMEMWB':" + str(self.reg["control"]) + ", 'pc':" + str(self.reg["pc"]) + ", 'rDestino':" + str(
                self.reg["rDestino"]) + ", 'instruccion':" + str(self.reg["instruccion"]) + ", 'resultadoAlu': " + str(self.reg["resultadoAlu"])\
                   + ", 'resultadoMem': " + str(self.reg["resultadoMem"]) + "}"
