from menu import *
from blockchain import blockchain
from funzioni import input_val

bch = blockchain()

# Funzione operazioni admin
def admin_home():
    print("Benvenuto Amministratore")
    while (True):
        menu_admin()
        s_admin = input()
        # Inserisce un nuovo agente
        if s_admin in {"1","2","3"}:
            print("Inserisci indirizzo portafoglio", tipo_utente.get(int(s_admin)), "oppure q per uscire")
            #TODO suggerimento indirizzo utente
            address = input_val()
            if(address=="q"):
                pass
            else:
                bch.aggiunta_agenti(int(s_admin),address)

        elif (s_admin == "q"):
            break
        else:
            print("Inserisci un numero valido")

def fornitore_home():
    print("Buongiorno sig. fornitore")

def trasformatore_home():
    print("Buongiorno sig. trasformatore")

def cliente_home():
    print("Buongiorno sig. cliente")

if __name__ == "__main__":

    #Stampe inziali, Benvenuto e controllo connessione blockchain
    print(bcolors.HEADER + "Benvenuto nella Dapp" + bcolors.ENDC)

    if bch.connessione():
        print("Sei connesso alla blockchain")
    else:
        print("Connessione fallita")
        #exit(10)

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
            exit("Arrivederci!!")
        else:
            print("Inserisci un numero valido")
