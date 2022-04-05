from eth_account import Account
import secrets
from texttable import Texttable
import json, codecs
from variabili import *


errori = json.load(codecs.open('errori.json', 'r', 'utf-8-sig'))
errori = errori[0]


def stato_home(bch, stato):
    stampa_menu(stato)
    bch.address = ""
    bch.tipo = 0
    utente = input_val(max_len = 1, arg = menu[stato].keys())

    if (utente == "0"):
        bch.tipo = 0
        return stati["admin"]
    elif (utente == "1"):
        bch.tipo = 1
        return stati["login"]
    elif (utente == "2"):
        bch.tipo = 2
        return stati["login"]
    elif (utente == "3"):
        bch.tipo = 3
        return stati["login"]
    elif (utente == "q"):
        bch.tipo = 0
        return stati["exit"]
    else:
        exit(errori["99"])


# Funzione operazioni admin
def stato_admin_home(bch, stato):
    print(bcolors.BOLD + bcolors.HEADER + "    Benvenuto Amministratore" + bcolors.ENDC + bcolors.ENDC)
    stampa_menu(stato)        # mostra il menu dell'amministratore
    input = input_val(max_len = 1, arg = menu[stato].keys())

    if input in {"1", "2", "3"}:  # tipologie di account ammessi
        bch.tipo = int(input)
        return stati["aggiungi_agenti"]

    elif (input == "b"):  # stampa l'elenco degli account creati
        stampa_tabella(["Elenco Fornitori:"], bch.ricerca_agenti(1,True))
        stampa_tabella(["Elenco Trasformatori:"], bch.ricerca_agenti(2, True))
        stampa_tabella(["Elenco Clienti:"], bch.ricerca_agenti(3, True))
        bch.tipo = 0
        return stati["admin"]

    elif (input == "q"):
        bch.tipo = 0
        return stati["home"]


def stato_aggiungi_agenti(bch):

    # Inserisce un nuovo agente
    address = input_val(messaggio="Inserisci indirizzo portafoglio " + tipo_utente.get(bch.tipo) + ", "
                                  + bcolors.WARNING + "c" + bcolors.ENDC + " per generarlo automaticamente, "
                                  + bcolors.OKCYAN + "q" + bcolors.ENDC + " per annullare ", max_len=42)

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
        bch.address = address
        # Aggiunta account nella blockchain
        bch.aggiunta_agenti()
        print(bcolors.OKGREEN + "Aggiunta account " + str(tipo_utente.get(bch.tipo)) + " riuscita" + bcolors.ENDC)
        # Inserimento account nel nodo corrente
        bch.inserimento_account(private_key, password)
        print(bcolors.OKGREEN + "Indirizzo inserito nel nodo corrente" + bcolors.ENDC)

    else:
        bch.tipo = 0

    return stati["admin"]


def stato_login(bch):
    print("\n", bcolors.BOLD + bcolors.HEADER + "Buongiorno sig. " + tipo_utente[bch.tipo] + " " + bcolors.ENDC + bcolors.ENDC)
    address = login(bch)  # funzione per sblocco account
    if address:
        bch.address = address
        return stati[tipo_utente[bch.tipo]]
    else:
        return stati["home"]    # se è stato chiesto un logout o lo sblocco non è andato a buon fine


def stato_fornitore_home(bch, stato):
    stampa_menu(stato)

    input = input_val(max_len = 1, arg = menu[stato].keys())

    if input == "q":
        if (bch.blocco_account()):
            print("Logout eseguito")
        return stati["home"]
    elif input == "1":
        return stati["crea_nft_fornitore"]
    elif input == "2":
        return stati["lista_nft"]
    elif input == "3":
        return stati["trasferisci_nft"]
    else:
        exit(errori["99"])


def stato_trasformatore_home(bch, stato):
    stampa_menu(stato)

    input = input_val(max_len = 1, arg = menu[stato].keys())

    if input == "q":
        if (bch.blocco_account()):
            print("Logout eseguito")
        return stati["home"]
    elif input == "1":
        return stati["aggiungi_azione"]
    elif input == "2":
        return stati["crea_nft_trasformatore"]
    elif input == "3":
        return stati["lista_nft"]
    elif input == "4":
        return stati["trasferisci_nft"]
    else:
        exit(errori["99"])


