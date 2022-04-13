import codecs
import json
import secrets

from eth_account import Account
from texttable import Texttable

from variabili import *

# si importa il file json contenente le descrizioni degli errori
errori = json.load(codecs.open('errori.json', 'r', 'utf-8-sig'))
errori = errori[0]


# STATO HOME
def stato_home(bch, stato):
    stampa_menu(stato)  # stampa il menu dello stato home
    bch.address = ""  # inizializza l'address ed il tipo di utente ogni volta che si torna allo stato home
    bch.tipo = 0
    # richiede l'input dell'utente, specificando la lunghezza massima(1) e i caratteri accettati
    utente = input_val(max_len=1, arg=menu[stato].keys())

    if utente == "0":
        bch.tipo = 0  # imposta il tipo di utente
        return stati["admin"]  # imposta lo stato di destinazione
    elif utente == "1":
        bch.tipo = 1
        return stati["login"]
    elif utente == "2":
        bch.tipo = 2
        return stati["login"]
    elif utente == "3":
        bch.tipo = 3
        return stati["login"]
    elif utente == "q":
        bch.tipo = 0
        return stati["exit"]
    else:
        # non è possibile arrivare a questa condizione con il normale flusso del programma
        # si provvede alla chiusura con notifica di errore "Errore grave nel sistema"
        exit(errori["99"])


# STATO ADMIN HOME
def stato_admin_home(bch, stato):
    print(Bcolors.BOLD + Bcolors.HEADER + "Benvenuto Amministratore" + Bcolors.ENDC + Bcolors.ENDC)
    stampa_menu(stato)  # mostra il menu dell'amministratore
    key = input_val(max_len=1, arg=menu[stato].keys())

    if key in {"1", "2", "3"}:  # tipologie di account ammessi
        # se l'input è una tipologia di account da aggiungere
        # si imposta il tipo e si ritorna il nuovo stato
        bch.tipo = int(key)
        return stati["aggiungi_agenti"]

    elif key == "b":  # stampa l'elenco degli account presenti nel nodo blockchain
        stampa_tabella(["Elenco Fornitori:"], bch.ricerca_agenti(1, True))
        stampa_tabella(["Elenco Trasformatori:"], bch.ricerca_agenti(2, True))
        stampa_tabella(["Elenco Clienti:"], bch.ricerca_agenti(3, True))
        bch.tipo = 0
        return stati["admin"]

    elif key == "q":
        bch.tipo = 0
        return stati["home"]


# STATO AGGIUNTA AGENTI
def stato_aggiungi_agenti(bch):
    # Inserisce un nuovo agente
    address = input_val(messaggio="Inserisci indirizzo portafoglio " + tipo_utente.get(bch.tipo) + ", "
                                  + Bcolors.WARNING + "c" + Bcolors.ENDC + " per generarlo automaticamente, "
                                  + Bcolors.OKCYAN + "q" + Bcolors.ENDC + " per annullare ", max_len=42, arg=("c", "q"),
                        tipo="address", bch=bch)

    if address != "q":  # l'admin intende inserire l'account

        if address == "c":
            # generazione automatica di indirizzo e chiave privata
            private_key, address = genera_portafoglio()
            print("Indirizzo generato:\n", "Address:", address, "\n", "Private Key:", private_key)
        else:
            # l'admin ha inserito un indirizzo manualmente, si chiede la relativa chiave privata
            private_key = input_val(messaggio="Inserisci la chiave privata: ")

        # Scelta password di sblocco
        password = richiedi_password()
        bch.address = address
        # Inserimento account nel nodo corrente
        bch.inserimento_account(private_key, password)
        print(Bcolors.OKGREEN + "Indirizzo inserito nel nodo corrente" + Bcolors.ENDC)
        # Aggiunta account nella blockchain
        bch.aggiunta_agenti()
        print(Bcolors.OKGREEN + "Aggiunta account " + str(tipo_utente.get(bch.tipo)) + " riuscita" + Bcolors.ENDC)

    else:
        bch.tipo = 0

    return stati["admin"]


# STATO LOGIN
def stato_login(bch):
    print("\n" + Bcolors.BOLD + Bcolors.HEADER + "Buongiorno sig. " + tipo_utente[
        bch.tipo] + " " + Bcolors.ENDC + Bcolors.ENDC)
    address = login(bch)  # funzione di sblocco dell'account nel nodo blockchain
    if address:
        bch.address = address
        return stati[tipo_utente[bch.tipo]]
    else:
        return stati["home"]  # se è stato chiesto un logout o lo sblocco non è andato a buon fine


