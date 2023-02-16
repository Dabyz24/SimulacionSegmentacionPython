class MemDatos:

    # Una memoria de datos de 32 posiciones todas ellas inicializadas a 0 donde cada posicion representa una palabra de 4 bytes
    def __init__(self):
        self.memDatos = dict()
        for i in range(32):
            self.memDatos[i] = 0

    # Getters y setter para obtener los valores de la clase
    def getDato(self, registro):
        return self.memDatos[registro]

    def setDato(self, posicion, dato):
        self.memDatos[posicion] = dato

    def getMemDatos(self):
        return self.memDatos