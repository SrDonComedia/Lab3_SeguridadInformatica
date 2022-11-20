import socket

#---------------------------------------------------- CONEXIÓN CON SERVIDOR
Cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Cliente.connect(("LocalHost", 8000))

#------------------------------------------------- FUNCIÓN PARA SABER SI ES PRIMO
def is_prime(n):
  for i in range(2,n):
    if (n%i) == 0:
      return False
  return True

#-------------------------------- FUNCIÓN PARA DETERMINAR EL MAXIMO COMÚN DIVISOR
def maximo_comun_divisor(a, b):
    temporal = 0
    while b != 0:
        temporal = b
        b = a % b
        a = temporal
    return a

#---------------------------------- SE SOLICITAN LOS NUMEROS PRIMOS P Y Q 
while True:
    try:
        priv_P=int(input("Ingrese un numero primo (P) para establecer conexión segura: "))
    except:
        print("Numero invalido, intente nuevamente")
    else:
        if(is_prime(priv_P)):
            while True:
                try:
                    priv_Q=int(input("Ingrese un numero primo (Q) para establecer conexión segura: "))
                except:
                    print("Numero invalido, intente nuevamente")
                else:
                    if(is_prime(priv_Q)):
                        break
                    else:
                        print("El numero ingresado debe ser un numero primo")
            break
        else:
            print("El numero ingresado debe ser un numero primo")


#-------------------------------------------------- SE CREAN LOS VALORES N Y 0(n)
public_N = priv_Q*priv_P 
priv_phiN=(1-priv_P)*(1-priv_Q)


#-------------------------------------------------- SE CALCULA EL VALOR E
for i in range(2,(priv_phiN-1)):
    if(maximo_comun_divisor(i,priv_phiN)==1 and is_prime(i)):
        public_E=i
        break

#--------------------------------------------------- SE BUSCA EL VALOR D
public_D=0
while True:
    if(((public_E*public_D)%priv_phiN) == 1):
        break
    else:
        public_D+=1

#---------------------------- SE ENVIAN E Y N PARA CIFRADO POR PARTE DEL SERVIDOR
Enviar = str(public_E)+","+str(public_N)
Cliente.send(Enviar.encode(encoding = "ascii", errors = "ignore"))

#-------------------------------------------------- SE RECIBE EL MENSAJE CIFRADO
Recibir = Cliente.recv(1024)
Recibir = Recibir.decode(encoding = "ascii", errors = "ignore")
print("\nMensaje Recibido: "+Recibir)
print("\nDESENCRIPTANDO CON LLAVE PRIVADA...\n")
Recibir=Recibir.split(",")

#----------------------------------------- SE DESCIFRA EL MENSAJE ENCRIPTADO
x=''
for caracter in Recibir:
    x+=chr(((int(caracter)**public_D)%public_N)+97)

#----------------------------------------- SE CREA EL ARCHIVO MENSAJERECIBIDO.TXT
print("MENSAJE DESCRIFRADO: "+x+"\n\nARCHIVO CREADO EXITOSAMENTE\n") 
archivo = open('mensajerecibido.txt','w+')
archivo.writelines(x)
archivo.close()
  
Cliente.close()