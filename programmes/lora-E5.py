#!/usr/bin/python
# Ce programme envoie la chaine 12345678 vers TTN

# Importer les bibliothèques
import serial
import time

# Définition des flags
is_join = False           # On peut joindre la carte
is_exist = False          # La carte Grove LoRa E5 a été détectée

# Définition du timeout
read_timeout = 0.2

# Créer l'instance pour gérer la carte via le port série
lora = serial.Serial(
    port='/dev/serial0',
    baudrate=9600,
    bytesize=8,
    parity='N',
    timeout=1,
    stopbits=1,
    xonxoff=False,
    rtscts=False,
    dsrdtr=False
)

def envoi_test_reponse(chaine_verif, timeout_ms, commande):
    startMillis = int(round(time.time() * 1000))
    
    # Tester si la chaine à vérifier existe
    if chaine_verif == "":
        return 0
    
    # Envoyer la commande
    fin_ligne = "\r\n"
    cmd = "%s%s" % (commande, fin_ligne)
    print ("Commande envoyée = ",cmd)
    lora.write(cmd.encode())
    
    # Attendre la réponse
    reponse = ""
    quantity = lora.in_waiting
    # Lire la réponse de la carte jusqu'au timeout
    while int(round(time.time() * 1000)) - startMillis < timeout_ms:
        # Si on a des données
        if quantity > 0:
            # Les ajouter à la chaine réponse
            reponse += lora.read(quantity).decode('utf-8')
            print("Reponse1 de la carte : ", reponse)

        else:
            # Sinon attendre un moment
            time.sleep(read_timeout) 
        # Regarder si on a des données reçues
        quantity = lora.in_waiting

    print("Reponse de la carte : ", reponse)
    
    # Tester si la chaine attendue existe
    if chaine_verif in reponse :
        print("La chaine réponse existe", reponse)
        return 1    
    else:
        return 0
    
# Configuration de la carte
if envoi_test_reponse("+AT: OK", 1000,"AT"):
    # La carte a été détectée = passer à True
    is_exist = True
    # Configurer la carte
    envoi_test_reponse("+ID: AppEui", 1000,"AT+ID")
    envoi_test_reponse("+MODE: LWOTAA", 1000,"AT+MODE=LWOTAA")
    envoi_test_reponse("+DR: EU868", 1000,"AT+DR=EU868")
    envoi_test_reponse("+CH: NUM", 1000, "AT+CH=NUM,0-2")
    envoi_test_reponse("+KEY: APPKEY", 1000, "AT+KEY=APPKEY,\"6224041874374E3E85B93F635AB5E774\"")
    envoi_test_reponse("+CLASS: C", 1000, "AT+CLASS=A")
    envoi_test_reponse("+PORT: 8", 1000, "AT+PORT=8")

# Joindre le réseau
envoi_test_reponse("+JOIN: Network joined", 12000, "AT+JOIN")
    

# Envoi d'une chaine de data pour test
data = "AT+CMSGHEX=\"12345678\""
envoi_test_reponse("Done", 5000, data)



