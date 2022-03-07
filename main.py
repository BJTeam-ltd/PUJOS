from menu import *
from blockchain import blockchain
from funzioni import *

bch = blockchain()


# Funzione operazioni admin
def admin_home():
    print("Benvenuto Amministratore")
    while (True):
        menu_admin()
        s_admin = input()
        # Inserisce un nuovo agente
        if s_admin in {"1", "2", "3"}:
            print("Inserisci indirizzo portafoglio", tipo_utente.get(int(s_admin)) + ",",
                  bcolors.WARNING + "c" + bcolors.ENDC + " per generarlo, " + bcolors.OKCYAN + "q" + bcolors.ENDC + " per uscire")
            address = input_val()
            if (address == "c"):
                private_key, address = genera_portafoglio()  # funzione che genera un indirizzo del portafoglio
                print("Indirizzo generato:\n", address, "\n", private_key)
            if (address == "q"):
                pass
            else:
                bch.aggiunta_agenti(int(s_admin), address)

        elif (s_admin == "b"):
            print("Elenco Fornitori:")
            print(bch.ricerca_agenti(1))
            print("Elenco Trasformatori:")
            print(bch.ricerca_agenti(2))
            print("Elenco Clienti:")
            print(bch.ricerca_agenti(3))

        elif (s_admin == "q"):
            break
        else:
            print("Inserisci un numero valido")


def accoglienza(tipo):
    print("Elenco indirizzi esistenti")
    print(bch.ricerca_agenti(tipo))
    print("Inserisci indirizzo portafoglio", tipo_utente.get(int(tipo)) + "," + bcolors.OKCYAN + "q" + bcolors.ENDC + " per uscire")
    address = input_val()
    if (address == "q"):
        return False
    else:
        bch.login_account(tipo, address) #TODO DEVE RITORNARE QUALCOSA
        return True


def fornitore_home():
    print("Buongiorno sig. fornitore")
    while(True):
        if not accoglienza(1):
            break
        else:
            menu_fornitore()
            s_fornitore = input_val(max_len = 1)
            if s_fornitore == 1:
                print("Inserisci il lotto relativo al prodotto")
                id_lotto = input_val(max_len = 20)
                print("Inserisci il totale di CO2 emessa in grammi")
                CO2 = input_val(max_len = 10)
                bch.crea_nft_fornitore(id_lotto,CO2)




def trasformatore_home():
    print("Buongiorno sig. trasformatore")


def cliente_home():
    print("Buongiorno sig. cliente")


if __name__ == "__main__":

    # Stampe inziali, Benvenuto e controllo connessione blockchain
    print(bcolors.HEADER + "Benvenuto nella Dapp" + bcolors.ENDC)

    if bch.connessione():
        print("Sei connesso alla blockchain")
    else:
        print("Connessione fallita")
        # exit(10)

    while (True):
        scelta_utente()  # Stampa il menù per la scelta utente
        utente = input()  # TODO controllare lunghezza massima

        if (utente == "0"):
            admin_home()
        elif (utente == "1"):
            fornitore_home()
        elif (utente == "2"):
            trasformatore_home()
        elif (utente == "3"):
            cliente_home()
        elif (utente == "h"):
            helper()
        elif (utente == "q"):
            exit("Arrivederci!!")
        else:
            print("Inserisci un numero valido")
