from menu import *

def admin_home():
    print("Buongiorno capo")

def fornitore_home():
    print("Buongiorno sig. fornitore")

def trasformatore_home():
    print("Buongiorno sig. trasformatore")

def cliente_home():
    print("Buongiorno sig. cliente")

print("Benvenuto nella Dapp")

while(True):
    scelta_utente() # Stampa il menù per la scelta utente
    utente = input() #TODO controllare lunghezza massima

    if(utente == "0"):
        admin_home()
    elif(utente == "1"):
        fornitore_home()
    elif(utente == "2"):
        trasformatore_home()
    elif(utente == "3"):
        cliente_home()
    elif(utente == "h"):
        helper()
    elif(utente == "q"):
        exit()
    else:
        print("Inserisci un numero valido")
