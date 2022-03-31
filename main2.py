from menu import *
from blockchain import blockchain
from variabili import *
from funzioni import *
import json
import codecs



bch = blockchain()

stato = stati["home"]
vecchio_stato = stati["home"]
tipo = 0

if __name__ == "__main__":

    # Stampe inziali, Benvenuto e controllo connessione blockchain
    print(bcolors.HEADER + "Benvenuto nella Dapp" + bcolors.ENDC)

    if bch.connessione():
        print("Sei connesso alla blockchain")
    else:
        print("Connessione fallita")
        exit(10)

    while True:

        if stato == stati["home"]:

            stato = stato_home(bch)  # Stampa il menù per la scelta utente


        elif stato == stati["exit"]:

            exit("Arrivederci!!")


        elif stato == stati["admin"]:

            stato = stato_admin_home(bch)


        elif stato == stati["aggiungi_agenti"]:

            stato = stato_aggiungi_agenti(bch)


        elif stato == stati["login"]:

            stato = stato_login(bch)


        elif stato == stati["fornitore"]:

            stato = stato_fornitore_home(bch)









