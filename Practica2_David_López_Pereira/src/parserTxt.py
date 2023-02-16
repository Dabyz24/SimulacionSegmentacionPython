import os

# Clase para leer del txt la lista de instrucciones, para poder manejarla en la clase segmentacion
class ParserTxt:

    def __init__(self, txt):
        self.txt = ".."+os.sep+txt+".txt"
        self.flag = False  # Esta flag sirve para controlar si el txt existe, si no se encuentra se pondra True.
        try:
            with open(self.txt) as f:
                self.listatxt = f.readlines()
                f.close()
                self.flag = False
        except:
            self.flag = True

    def getListaTxt(self):
        return self.listatxt

    def getFlag(self):
        return self.flag

    def getTxt(self):
        return self.txt