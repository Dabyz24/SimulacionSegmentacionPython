from parserTxt import ParserTxt
from segmentacion import Segmentacion

print("--------------------------------------------------------------")
e = ParserTxt(input("Escriba el nombre del fichero que desee ejecutar sin escribir la extension .txt "))
# Gracias al bucle puedo controlar si el txt existe en el proyecto o no y asi evitar codigos de errores
while e.getFlag():
    e = ParserTxt(input("Txt no encontrado, por favor escriba un documento txt valido sin escribir la extension .txt "))

# Iniciamos la clase segmentacion con las instrucciones del fichero y ejecutamos el bucle de ejecucion
s = Segmentacion(e)
print("--------------------------------------------------------------")
print("Comenzando ejecucion de las instrucciones del fichero de texto " + e.getTxt())
s.bucleEjecucion()
print("--------------------------------------------------------------")
print("\tFin de ejecucion del bucle")

# Una vez finalizada la ejecucion muestro por pantalla el estado final de los 32 registros de MIPS y los valores de la memoria de datos
print("--------------------------------------------------------------")
print("Valores de Registros caracteristicos de Mips32")
print("--------------------------------------------------------------")

registros = s.getRegistros()

for i in registros.getRegistros():
    if i == "zero":
        print("\t\tReg $"+i+" ===> " + str(registros.getRegistro(i)))
    else:
        print("\t\tReg $"+i+" =====> " + str(registros.getRegistro(i)))

print("--------------------------------------------------------------")
print("Valores de Memoria de datos")
print("--------------------------------------------------------------")

memoriaDatos = s.getMemoriaDatos()
for i in memoriaDatos.getMemDatos():
    if i >= 10:
        print("\tPosicion " + str(i) + " ===> " + str(memoriaDatos.getDato(i)))
    else:
        print("\tPosicion "+str(i)+" ====> " + str(memoriaDatos.getDato(i)))
