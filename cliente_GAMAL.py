import socket
import random

#------------------------------------------------- CONEXIÓN CON SERVIDOR
Cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Cliente.connect(("LocalHost", 8000))

#------------------------------------------------- FUNCIÓN PARA SABER SI ES PRIMO
def is_prime(n):
  for i in range(2,n):
    if (n%i) == 0:
      return False
  return True

#------------------------------------------------- SE SOLICITA UN PRIMO (P) ALTO
while True:
    try:
        public_P=int(input("Ingrese un numero primo grande (P) para establecer conexión segura: "))
    except:
        print("Numero invalido, intente nuevamente")
    else:
        if(is_prime(public_P)):
            break
        else:
            print("El numero ingresado debe ser un numero primo")

#------------------------------- SE HACE ENVIO DEL NUMERO PRIMO GRANDE
Enviar = str(public_P)
Cliente.send(Enviar.encode(encoding = "ascii", errors = "ignore"))

#----------------------------------------------SE CREA LA LLAVE PRIVADA DEL CLIENTE
priv_key_client=random.randint(0,public_P-1)

#---------------------------------------------- SE RECIBE EL GENERADOR ALEATORIO
Recibir = Cliente.recv(1024)
public_A = int(Recibir.decode(encoding = "ascii", errors = "ignore"))

#----------------------------------------------- SE CREA LA CLAVE PUBLICA DEL CLIENTE
public_K=(public_A**priv_key_client)%public_P

#----------------------------------------------- SE ENVIA LA CLAVE PUBLICA DEL CLIENTE
Cliente.send(str(public_K).encode(encoding = "ascii", errors = "ignore"))

#--------------------------------------------- SE RECIBE LA CLAVE PUBLICA DEL SERVIDOR
Recibir = Cliente.recv(1024)
public_K_server = int(Recibir.decode(encoding = "ascii", errors = "ignore"))

#----------------------------------------------- SE SINCORNIZAN LAS CLAVES
llave_general=(public_K_server**priv_key_client)%public_P

print("llave general: "+str(llave_general))

Recibir = Cliente.recv(1024)
Recibir = Recibir.decode(encoding = "ascii", errors = "ignore")

print("\nMensaje Recibido: "+Recibir)
print("\nDESENCRIPTANDO CON LLAVE PRIVADA...\n")
Recibir=Recibir.split(",")

#------------------------------------------------ DESCIFRAR EL MENSAJE
x=''
for caracter in Recibir:
    x+=str(chr((((public_K_server**(public_P-1-priv_key_client))*int(caracter))%public_P)+97))

#------------------------------------------------ SE CREA EL ARCHIVO
print("MENSAJE DESCRIFRADO: "+x+"\n\nARCHIVO CREADO EXITOSAMENTE\n") 
archivo = open('mensajerecibido.txt','w+')
archivo.writelines(x)
archivo.close()
  
Cliente.close()