# STATO FORNITORE HOME
def stato_fornitore_home(bch, stato):
    stampa_menu(stato)  # stampa il menu home del fornitore

    key = input_val(max_len=1, arg=menu[stato].keys())

    if key == "q":
        if bch.blocco_account():
            print(Bcolors.OKCYAN + "Logout eseguito" + Bcolors.ENDC)
        return stati["home"]
    elif key == "1":
        return stati["crea_nft_fornitore"]
    elif key == "2":
        return stati["lista_nft"]
    elif key == "3":
        return stati["trasferisci_nft"]
    else:
        # non è possibile arrivare a questa condizione con il normale flusso del programma
        # si provvede alla chiusura con notifica di errore "Errore grave nel sistema"
        exit(errori["99"])


# STATO TRASFORMATORE HOME
def stato_trasformatore_home(bch, stato):
    stampa_menu(stato)  # stampa il menu home del fornitore

    key = input_val(max_len=1, arg=menu[stato].keys())

    if key == "q":
        if bch.blocco_account():
            print(Bcolors.OKCYAN + "Logout eseguito" + Bcolors.ENDC)
        return stati["home"]
    elif key == "1":
        return stati["aggiungi_azione"]
    elif key == "2":
        return stati["crea_nft_trasformatore"]
    elif key == "3":
        return stati["lista_nft"]
    elif key == "4":
        return stati["trasferisci_nft"]
    else:
        # non è possibile arrivare a questa condizione con il normale flusso del programma
        # si provvede alla chiusura con notifica di errore "Errore grave nel sistema"
        exit(errori["99"])


# STATO CREAZIONE NFT FORNITORE
def stato_crea_nft_fornitore(bch):
    id_lotto = input_val(messaggio="Inserisci il lotto relativo al prodotto o " + Bcolors.OKCYAN + "q"
                                   + Bcolors.ENDC + " per annullare ", max_len=20, tipo="cifre_q")
    if id_lotto == "q":
        pass
    else:
        co2 = int(input_val(messaggio="Inserisci il totale di CO2 emessa in grammi: ", max_len=10, tipo="cifre"))
        bch.crea_nft_fornitore(int(id_lotto), co2)  # creazione dell'nft a partire dall'id lotto e dalla co2
        print(Bcolors.OKGREEN + "NFT creato con successo" + Bcolors.ENDC)
    # si ritorna stato "fornitore"
    return stati["fornitore"]


# STATO LISTA NFT
def stato_lista_nft(bch):
    # Solo il trasformatore può avere NFT non più utili, poiché trasferiti o elaborati
    if bch.tipo == id_utente["trasformatore"]:
        mostra_tutti = input_val(messaggio="Vuoi mostrare anche gli nft non più utilizzabili?: s/n ",
                                 max_len=1, arg=("s", "n"))
    else:
        mostra_tutti = "s"  # Fisso il parametro per gli altri

    if mostra_tutti in {"s", "n"}:
        mostra_tutti_stato = (mostra_tutti == "s")
        my_nft = bch.lista_nft(mostra_tutti=mostra_tutti_stato)
        # Creazione della tabella per mostrare gli nft
        titolo = ['ID NFT', 'Lotto', 'CO\u2082']
        stampa_tabella(titolo, my_nft)

    return stati[tipo_utente[bch.tipo]]  # Torna allo stato dell'account loggato


# STATO TRASFERISCI NFT
def stato_trasferisci_nft(bch):
    stampa_tabella(["Elenco trasformatori esistenti"], bch.ricerca_agenti(id_utente["trasformatore"], False))
    if bch.tipo == id_utente["trasformatore"]:  # i trasformatori possono trasferire anche ai clienti
        stampa_tabella(["Elenco clienti esistenti"], bch.ricerca_agenti(id_utente["cliente"], False))
    destinatario = input_val(messaggio="Inserisci destinatario dell'NFT o " + Bcolors.OKCYAN + "q"
                                       + Bcolors.ENDC + " per annullare ", max_len=43, tipo="address", arg="q",
                             bch=bch)
    if destinatario != "q":
        id_lotto = input_val(messaggio="Inserisci id lotto: ", max_len=20, tipo="cifre")
        bch.trasferisci_nft(destinatario, int(id_lotto))
        print(Bcolors.OKGREEN + "Trasferimento NFT del lotto", id_lotto, "verso", destinatario,
              "riuscito" + Bcolors.ENDC)
    # si provvede a verificare il tipo di utente, quindi lo stato precedente
    if bch.tipo == id_utente["fornitore"]:
        # se lo stato di provenienza era un "fornitore", torno allo stato "fornitore"
        return stati["fornitore"]
    elif bch.tipo == id_utente["trasformatore"]:
        return stati["trasformatore"]
    else:
        # non è possibile arrivare a questa condizione con il normale flusso del programma
        # si provvede alla chiusura con notifica di errore "Errore grave nel sistema"
        exit(errori["99"])


