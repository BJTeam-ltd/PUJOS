from eth_account import Account
import secrets
from texttable import Texttable


# Validazione input
# Controlla la lunghezza e restituisce la stringa validata
# Di default chiede l'input 5 volte e la lunghezza massima è 66 (quella della private key)
def input_val(max_len = 66, max_retry = 5, messaggio = ""):
    validated = False   # Input non ancora validato

    while not validated:
        if max_retry <= 0:  # tentativi terminati
            exit(5)

        print("", end=messaggio)  # stampa un eventuale messaggio passato come parametro
        in_str = input()    # lettura input e conteggio tentativo
        max_retry -= 1

        if not in_str.isalnum():        # Controllo caratteri speciali
            print('Caratteri non ammessi')
        elif len(in_str) > max_len:  # Controllo massima lunghezza
            print('Input troppo lungo')
        else:   # Se i controlli sono passati, l'input è validato
            validated = True

    return in_str


def richiedi_password():        # Chiede di scegliere una password, se non inserita, la sceglie in automatico
    passw = input_val(messaggio="Scegli una password o premi 'p' per default password: ", max_len=32)
    if(passw == "p"):
        passw = "passwordsicura"
    return passw

#TODO richiedere lunghezza minima per passw

def genera_portafoglio():
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)
    return private_key, acct.address


# Stampa una tabella con titolo e dati passati per parametri
#  se i dati di ogni elemento sono più degli elementi del titolo li tronca
#  accetta in input un array di stringhe per il titolo, array di stringhe o lista di dizionari per i dati
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
