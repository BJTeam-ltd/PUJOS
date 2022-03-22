from menu import *
from blockchain import blockchain
from funzioni import *
import json
import codecs

errori = json.load(codecs.open('errori.json', 'r', 'utf-8-sig'))


print(errori[0]["2"] )


bch = blockchain()


# Funzione operazioni admin
def admin_home():
    print("Benvenuto Amministratore")
    while (True):
        s_admin = menu_admin()        # mostra il menu dell'amministratore

        # Inserisce un nuovo agente
        if s_admin in {"1", "2", "3"}:  # tipologie di account ammessi
            address = input_val(messaggio="Inserisci indirizzo portafoglio " + tipo_utente.get(int(s_admin)) + ", " +
                  bcolors.WARNING + "c" + bcolors.ENDC + " per generarlo automaticamente, " + bcolors.OKCYAN + "q" + bcolors.ENDC + " per annullare ", max_len=42)

            if (address != "q"):    # l'admin intende inserire l'account

                if (address == "c"):
                    # generazione automatica di indirizzo e chiave privata
                    private_key, address = genera_portafoglio()
                    print("Indirizzo generato:\n", "Address:", address, "\n", "Private Key:", private_key)
                else:
                    # l'admin ha inserito un indirizzo manualmente, chiedo la relativa chiave privata
                    private_key = input_val(messaggio="Inserisci la chiave privata: ")

                # Scelta password di sblocco
                password = richiedi_password()

                # Aggiunta account nella blockchain
                bch.aggiunta_agenti(int(s_admin), address)

                # Inserimento account nel nodo corrente
                if bch.inserimento_account(private_key, password):
                    print("Indirizzo inserito nel nodo corrente")
                else:
                    print(bcolors.FAIL + "Errore nell'inserimento dell'Account nel nodo" + bcolors.ENDC)
            else:
                pass

        elif (s_admin == "b"):      # stampa l'elenco degli account creati
            stampa_tabella(["Elenco Fornitori:"], bch.ricerca_agenti(1))
            stampa_tabella(["Elenco Trasformatori:"], bch.ricerca_agenti(2))
            stampa_tabella(["Elenco Clienti:"], bch.ricerca_agenti(3))

        elif (s_admin == "q"):
            break
        else:
            print("Inserisci un carattere valido")


def login(tipo):
    stampa_tabella(["Elenco indirizzi esistenti"], bch.ricerca_agenti(tipo))
    print("Inserisci indirizzo portafoglio", tipo_utente.get(int(tipo)) + "," + bcolors.OKCYAN + " q" + bcolors.ENDC + " per uscire")
    address = input_val(max_len = 42)
    if (address == "q"):    # logout
        return False
    else:
        if not bch.account_sbloccato(address):
            password = richiedi_password()    # inserimento password account
            logged = bch.sblocco_account(address, password)
            if (logged):
                print(bcolors.OKCYAN + "account sbloccato" + bcolors.ENDC)
            else:
                print(bcolors.FAIL + "errore nello sblocco dell'account" + bcolors.ENDC)
                return False    # sblocco account non andato a buon fine, logout
        else:
            print(bcolors.OKCYAN + "account già sbloccato" + bcolors.ENDC)
        return address  # se l'account era già sbloccato o è stato sbloccato


def fornitore_home():
    print("Buongiorno sig. fornitore")
    address = login(1)  # funzione per sblocco account
    if not address:
        pass    # se è stato chiesto un logout o lo sblocco non è andato a buon fine
    else:
        while(True):
            s_fornitore = menu_fornitore()

            if s_fornitore == "q":
                if (bch.blocco_account(address)):
                    print("logout eseguito")
                break

            elif s_fornitore == "1":
                id_lotto = input_val(messaggio = "Inserisci il lotto relativo al prodotto o " + bcolors.OKCYAN + "q" + bcolors.ENDC + " per annullare ", max_len = 20)
                if (id_lotto != "q"):
                    CO2 = int(input_val(messaggio = "Inserisci il totale di CO2 emessa in grammi: ", max_len = 10))
                    if bch.crea_nft_fornitore(address, int(id_lotto), CO2):
                        print(bcolors.OKGREEN + "NFT creato con successo" + bcolors.ENDC)
                    else:
                        print(bcolors.FAIL + "NFT non creato" + bcolors.ENDC)

            elif s_fornitore == "2":
                my_nft = bch.lista_nft(address)
                # Creazione della tabella per mostrare gli nft
                titolo = ['ID NFT', 'Lotto', 'CO\u2082']
                stampa_tabella(titolo, my_nft)

            elif s_fornitore == "3":
                stampa_tabella(["Elenco trasformatori esistenti"], bch.ricerca_agenti(2))
                destinatario = input_val(messaggio = "Inserisci destinatario dell'NFT o " + bcolors.OKCYAN + "q" + bcolors.ENDC + " per annullare ", max_len = 43)
                if (destinatario != "q"):
                    id_lotto = input_val(messaggio="Inserisci id lotto: ", max_len=20)
                    if bch.trasferisci_nft(destinatario, int(id_lotto), address):
                        print(bcolors.OKGREEN + "Trasferimento NFT", id_lotto, "verso", destinatario, "è riuscito" + bcolors.ENDC)