# STATO AGGIUNGI AZIONE
def stato_aggiungi_azione(bch):
    azione = input_val(messaggio="Inserisci l'azione da aggiungere o " + Bcolors.OKCYAN + "q" + Bcolors.ENDC
                                 + " per annullare ", max_len=30)
    if azione != "q":
        id_lotto = int(input_val(messaggio="Inserisci il lotto relativo al prodotto: ", max_len=20, tipo="cifre"))
        CO2 = int(input_val(messaggio="Inserisci CO2 emessa in grammi: ", max_len=10, tipo="cifre"))
        bch.aggiungi_azione(azione, id_lotto, CO2)  # funzione che aggiunge azioni effettuate dal trasformatore
        print(Bcolors.OKGREEN + "Azione sul lotto numero", id_lotto, "aggiunta con successo" + Bcolors.ENDC)
    # al termine si torna allo stato trasformatore
    return stati["trasformatore"]


# STATO CREAZIONE NFT FORNITORE
def stato_crea_nft_trasformatore(bch):
    id_lotto = input_val(messaggio="Inserisci il lotto relativo al prodotto o " + Bcolors.OKCYAN + "q"
                                   + Bcolors.ENDC + " per annullare ", max_len=20, tipo="cifre_q")
    if id_lotto != "q":
        # funzione per la creazione dell'NFT a partire dall'NFT precedente e dalle azioni del trasformatore
        bch.crea_nft_trasformatore(int(id_lotto))
        print(Bcolors.OKGREEN + "NFT creato con successo" + Bcolors.ENDC)
    # al termine si torna allo stato trasformatore
    return stati["trasformatore"]


# STATO CLIENTE HOME
def stato_cliente_home(bch, stato):
    stampa_menu(stato)
    key = input_val(max_len=1, arg=menu[stato].keys())

    if key == "q":
        # per uscire si esegue prima il logout e successivamente si ritorna lo stato "home"
        if bch.blocco_account():
            print(Bcolors.OKCYAN + "Logout eseguito" + Bcolors.ENDC)
        return stati["home"]
    elif key == "1":
        return stati["stato_lettura_nft"]
    elif key == "2":
        return stati["stato_lettura_lotto"]


# STATO LETTURA NFT
def stato_lettura_nft(bch):
    id_nft = input_val(messaggio="Inserisci l'id NFT da leggere o " + Bcolors.OKCYAN + "q" + Bcolors.ENDC
                                 + " per annullare ", max_len=10, tipo="cifre_q")
    if id_nft != "q":
        titolo, dati = bch.lettura_impronta_da_nft(int(id_nft))  # funzione che ricerca l'NFT a partire dall'ID
        stampa_tabella(titolo, dati)
    return stati["cliente"]


# STATO LETTURA LOTTO
def stato_lettura_lotto(bch):
    id_lotto = input_val(messaggio="Inserisci l'id lotto da leggere o " + Bcolors.OKCYAN + "q" + Bcolors.ENDC
                                   + " per annullare ", max_len=10, tipo="cifre_q")
    if id_lotto != "q":
        titolo, dati = bch.lettura_impronta_da_lotto(int(id_lotto))  # funzione che ricerca l'NFT a partire dal lotto
        if titolo[0] == "Lotto Inesistente":
            print("Lotto inesistente")
        else:
            stampa_tabella(titolo, dati)
    return stati["cliente"]