def stato_crea_nft_fornitore(bch):
    id_lotto = input_val(messaggio="Inserisci il lotto relativo al prodotto o " + bcolors.OKCYAN + "q"
                                   + bcolors.ENDC + " per annullare ", max_len=20 , tipo="cifre")
    if (id_lotto == "q"):
        pass
    else:
        CO2 = int(input_val(messaggio="Inserisci il totale di CO2 emessa in grammi: ", max_len=10, tipo="cifre"))
        bch.crea_nft_fornitore(int(id_lotto), CO2)
        print(bcolors.OKGREEN + "NFT creato con successo" + bcolors.ENDC)

    return stati["fornitore"]


def stato_lista_nft(bch):
    mostra_tutti = input_val(messaggio="Vuoi mostrare anche gli nft non più utilizzabili?: s/n ",
                             max_len=1, arg=("s","n"))
    if (mostra_tutti in {"s", "n"}):
        all = (mostra_tutti == "s")
        my_nft = bch.lista_nft(mostra_tutti=all)
        # Creazione della tabella per mostrare gli nft
        titolo = ['ID NFT', 'Lotto', 'CO\u2082']
        stampa_tabella(titolo, my_nft)

    return stati[tipo_utente[bch.tipo]]     # Torna allo stato dell'account loggato


def stato_trasferisci_nft(bch):
    stampa_tabella(["Elenco trasformatori esistenti"], bch.ricerca_agenti(id_utente["trasformatore"], False))
    if bch.tipo == id_utente["trasformatore"]: #i trasformatori possono trasferire anche ai clienti
        stampa_tabella(["Elenco clienti esistenti"], bch.ricerca_agenti(id_utente["cliente"], False))
    destinatario = input_val(messaggio="Inserisci destinatario dell'NFT o " + bcolors.OKCYAN + "q"
                                       + bcolors.ENDC + " per annullare ", max_len=43)
    if (destinatario != "q"):
        id_lotto = input_val(messaggio="Inserisci id lotto: ", max_len=20, tipo="cifre")
        bch.trasferisci_nft(destinatario, int(id_lotto))
        print(bcolors.OKGREEN + "Trasferimento NFT del lotto", id_lotto, "verso", destinatario, "riuscito" + bcolors.ENDC)
    if(bch.tipo == id_utente["fornitore"]):
        return stati["fornitore"]
    elif (bch.tipo == id_utente["trasformatore"]):
        return stati["trasformatore"]
    else:
        exit(errori["99"])


def stato_aggiungi_azione(bch,stato):
    azione = input_val(messaggio="Inserisci l'azione da aggiungere o " + bcolors.OKCYAN + "q" + bcolors.ENDC
                                 + " per annullare ", max_len=30)
    if (azione != "q"):
        id_lotto = int(input_val(messaggio="Inserisci il lotto relativo al prodotto: ", max_len=20, tipo="cifre"))
        CO2 = int(input_val(messaggio="Inserisci CO2 emessa in grammi: ", max_len=10, tipo="cifre"))
        bch.aggiungi_azione(azione, id_lotto, CO2)
        print(bcolors.OKGREEN + "Azione sul lotto numero", id_lotto, "aggiunta con successo" + bcolors.ENDC)

    return stati["trasformatore"]


def stato_crea_nft_trasformatore(bch):
    id_lotto = input_val(messaggio="Inserisci il lotto relativo al prodotto o " + bcolors.OKCYAN + "q"
                                   + bcolors.ENDC + " per annullare ", max_len=20, tipo="cifre")
    if (id_lotto != "q"):
        bch.crea_nft_trasformatore(int(id_lotto))
        print(bcolors.OKGREEN + "NFT creato con successo" + bcolors.ENDC)

    return stati["trasformatore"]


def stato_cliente_home(bch, stato):
    stampa_menu(stato)
    input = input_val(max_len=1, arg=menu[stato].keys())

    if input == "q":
        if (bch.blocco_account()):
            print("Logout eseguito")
        return stati["home"]
    elif input == "1":
        return stati["stato_lettura_nft"]
    elif input == "2":
        return stati["stato_lettura_lotto"]


def stato_lettura_nft(bch,stato):
    id_nft = input_val(messaggio="Inserisci l'id NFT da leggere o " + bcolors.OKCYAN + "q" + bcolors.ENDC
                                 + " per annullare ", max_len=10, tipo="cifre")
    if id_nft != "q":
        titolo, dati = bch.lettura_impronta_da_nft(int(id_nft))
        stampa_tabella(titolo, dati)
    return stati["cliente"]


