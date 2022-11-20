import socket

#------------------------------------------------------- SE CREA EL SERVIDOR
Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Server.bind(("LocalHost", 8000))
Server.listen(1)
Conexion, Addr = Server.accept()

#----------------------------------------- SE RECIBEN LOS VALORES DE E Y N
Recibir = Conexion.recv(1024)
Recibir = Recibir.decode(encoding = "ascii", errors = "ignore")
e,n=Recibir.split(",")

#--------------------------------------- SE PASAN A ENTERO PARA TRABAJARLOS
e=int(e)
n=int(n)

print("INFORMACIÓN DE ENCRIPTACIÓN RECIBIDA, CIFRANDO MENSAJE...\n")
archivo = open("mensajeentrada.txt","r+")
lineas = archivo.readlines()
archivo.close()
lineas=lineas[0]
print("\nMENSAJE: "+lineas)

#--------------------------------------- SE CIFRA CADA CARACTER DEL MENSAJE
x=''
for caracter in lineas:
    x+=str(((ord(caracter)-97)**e)%n)+","
x=x[0:-1]

#--------------------------------------------- SE ENVIA EL MENSAJE CIFRADO
Conexion.send(x.encode(encoding = "ascii", errors = "ignore"))
print("\nMENSAJE CIFRADO Y ENVIADO CORRECTAMENTE.\n")
print("Mensaje cifrado: "+x+"\n")
Conexion.close()