# Validazione input
# Controlla la lunghezza e restituisce la stringa validata
# Di default chiede l'input 5 volte e la lunghezza massima è 66 (quella della private key)
def input_val(max_len=66, max_retry=5, messaggio="", arg=(), tipo=None, bch=None):
    # tipo = None (tutto ammesso), "cifre" (solo cifre), "cifre_q" (solo cifre o "q")
    validated = False  # Input non ancora validato

    while not validated:

        print("", end=messaggio)  # Stampa un eventuale messaggio passato come parametro
        in_str = input()  # Lettura input e conteggio tentativo
        max_retry -= 1
        avviso = errori["100"]  # "Caratteri non ammessi, riprova: "

        if not in_str.isalnum():
            pass  # Sono presenti caratteri speciali

        elif len(in_str) > max_len:
            # L'input supera la lunghezza massima
            avviso = errori["101"]  # "Input troppo lungo, riprova: "

        elif tipo == "address" and not (in_str in arg):
            if not bch.indirizzo_valido(in_str):
                avviso = errori["102"]  # "Indirizzo non valido, riprova: "
            else:
                return in_str

        elif arg and not (in_str in arg):
            pass  # L'input non è compreso nella lista ammessa

        elif tipo == "cifre_q" and not (in_str.isdigit() or in_str == "q"):
            pass  # È richiesta una cifra o una q ma non è soddisfatta

        elif tipo == "cifre" and not in_str.isdigit():
            pass  # È richiesta una cifra o una q ma non è soddisfatta

        else:  # Se i controlli sono passati, l'input è validato
            return in_str

        if max_retry > 0:
            print(Bcolors.WARNING + avviso + Bcolors.ENDC)
        else:
            # Tentativi terminati, errore
            raise Exception("13")


def richiedi_password():  # Chiede di scegliere una password, se non inserita, la sceglie in automatico
    passw = input_val(messaggio="Scegli una password o premi 'p' per default password: ", max_len=32)
    if passw == "p":
        passw = "passwordsicura"
    return passw


def login(bch):
    lista_agenti_tipo = bch.ricerca_agenti(bch.tipo, True)
    stampa_tabella(["Elenco indirizzi esistenti"], lista_agenti_tipo)
    address = input_val(messaggio="Inserisci indirizzo portafoglio " + tipo_utente.get(
        int(bch.tipo)) + "," + Bcolors.OKCYAN + " q" + Bcolors.ENDC + " per uscire ", max_len=42, tipo="address",
                        arg="q", bch=bch)

    if address == "q":  # logout
        return False
    else:
        bch.address = address
        if address in lista_agenti_tipo:
            if not bch.account_sbloccato():
                password = richiedi_password()  # inserimento password account
                bch.sblocco_account(password)
                print(Bcolors.OKCYAN + "Account sbloccato" + Bcolors.ENDC)
            else:
                print(Bcolors.OKCYAN + "Account già sbloccato" + Bcolors.ENDC)
            return address  # se l'account era già sbloccato o è stato sbloccato
        else:
            raise Exception("14")


def gestione_errori(errore, bch, stato):  # funzione di gestione degli errori
    try:
        errore = str(errore)
        if debug:  # se debug è impostato su True mostra l'errore originale del sistema
            print("Errore originale: ", errore)
        e = int(errore[(len(errore) - 2):])
        if str(e) in errori:  # ricerca se il codice di errore è presente nell file "errori.json"
            print(Bcolors.WARNING + errori[str(e)] + Bcolors.ENDC)
        else:
            print("Errore")
            exit()
        if str(e) == "13":
            if bch.blocco_account():
                print(Bcolors.FAIL + "Logout eseguito" + Bcolors.ENDC)
            return stati["home"]
        else:
            return stato
    except:
        bch.blocco_account()
        exit(errori["99"])


def genera_portafoglio():  # funzione che genera il portafoglio
    priv = secrets.token_hex(32)  # si genera una chiave privata
    private_key = "0x" + priv
    acct = Account.from_key(private_key)  # si genera la chave pubblica a partire da quella privata
    return private_key, acct.address


# Stampa una tabella con titolo e dati passati per parametri
#  se i dati di ogni elemento sono più degli elementi del titolo li tronca
#  accetta in input un array di stringhe per il titolo, lista di stringhe o lista di dizionari per i dati
def stampa_tabella(titolo, dati):
    t = Texttable()
    t.header(titolo)  # titolo tabella

    for i in range(0, len(dati)):  # itera sulla lista di dizionari in input
        if type(dati[i]) != str:
            sel_val = list(dati[i].values())[0:len(titolo)]  # tronca gli elementi in eccesso
        else:
            sel_val = [dati[i]]
        t.add_row(sel_val)  # aggiunge la riga alla tabella

    print(t.draw())
    print("")


def stampa_menu(stato):  # funzione che stampa il menu in base allo stato
    print("************************")
    _menu = menu[stato]
    for key, value in _menu.items():
        if key == "titolo":
            print(value)
        else:
            if key.isdigit():
                color = Bcolors.WARNING
            else:
                color = Bcolors.OKCYAN
            print(color + key + Bcolors.ENDC + ' - ' + value)
    print("************************")