def stato_lettura_lotto(bch,stato):
    id_lotto = input_val(messaggio="Inserisci l'id lotto da leggere o " + bcolors.OKCYAN + "q" + bcolors.ENDC
                  + " per annullare ", max_len=10, tipo="cifre")
    if id_lotto != "q":
        titolo, dati = bch.lettura_impronta_da_lotto(int(id_lotto))
        if titolo[0] == "Lotto Inesistente":
            print("Lotto inesistente")
        else:
            stampa_tabella(titolo, dati)
    return stati["cliente"]


# Validazione input
# Controlla la lunghezza e restituisce la stringa validata
# Di default chiede l'input 5 volte e la lunghezza massima è 66 (quella della private key)
def input_val(max_len = 66, max_retry = 5, messaggio = "", arg = (), tipo = None):
    # tipo = None (tutto ammesso), "cifre" (solo cifre o "q")
    validated = False   # Input non ancora validato

    while not validated:

        print("", end = messaggio)  # Stampa un eventuale messaggio passato come parametro
        in_str = input()    # Lettura input e conteggio tentativo
        max_retry -= 1
        avviso = "Caratteri non ammessi, riprova:"

        if not in_str.isalnum():
            pass    # Sono presenti caratteri speciali

        elif len(in_str) > max_len:
            # L'input supera la lunghezza massima
            avviso = "Input troppo lungo, riprova:"

        elif arg and not in_str in arg:
            pass    # L'input non è compreso nella lista ammessa

        elif tipo == "cifre" and not (in_str.isdigit() or in_str == "q"):
            pass    # È richiesta una cifra o una q ma non è soddisfatta

        else:   # Se i controlli sono passati, l'input è validato
            return in_str

        if max_retry > 0:
            print(bcolors.WARNING + avviso + bcolors.ENDC)
        else:
            # Tentativi terminati, errore
            raise Exception("13")


def richiedi_password():        # Chiede di scegliere una password, se non inserita, la sceglie in automatico
    passw = input_val(messaggio="Scegli una password o premi 'p' per default password: ", max_len=32)
    if(passw == "p"):
        passw = "passwordsicura"
    return passw


def login(bch):
    stampa_tabella(["Elenco indirizzi esistenti"], bch.ricerca_agenti(bch.tipo, True))

    print("Inserisci indirizzo portafoglio", tipo_utente.get(int(bch.tipo)) + "," + bcolors.OKCYAN + " q" + bcolors.ENDC + " per uscire")
    address = input_val(max_len = 42)

    if (address == "q"):    # logout
        return False
    else:
        bch.address = address
        if not bch.account_sbloccato():
            password = richiedi_password()    # inserimento password account
            bch.sblocco_account(password)
            print(bcolors.OKCYAN + "Account sbloccato" + bcolors.ENDC)
        else:
            print(bcolors.OKCYAN + "Account già sbloccato" + bcolors.ENDC)
        return address  # se l'account era già sbloccato o è stato sbloccato




def gestione_errori(errore,bch,stato):
    try:
        errore = str(errore)
        if debug:
            print("Errore originale: ", errore)
        e = int(errore[(len(errore) - 2):])
        if str(e) in errori:
            print(bcolors.WARNING + errori[str(e)] + bcolors.ENDC)
        else:
            print("Errore")
            exit()
        if str(e) == "13":
            if (bch.blocco_account()):
                print("Logout eseguito")
            return stati["home"]
        else:
            return stato
    except:
        bch.blocco_account()
        exit(errori["99"])


def genera_portafoglio():
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)
    return private_key, acct.address


# Stampa una tabella con titolo e dati passati per parametri
#  se i dati di ogni elemento sono più degli elementi del titolo li tronca
#  accetta in input un array di stringhe per il titolo, lista di stringhe o lista di dizionari per i dati
def stampa_tabella(titolo, dati):
    t = Texttable()
    t.header(titolo)        # titolo tabella

    for i in range(0, len(dati)):       # itera sulla lista di dizionari in input
        if type(dati[i]) != str:
            sel_val = list(dati[i].values())[0:len(titolo)]     # tronca gli elementi in eccesso
        else:
            sel_val = [dati[i]]
        t.add_row(sel_val)     # aggiunge la riga alla tabella

    print(t.draw())
    print("")


def stampa_menu(stato):
    print("************************")
    _menu = menu[stato]
    for key, value in _menu.items():
        if key == "titolo":
            print(value)
        else:
            if key.isdigit():
                color = bcolors.WARNING
            else:
                color = bcolors.OKCYAN
            print(color + key + bcolors.ENDC + ' - ' + value)
    print("************************")

#TODO pensare a cosa fare se fallisce sblocco account (se creare errore nuovo o fare errore 99)