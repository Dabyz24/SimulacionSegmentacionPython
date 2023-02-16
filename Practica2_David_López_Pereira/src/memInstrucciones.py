class MemInstrucciones:

    def __init__(self, instrucciones):
        self.listaInstrucciones = []
        self.etiquetas = {}
        numLinea = 0

        for i in instrucciones:
            operandos = i.split(",")  # Divido la lista en operandos
            operacion = operandos[0].split(" ")  # Divido la lista por espacios para tener cada elemento por separado
            if operacion[0].__contains__(":"):  # Si la operacion en su primer elemento contiene : es que tiene etiqueta
                etiqueta = operacion[0].replace(":", "")  # La etiqueta sera el primer elemento hasta :
                instruccion = i.split(":")[1].replace(" ","", 1)  # Divido la instruccion y me quedo con la parte sin etiqueta
                instruccion = instruccion.replace("\n", "")  # Elimino el \n para que no lo escriba en la lista
                self.listaInstrucciones.append(instruccion)  # Añadimos a la lista la instruccion sin etiquetas
                self.etiquetas[etiqueta] = numLinea  # Guardamos en un diccionario la etiqueta con su correspondiente posicion en la lista
            else:
                instruccion = i.replace("\n", "")
                self.listaInstrucciones.append(instruccion)
                # Si no tiene etiqueta simplemente remplazamos el \n y lo añadimos a la lista
            numLinea = numLinea + 1  # Permite saber la posicion de la etiqueta en la lista de instrucciones

    def getListaInstrucciones(self):
        return self.listaInstrucciones

    def getEtiquetas(self):
        return self.etiquetas

    def getPos(self, pos):
        if pos < len(self.listaInstrucciones):
            return self.listaInstrucciones[pos]
        else:
            return "Posicion no encontrada"