def trasformatore_home():
    print("Buongiorno sig. trasformatore")

    address = login(2)  # funzione per sblocco account
    if not address:
        pass  # se è stato chiesto un logout o lo sblocco non è andato a buon fine
    else:
        while (True):
            s_trasformatore = menu_trasformatore()

            if s_trasformatore == "q":
                if (bch.blocco_account(address)):
                    print("logout eseguito")
                break

            if s_trasformatore == "1":
                azione = input_val(messaggio="Inserisci l'azione da aggiungere o " + bcolors.OKCYAN + "q" + bcolors.ENDC + " per annullare ", max_len=30)
                if(azione != "q"):
                    id_lotto = int(input_val(messaggio="Inserisci il lotto relativo al prodotto: ", max_len=20))
                    CO2 = int(input_val(messaggio="Inserisci CO2 emessa in grammi: ", max_len=10))
                    if bch.aggiungi_azione(address, azione,id_lotto,CO2):
                        print(bcolors.OKGREEN + "Azione sul lotto numero", id_lotto,"aggiunta con successo" + bcolors.ENDC)
                    else:
                        print(bcolors.FAIL + "Azione non aggiunta" + bcolors.ENDC)

            if s_trasformatore == "2":
                id_lotto = input_val(messaggio="Inserisci il lotto relativo al prodotto o " + bcolors.OKCYAN + "q" + bcolors.ENDC + " per annullare ", max_len=20)
                if(id_lotto != "q"):
                    if bch.crea_nft_trasformatore(address, int(id_lotto)):
                        print(bcolors.OKGREEN + "NFT creato con successo" + bcolors.ENDC)
                    else:
                        print(bcolors.FAIL + "NFT non creato" + bcolors.ENDC)

            if s_trasformatore == "3":
                mostra_tutti = input_val(messaggio = "Vuoi mostrare anche gli nft non più utilizzabili?: y/n", max_len = 1)
                if (mostra_tutti in {"y", "n"}):
                    all = (mostra_tutti == "y")
                    my_nft = bch.lista_nft(address, mostra_tutti=all)
                    # Creazione della tabella per mostrare gli nft
                    titolo = ['ID NFT', 'Lotto', 'CO\u2082', 'NFT precedente']
                    stampa_tabella(titolo, my_nft)

            if s_trasformatore == "4":
                stampa_tabella(["Elenco altri trasformatori esistenti"], bch.ricerca_agenti(2, address))
                destinatario = input_val(messaggio = "Inserisci destinatario dell'NFT o " + bcolors.OKCYAN + "q" + bcolors.ENDC + " per annullare ", max_len = 43)
                if(destinatario != "q"):
                    id_lotto = input_val(messaggio = "Inserisci id lotto: ", max_len=20)
                    if bch.trasferisci_nft(destinatario, int(id_lotto), address):
                        print(bcolors.OKGREEN + "Trasferimento NFT", id_lotto, "verso", destinatario,
                          "riuscito" + bcolors.ENDC)


def cliente_home():
    print("Buongiorno sig. cliente")

    address = login(3)  # funzione per sblocco account
    if not address:
        pass  # se è stato chiesto un logout o lo sblocco non è andato a buon fine
    else:
        while (True):
            s_cliente = menu_cliente()
            if s_cliente == "1":
                id_nft = input_val(messaggio="Inserisci l'id NFT da leggere o " + bcolors.OKCYAN + "q" + bcolors.ENDC + " per annullare ", max_len=10)
                if(id_nft != "q"):
                    print(bch.lettura_impronta_da_nft(int(id_nft)))
            if s_cliente == "2":
                id_lotto = input_val(messaggio="Inserisci l'id lotto da leggere o " + bcolors.OKCYAN + "q" + bcolors.ENDC + " per annullare ", max_len=10)
                if(id_lotto != "q"):
                    print(bch.lettura_impronta_da_lotto(int(id_lotto)))
            if s_cliente == "q":
                if (bch.blocco_account(address)):
                    print("logout eseguito")
                    break


if __name__ == "__main__":

    # Stampe inziali, Benvenuto e controllo connessione blockchain
    print(bcolors.HEADER + "Benvenuto nella Dapp" + bcolors.ENDC)

    if bch.connessione():
        print("Sei connesso alla blockchain")
    else:
        print("Connessione fallita")
        exit(10)

    while (True):
        utente = scelta_utente()  # Stampa il menù per la scelta utente

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
            print("Inserisci un carattere valido")
