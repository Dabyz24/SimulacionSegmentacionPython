from memInstrucciones import MemInstrucciones
from memDatos import MemDatos
from alu import Alu
from control import Control
from registros import Registros
from instruccion import Instruccion
from regAcoplamiento import RegAcoplamiento

# Clase encargada de toda la funcionalidad de segmentacion, como son las etapas, forwarding unit y el bucle de ejecucion
class Segmentacion:

    def __init__(self, instrucciones):
        self.memoriaInstrucciones = MemInstrucciones(instrucciones.getListaTxt())
        self.memoriaDatos = MemDatos()
        self.registros = Registros()
        self.alu = Alu()
        self.control = Control()
        self.pc = 0
        self.cicloPrograma = 1  # Ciclo para controlar el bucle de ejecucion
        self.cicloActual = -1  # Ciclo en el que se encuentra el programa actualmente
        self.burbuja = False    # Booleano que avisa cuando se realiza una burbuja
        self.controlBurbuja = False  # Si ha habido burbuja se activa para no entrar en etapas no deseadas
        # Inicializo el registro de acoplamiento para IF/ID
        self.registroAcoplamientoIFID = RegAcoplamiento(0)
        # Inicializo el registro de acoplamiento para ID/EX
        self.registroAcoplamientoIDEX = RegAcoplamiento(1)
        # Inicializo el registro de acoplamiento para EX/MEM
        self.registroAcoplamientoEXMEM = RegAcoplamiento(2)
        # Inicializo el registro de acoplamiento para MEM/WB
        self.registroAcoplamientoMEMWB = RegAcoplamiento(3)

    # Devolvemos la instruccion deseada de la posicion de memoria de instrucciones con el pc
    def IF(self, pc, memInstrucciones: MemInstrucciones):
        print("Instruccion fetch(IF) de instruccion: " + str(pc))
        instruccion = memInstrucciones.getPos(pc)
        print("La instruccion buscada es: " + instruccion)
        return instruccion

    # Obtenemos todos los datos de interes de una instruccion con la instruccion previamente  obtenida en IF
    def ID(self, pc, instruccion, registros, señal):
        print("Decodificacion de instruccion(ID): " + str(pc))
        decodificada = Instruccion()
        decodificada.obtenerInstruccion(instruccion)
        registroDestino = registros.getRegistro(decodificada.getRegistroDestino())
        registroFuente1 = registros.getRegistro(decodificada.getRegistroFuente1())
        registroFuente2 = registros.getRegistro(decodificada.getRegistroFuente2())
        desplazamiento = decodificada.getDesplazamiento()
        inmediato = decodificada.getInmediato()
        etiqueta = decodificada.getEtiqueta()
        señal.getSeñales(decodificada)
        return decodificada, registroDestino, registroFuente1, registroFuente2, desplazamiento, inmediato, señal.getTipo(), etiqueta

    # Fase de ejecucion donde en funcion de la señal AluSrc realizara una operacion u otras
    def EX(self, pc, instruccion, rFuente1, rFuente2, inmediato, desplazamiento, alu, señal):
        print("Fase de ejecucion en ALU de instruccion: " + str(pc))
        print("AluSrc=" + str(señal.get("AluSrc")))
        resultado = ""
        zero = ""
        if señal["AluSrc"] == 2:
            print("Instruccion "+str(pc)+" sin fase EX, debido a que su AluSrc es 2")
        elif señal["AluSrc"] == 0:  # Si aluSrc es 0 entonces se utilizan los registros fuente1 y 2
            operacion = alu.setOperacion(señal["AluOp1"], señal["AluOp2"], instruccion)
            resultado, zero = alu.calcular(rFuente1, rFuente2, operacion)
            print("El calculo a realizar es: " + str(rFuente1) + operacion + str(rFuente2))
            print("Resultado: " + str(int(resultado)))
        elif señal["AluSrc"] == 1:  # Si aluSrc es 1 entonces se calcula el Fuente1 con el inmediato o desplazamiento
            operacion = alu.setOperacion(señal["AluOp1"],señal["AluOp2"], instruccion)
            if inmediato == -1:
                resultado, zero = alu.calcular(rFuente1, desplazamiento, operacion)
                print("El calculo a realizar es: " + str(rFuente1) + operacion + str(desplazamiento))
                print("Resultado: " + str(int(resultado)))
            elif desplazamiento == -1:
                resultado, zero = alu.calcular(rFuente1, inmediato, operacion)
                print("El calculo a realizar es: " + str(rFuente1) + operacion + str(inmediato))
                print("Resultado: " + str(int(resultado)))
        print("Fase de ejecucion en ALU (EX) terminada para instruccion: "+str(pc))
        return resultado, zero

    # En funcion de la señal de control MemRead o MemWrite escribiremos en memoria u obtendremos un valor
    def MEM(self, pc, memDatos, posicion, valor, señal):
        print("Fase MEM de instruccion: " + str(pc))
        # Comprobar MemRead y MemWrite
        if señal["MemRead"] == 1 and señal["MemWrite"] == 0:
            print("MemRead = 1 , MemWrite = 0")
            valor = memDatos.getDato(posicion)
            print("Dato obtenido en la posicion " + str(posicion) + " con un valor de " + str(valor))
        elif señal["MemRead"] == 0 and señal["MemWrite"] == 1:  # sw
            print("MemRead = 0 , MemWrite = 1")
            memDatos.setDato(posicion, valor)
            print("Valor " + str(valor) + " escrito correctamente en la posicion " + str(posicion))
        else:
            print("La instruccion " + str(pc) + " no tiene fase MEM")
        print("Fase MEM terminada para la instruccion: " + str(pc))
        return valor

    # Fase de escritura de instruccion en funcion de la señal MemtoReg y RegWrite
    def WB(self, pc, instruccion, valorDatos, resultado, registros, señal):
        print("Fase de escritura (WB) de instruccion: " + str(pc) + " " + str(instruccion.getOperacion()))

        if señal["MemtoReg"] == 1 and señal["RegWrite"] == 1:
            # Escribo en los registros el valor de la memoria
            print("MemtoReg= 1 , RegWrite= 1")
            print("Escribiendo dato de la memoria: " + str(valorDatos) + " en registro " + instruccion.getRegistroDestino())
            registros.setRegistro(instruccion.getRegistroDestino(), valorDatos)
        elif señal["MemtoReg"] == 0 and señal["RegWrite"] == 1 and instruccion.getOperacion() == "li":
            print("MemtoReg= 0 , RegWrite= 1")
            registros.setRegistro(instruccion.getRegistroDestino(), instruccion.getInmediato())
            print("Inmediato " + str(instruccion.getInmediato()) + " correctamente escrito en el registro " + instruccion.getRegistroDestino())
        elif señal["MemtoReg"] == 0 and señal["RegWrite"] == 1:
            print("MemtoReg= 0 , RegWrite= 1")
            registros.setRegistro(instruccion.getRegistroDestino(), resultado)
            print("Resultado " + str(resultado) + " correctamente escrito en el registro " + instruccion.getRegistroDestino())
        else:
            # Si el valor de RegWrite = 0 entonces el valor de MemtoReg es irrelevante porque no escribira nada en memoria
            print("La instruccion: " + str(pc)+" no realiza ninguna accion en la fase WB")

    # Unidad de cortocircuito del sistema para solucionar los riesgos de datos
    def unidadCortocircuito(self, registroIDEX, registroEXMEM, registroMEMWB):
        # Siempre que la operacion de ID/EX sea distinta a lw y li se comprueba si alguno de sus registros fuente1, fuente2 o Destino estan presentes en otra operacion
        if registroIDEX.get("instruccion").getOperacion() != "lw" and registroIDEX.get("instruccion").getOperacion() != "li":
            if registroIDEX.get("instruccion").getRegistroFuente1() == registroMEMWB.get("instruccion").getRegistroDestino() and registroIDEX.get("instruccion").getRegistroFuente1() != "zero":
                if registroMEMWB.get("instruccion").getOperacion() == "lw":
                    registroIDEX.set("rFuente1", registroMEMWB.get("resultadoMem"))
                    print("Actualizado el valor del registroFuente1 con el valor "+str(registroMEMWB.get("resultadoMem")) +" de memoria de instruccion de LW")
                elif registroMEMWB.get("instruccion").getOperacion() == "li":
                    registroIDEX.set("rFuente1", registroMEMWB.get("instruccion").getInmediato())
                    print("Actualizado el valor del registroFuente1 con el valor inmediato "+str(registroMEMWB.get("instruccion").getInmediato())+" de li")
                else:
                    registroIDEX.set("rFuente1", registroMEMWB.get("resultadoAlu"))
                    print("Se actualiza valor del registroFuente1 con valor "+str(registroMEMWB.get("resultadoAlu")) + " resultante de la ALU del registro de acoplamiento MEM/WB")
            elif registroIDEX.get("instruccion").getRegistroFuente1() == registroEXMEM.get("instruccion").getRegistroDestino() and registroIDEX.get("instruccion").getRegistroFuente1() != "zero":
                if registroEXMEM.get("instruccion").getOperacion() == "lw":
                    print("Riesgo de datos tipo RAW en la instruccion: " + registroIDEX.get("instruccion").getOperacion())
                    return True  # Indicador que se ha realizado una burbuja
                elif registroEXMEM.get("instruccion").getOperacion() == "li":
                    registroIDEX.set("rFuente1", registroEXMEM.get("instruccion").getInmediato())
                    print("Actualizado el valor del registroFuente1 con el valor inmediato "+str(registroEXMEM.get("instruccion").getInmediato())+" de li de registro acoplamiento EX/MEM")
                else:
                    registroIDEX.set("rFuente1",registroEXMEM.get("resultado"))
                    print("Se actualiza valor del registroFuente1 con valor "+str(registroEXMEM.get("resultado")) + " resultante de la ALU del registro de acoplamiento EX/MEM")

            elif registroIDEX.get("instruccion").getRegistroFuente2() == registroMEMWB.get("instruccion").getRegistroDestino() and registroIDEX.get("instruccion").getRegistroFuente2() != "zero":
                if registroMEMWB.get("instruccion").getOperacion() == "lw":
                    registroIDEX.set("rFuente2", registroMEMWB.get("resultadoMem"))
                    print("Se actualiza valor del registroFuente2 con valor "+str(registroMEMWB.get("resultadoMem"))+"de memoria de instruccion de LW")
                elif registroMEMWB.get("instruccion").getOperacion() == "li":
                    registroIDEX.set("rFuente2", registroMEMWB.get("instruccion").getInmediato())
                    print("Actualizado el valor del registroFuente2 con el valor inmediato "+str(registroMEMWB.get("instruccion").getInmediato())+" de li")
                else:
                    registroIDEX.set("rFuente2", registroMEMWB.get("resultadoAlu"))
                    print("Se actualiza valor del registroFuente2 con valor "+str(registroMEMWB.get("resultadoAlu")) + " resultante de la ALU del registro de acoplamiento MEM/WB")

            elif registroIDEX.get("instruccion").getRegistroFuente2() == registroEXMEM.get("instruccion").getRegistroDestino() and registroIDEX.get("instruccion").getRegistroFuente2() != "zero":
                if registroEXMEM.get("instruccion").getOperacion() == "lw":
                    print("Riesgo de datos tipo RAW en la instruccion: " + registroIDEX.get("instruccion").getOperacion())
                    return True
                elif registroEXMEM.get("instruccion").getOperacion() == "li":
                    registroIDEX.set("rFuente2", registroEXMEM.get("instruccion").getInmediato())
                    print("Actualizado el valor del registroFuente2 con el valor inmediato "+str(registroMEMWB.get("instruccion").getInmediato())+" de li de EX/MEM")
                else:
                    registroIDEX.set("rFuente2", registroEXMEM.get("resultado"))
                    print("Se actualiza valor del registroFuente2 con valor "+str(registroMEMWB.get("resultadoAlu")) + " resultante de la ALU del registro de acoplamiento MEM/WB")

            return False  # No se ha realizado burbuja

    def bucleEjecucion(self):
        # Siempre que el ciclo de Programa se mantenga en 1 realizo las etapas
        while self.cicloPrograma == 1:
            self.cicloActual = self.cicloActual + 1
            print("--------------------------------------------------------------")  # Permite diferenciar de manera visual cada ciclo del programa
            print("Está en el ciclo: " + str(self.cicloActual))
            # Primero compruebo la fase WB de la instruccion MEMWB en las primeras interacciones sera vacio
            if self.registroAcoplamientoMEMWB.get("instruccion").getEtapa() == "WB":
                self.WB(self.registroAcoplamientoMEMWB.get("pc"), self.registroAcoplamientoMEMWB.get("instruccion")
                     , self.registroAcoplamientoMEMWB.get("resultadoMem"), self.registroAcoplamientoMEMWB.get("resultadoAlu")
                     , self.registros, self.registroAcoplamientoMEMWB.get("controlMEMWB"))

                if self.registroAcoplamientoMEMWB.get("pc") == len(self.memoriaInstrucciones.getListaInstrucciones()) - 1:
                    self.setCicloPrograma(0)  # Si es el ultimo ciclo del programa se finaliza la ejecucion
                self.registroAcoplamientoMEMWB.get("instruccion").setEtapa("ID")

            # Compruebo si la instruccion se encuientra en la etapa MEM y si el ciclo de programa es 1 para evitar que se ejecute en la ultima interaccion del while
            if self.registroAcoplamientoEXMEM.get("instruccion").getEtapa() == "MEM" and self.cicloPrograma != 0:  # MEM
                self.registroAcoplamientoMEMWB.set("resultadoMem", self.MEM(self.registroAcoplamientoEXMEM.get("pc"),
                                                                  self.memoriaDatos,
                                                                  self.registroAcoplamientoEXMEM.get("resultado"),
                                                                  self.registroAcoplamientoEXMEM.get("rDestino"),
                                                                  self.registroAcoplamientoEXMEM.get("controlEXMEM")))

                self.registroAcoplamientoEXMEM.get("instruccion").setEtapa("WB")
                self.registroAcoplamientoMEMWB.set("resultadoAlu",self.registroAcoplamientoEXMEM.get("resultado"))
                self.registroAcoplamientoMEMWB.set("controlMEMWB", self.registroAcoplamientoEXMEM.get("controlEXMEM"))
                self.registroAcoplamientoMEMWB.set("instruccion", self.registroAcoplamientoEXMEM.get("instruccion"))
                self.registroAcoplamientoMEMWB.set("pc", self.registroAcoplamientoEXMEM.get("pc"))
                # Igualo todos los valores del registro MEMWB a los de EXMEM para poder avanzar a la siguiente etapa
                if self.burbuja:  # Si hay burbuja
                    self.registroAcoplamientoIDEX.get("instruccion").setEtapa("ID")
                    self.registroAcoplamientoEXMEM.inicializarEXMEM()
                    self.pc = self.pc - 1
                    self.registroAcoplamientoIFID.setAcoplamientoIFID(ifidAuxiliar)
                    # establezco la fase de IDEX en ID para repetir parar e inicializo el EXMEM resto 1 al pc
                print("Cargando datos de memoria y de registroAcoplamiento EX/MEM ===> registroAcoplamiento MEM/WB")

            # Si la etapa es la EX realizo las operaciones en la Alu
            if self.registroAcoplamientoIDEX.get("instruccion").getEtapa() == "EX" and self.cicloPrograma != 0:  # EX
                # Divido la operacion sw para pasarle como valor el rDestino en vez del fuente1
                if self.registroAcoplamientoIDEX.get("instruccion").getOperacion() == "sw":
                    resultado, pcSource = self.EX(self.registroAcoplamientoIDEX.get("pc"),self.registroAcoplamientoIDEX.get("instruccion"),
                        self.registroAcoplamientoIDEX.get("rDestino"),self.registroAcoplamientoIDEX.get("rFuente2"),
                        self.registroAcoplamientoIDEX.get("inmediato"),self.registroAcoplamientoIDEX.get("desplazamiento"),
                        self.alu,self.registroAcoplamientoIDEX.get("controlIDEX"))
                    self.registroAcoplamientoEXMEM.set("rDestino", self.registroAcoplamientoIDEX.get("rFuente1"))
                else:
                    resultado, pcSource = self.EX(self.registroAcoplamientoIDEX.get("pc"),
                                              self.registroAcoplamientoIDEX.get("instruccion"),
                                              self.registroAcoplamientoIDEX.get("rFuente1"),
                                              self.registroAcoplamientoIDEX.get("rFuente2"),
                                              self.registroAcoplamientoIDEX.get("inmediato"),
                                              self.registroAcoplamientoIDEX.get("desplazamiento"),
                                              self.alu, self.registroAcoplamientoIDEX.get("controlIDEX"))
                    self.registroAcoplamientoEXMEM.set("rDestino", self.registroAcoplamientoIDEX.get("rDestino"))

                self.registroAcoplamientoEXMEM.set("resultado", resultado)
                self.registroAcoplamientoEXMEM.set("zero", pcSource)
                self.registroAcoplamientoIDEX.get("instruccion").setEtapa("MEM")
                self.registroAcoplamientoEXMEM.set("instruccion", self.registroAcoplamientoIDEX.get("instruccion"))
                self.registroAcoplamientoEXMEM.set("rFuente2", self.registroAcoplamientoIDEX.get("rFuente2"))
                self.registroAcoplamientoEXMEM.set("controlEXMEM", self.registroAcoplamientoIDEX.get("controlIDEX"))
                self.registroAcoplamientoEXMEM.set("pc", self.registroAcoplamientoIDEX.get("pc"))
                # Igualo todos los valores de IDEX en EXMEM
                print("Cargando datos de la ALU y de registroAcoplamiento ID/EX ===> registroAcoplamiento EX/MEM")

                if self.registroAcoplamientoEXMEM.get("pc") == len(self.memoriaInstrucciones.getListaInstrucciones()) - 1:
                    self.controlBurbuja = True  # Si es la ultima no vuelve a entrar en las etapas de IF e ID
                if self.registroAcoplamientoEXMEM.get("controlEXMEM").get("Branch") == 1 and self.registroAcoplamientoEXMEM.get("zero") == 1:
                    self.pc = self.getMemoriaInstrucciones().getEtiquetas().get(etiqueta)
                    print("El valor de Branch es 1 y el de PcSource=1, calculamos el nuevo PC sumando con la direccion de etiqueta ", etiqueta)
                    print("PC actual es: " + str(self.pc))
                    self.registroAcoplamientoIFID.inicializarIFID()
                    self.registroAcoplamientoIDEX.inicializarIDEX()
                    self.controlBurbuja = False
                elif self.registroAcoplamientoEXMEM.get("controlEXMEM").get("Branch") == 2:
                    print("El valor de PcSource es 1, se actualiza PC a dir de etiqueta de salto incondicional: " + etiqueta)
                    self.pc = self.memoriaInstrucciones.getEtiquetas().get(etiqueta)
                    self.registroAcoplamientoIFID.inicializarIFID()
                    self.registroAcoplamientoIDEX.inicializarIDEX()
                    self.controlBurbuja = False
                    print("El valor del PC es: " + str(self.getPc()))
            # Si no es la ultima instruccion entro en la etapa ID
            if self.pc - 1 < len(self.memoriaInstrucciones.getListaInstrucciones()) and self.cicloPrograma != 0 and not self.controlBurbuja:  # ID
                # Si coincide con la instruccion leida en IFID en el ciclo anterior entonces realizo la operacion ID
                if self.memoriaInstrucciones.getListaInstrucciones()[self.pc - 1] == self.registroAcoplamientoIFID.get():
                    self.registroAcoplamientoIDEX.set("pc", self.pc - 1)  # apuntando a la siguiente instrucción
                    instruccionAux, rDestinoAux, rFuente1Aux,rFuente2Aux, desplazamientoAux, inmediatoAux,controlAux,\
                    etiqueta = self.ID(self.registroAcoplamientoIDEX.get("pc"), self.registroAcoplamientoIFID.get()
                                       , self.registros, self.control)

                    self.registroAcoplamientoIDEX.set("instruccion", instruccionAux)
                    self.registroAcoplamientoIDEX.set("rDestino", rDestinoAux)
                    self.registroAcoplamientoIDEX.set("rFuente1", rFuente1Aux)
                    self.registroAcoplamientoIDEX.set("rFuente2", rFuente2Aux)
                    self.registroAcoplamientoIDEX.set("desplazamiento", desplazamientoAux)
                    self.registroAcoplamientoIDEX.set("inmediato", inmediatoAux)
                    self.registroAcoplamientoIDEX.set("controlIDEX", controlAux)
                    self.registroAcoplamientoIDEX.get("instruccion").setEtapa("EX")
                    # En esta fase compruebo una vez que el registro IDEX este completo que no haya ningun cortocircuito
                    self.burbuja = self.unidadCortocircuito(self.registroAcoplamientoIDEX, self.registroAcoplamientoEXMEM,
                                                    self.registroAcoplamientoMEMWB)
            # Si sigue habiendo instrucciones en la memoria
            if self.pc < len(self.memoriaInstrucciones.getListaInstrucciones()) and self.cicloPrograma != 0 and not self.controlBurbuja:  # IF
                # Guardo la instruccion de ifid anterior
                ifidAuxiliar = self.registroAcoplamientoIFID.get()
                # Establezco la nueva instruccion con el metodo IF
                self.registroAcoplamientoIFID.setAcoplamientoIFID(self.IF(self.pc, self.memoriaInstrucciones))
                print("Cargando datos en registroAcoplamiento IF/ID")
                self.pc = self.pc + 1
                print("Valor del Pc: " + str(self.pc)+ " incrementado en Fase IF")

    # Getters y setters de los elementos de la clase segmentacion
    def getMemoriaInstrucciones(self):
        return self.memoriaInstrucciones

    def getMemoriaDatos(self):
        return self.memoriaDatos

    def getRegistros(self):
        return self.registros

    def getAlu(self):
        return self.alu

    def getControl(self):
        return self.control

    def getPc(self):
        return self.pc

    def getCicloPrograma(self):
        return self.cicloPrograma

    def getCicloActual(self):
        return self.cicloActual

    def getBurbuja(self):
        return self.burbuja

    def getAcoplamientoIFID(self):
        return self.registroAcoplamientoIFID

    def getAcoplamientoIDEX(self):
        return self.registroAcoplamientoIDEX

    def getAcoplamientoEXMEM(self):
        return self.registroAcoplamientoEXMEM

    def getAcoplamientoMEMWB(self):
        return self.registroAcoplamientoMEMWB

    def setControl(self, control):
        self.control = control

    def setPc(self, pc):
        self.pc = pc

    def setCicloPrograma(self, ciclo):
        self.cicloPrograma = ciclo

    def setCicloActual(self, ciclo):
        self.cicloActual = ciclo

    def getBurbuja(self):
        return self.burbuja

    def setBurbuja(self, bool):
        self.burbuja = bool

    def getControlBurbuja(self):
        return self.controlBurbuja

    def setControlBurbuja(self, bool):
        self.controlBurbuja = bool

