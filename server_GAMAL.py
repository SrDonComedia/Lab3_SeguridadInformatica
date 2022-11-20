import socket
import random

#----------------------------------------------------- SE CREA EL SERVIDOR
Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Server.bind(("LocalHost", 8000))
Server.listen(1)
Conexion, Addr = Server.accept()

#------------------------------- SE RECIBE EL PRIMO P
Recibir = Conexion.recv(1024)
public_P = int(Recibir.decode(encoding = "ascii", errors = "ignore"))

#---------------------------------------- SE CREA EL GENERADOR ALEATORIO
public_A=random.randint(0,public_P-1)

#-------------------------------------- SE ENVIA EL GENERADOR ALEATORIO
Conexion.send(str(public_A).encode(encoding = "ascii", errors = "ignore"))

#-------------------------------------- SE CREA LA CLAVE PRIVADA DEL SERVIDOR
priv_key_server=random.randint(0,public_P-1)

#-------------------------------------- SE CREA LA CLAVE PUBLICA DEL SERVIDOR
public_K=(public_A**priv_key_server)%public_P

#----------------------------------------- SE RECIBE CLAVE PUBLICA DE CLIENTE
Recibir = Conexion.recv(1024)
public_K_client = int(Recibir.decode(encoding = "ascii", errors = "ignore"))

#----------------------------------------- SE ENVIA CLAVE PUBLICA DEL SERVIDOR
Conexion.send(str(public_K).encode(encoding = "ascii", errors = "ignore"))

#----------------------------------------------- SE SINCORNIZAN LAS CLAVES
llave_general=(public_K_client**priv_key_server)%public_P

print("llave general: "+str(llave_general))

print("INFORMACIÓN DE ENCRIPTACIÓN RECIBIDA, CIFRANDO MENSAJE...\n")
archivo = open("mensajeentrada.txt","r+")
lineas = archivo.readlines()
archivo.close()
lineas=lineas[0]
print("\nMENSAJE: "+lineas)

#------------------------------------------ SE CIFRA EL MENSAJE PARA ENVIARLO
x=''
for caracter in lineas:
    x+=str((llave_general*(ord(caracter)-97))%public_P)+","
x=x[0:-1]

Conexion.send(x.encode(encoding = "ascii", errors = "ignore"))
print("\nMENSAJE CIFRADO Y ENVIADO CORRECTAMENTE.\n")
print("Mensaje cifrado: "+x+"\n")
Conexion.close()