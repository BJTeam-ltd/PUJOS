from eth_account import Account
from menu import *
import secrets
from texttable import Texttable
import json, codecs
from variabili import *

errori = json.load(codecs.open('errori.json', 'r', 'utf-8-sig'))
errori = errori[0]
debug = False


def stato_home():
    menu_home()

    utente = input_val(max_len=1,arg=("0","1","2","3","q"))

    if (utente == "0"):
        return stati["admin"]
    elif (utente == "1"):
        return stati["fornitore"]
    elif (utente == "2"):
        return stati["trasformatore"]
    elif (utente == "3"):
        return stati["cliente"]
    elif (utente == "q"):
        return stati["exit"]
    else:
        print("Inserisci un carattere valido")


# Funzione operazioni admin
def stato_admin_home(bch):
    print(bcolors.BOLD + bcolors.HEADER + "    Benvenuto Amministratore" + bcolors.ENDC + bcolors.ENDC)
    menu_admin()        # mostra il menu dell'amministratore
    input = input_val(max_len=1,arg=("1","2","3","b","q"))

    if input in {"1", "2", "3"}:  # tipologie di account ammessi
        return stati["aggiungi_agenti"],int(input)

    elif (input == "b"):  # stampa l'elenco degli account creati
        stampa_tabella(["Elenco Fornitori:"], bch.ricerca_agenti(1))
        stampa_tabella(["Elenco Trasformatori:"], bch.ricerca_agenti(2))
        stampa_tabella(["Elenco Clienti:"], bch.ricerca_agenti(3))
        return stati["admin"],0

    elif (input == "q"):
         return stati["home"],0


def stato_aggiungi_agenti(bch, tipo):

    # Inserisce un nuovo agente
    address = input_val(messaggio="Inserisci indirizzo portafoglio " + tipo_utente.get(tipo) + ", " +
              bcolors.WARNING + "c" + bcolors.ENDC + " per generarlo automaticamente, " + bcolors.OKCYAN + "q" + bcolors.ENDC + " per annullare ", max_len=42)

    if (address != "q"):    # l'admin intende inserire l'account

        if (address == "c"):
            # generazione automatica di indirizzo e chiave privata
            private_key, address = genera_portafoglio()
            print("Indirizzo generato:\n", "Address:", address, "\n", "Private Key:", private_key)
        else:
            # l'admin ha inserito un indirizzo manualmente, chiedo la relativa chiave privata
            private_key = input_val(messaggio="Inserisci la chiave privata: ")

        try:
            # Scelta password di sblocco
            password = richiedi_password()

            # Aggiunta account nella blockchain
            bch.aggiunta_agenti(tipo, address)

            # Inserimento account nel nodo corrente
            if bch.inserimento_account(private_key, password):
                print("Indirizzo inserito nel nodo corrente")
            else:
                print(bcolors.FAIL + "Errore nell'inserimento dell'Account nel nodo" + bcolors.ENDC)

            return stati["admin"]
        except Exception as problema:
            if str(problema) == "13":
                print(errori["13"])
                return stati["admin"]
            else:
                exit()


# Validazione input
# Controlla la lunghezza e restituisce la stringa validata
# Di default chiede l'input 5 volte e la lunghezza massima è 66 (quella della private key)
def input_val(max_len = 66, max_retry = 5, messaggio = "", min_len = 1,arg = ()):
    validated = False   # Input non ancora validato

    while not validated:
        if max_retry <= 0:  # tentativi terminati
            raise Exception("13")
        else:
            print("", end=messaggio)  # stampa un eventuale messaggio passato come parametro
            in_str = input()    # lettura input e conteggio tentativo
            max_retry -= 1

            if not in_str.isalnum():        # Controllo caratteri speciali
                if (max_retry > 0):
                    print('Caratteri non ammessi, riprova:')
                else:
                    print('Caratteri non ammessi')
            elif len(in_str) > max_len:  # Controllo massima lunghezza
                if(max_retry>0):
                    print('Input troppo lungo, riprova:')
                else:
                    print('Input troppo lungo')
            elif arg and not in_str in arg:
                if (max_retry > 0):
                    print('Caratteri non ammessi, riprova:')
                else:
                    print('Caratteri non ammessi')
            else:   # Se i controlli sono passati, l'input è validato
                validated = True

    return in_str


def richiedi_password():        # Chiede di scegliere una password, se non inserita, la sceglie in automatico
    passw = input_val(messaggio="Scegli una password o premi 'p' per default password: ", max_len=32)
    if(passw == "p"):
        passw = "passwordsicura"
    return passw


def gestione_errori(errore):
    try:
        errore = str(errore)
        e = int(errore[(len(errore) - 2):])
        if str(e) in errori:
            print(errori[str(e)])
        else:
            print("Errore")
    except:
        print("Errore.")

    if (debug):
        print("Errore originale: ", errore)


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
