#!/usr/bin/python
# Programme de démonstration pour la carte Seedstudio LoRa E5 Grove
# En       la température du CPU du Pi400 vers TTN
# au format Cayenne
# Introduction d'une valeur de retour numérique
# Ajouté la lecture d'un bouton GPIO26 / GND   - Pin 37 / Pin 39
# Automatisation de la génération de payload avec la valeur du bouton
# Code récupération T : https://www.dad3zero.net/201903/raspberry-pi-temperature-python/

# Importer les bibliothèques
import serial
import time
import binascii
from gpiozero import Button

# Le bouton est connecté en GPIO26
button = Button(26)
capteur = 0     # Le bouton n'est pas appuyé

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

# Lire la température CPU du Raspberry Pi
def temp_cpu():
    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as ftemp:
        t = int(ftemp.read()) / 1000
        current_temp = int(10*round (t,1))
        print(current_temp)
        return current_temp

# Envoyer la commande à LoRa - format :
# Chaine à vérifier (on doit la retrouver dans la réponse)
# Time out en milli secondes
# Commande à envoyer à LoRa
def envoi_test_reponse(chaine_verif, timeout_ms, commande):
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
    # Enregistrer l heure actuelle
    startMillis = int(round(time.time() * 1000))
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
    # Positionner le flag indiquant que la carte est jointe au réseau
    is_join = True
# Si la carte ne répond pas à AT elle n'est pas connectée ou HS
else:
    is_exist = False
    print("La carte LoRa E5 n'a pas été trouvée...")

# Boucle principale du programme
while True :
    # Lire l'état du bouton, positionner la variable
    if button.is_pressed:
        capteur = 1
    else:
        capteur = 0

    # Si la carte est bien connectée
    if (is_exist):
        rep = 0
        # Si le flag indique de connecter la carte LoRa au réseau
        if is_join:
        # Joindre le réseau - rep = 1 si ça fonctionne
            rep = envoi_test_reponse("+JOIN: Network joined", 12000, "AT+JOIN")
            if (rep):
                # La carte est connectée au réseau mattre le flag indiquant qu'il faut la connecter à False
                is_join = False
            else:
                # Récupérer son ID
                envoi_test_reponse("+ID: AppEui", 1000,"AT+ID")
                print("Impossible de joindre la carte LoRa au réseau !!\r\n")
                time.sleep(5)

        else:
            # Lire la température CPU
            temp = temp_cpu()
            # Envoi d'une chaine de data pour test
            # En hexadécimal
            print("temp", temp/10)
            # Conversion au format Cayenne
            payload = ('0201{:02x}0167{:04x}'.format(capteur, temp))
            print("payload : ", payload)
            commande= "AT+CMSGHEX="+payload +""
            print ("Commande : ", commande)
            rep = envoi_test_reponse("Done", 5000, commande)

            if rep:
                # Envoi réussi : Lire le Buffer de réception
                print("L\'envoi des données a fonctionné !!\r\n")
            else:
                # Envoi non réussi
                print("L\'envoi des données n'a pas fonctionné !!\r\n")
            time.sleep(15)
    else:
        time.sleep(5)

    

