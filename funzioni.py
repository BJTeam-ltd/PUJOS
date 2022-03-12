from eth_account import Account
import secrets

# Validazione input
# Controlla la lunghezza e restituisce la stringa validata
# Di default chiede l'input 5 volte e la lunghezza massima è 66 (quella della private key)
def input_val(max_len = 66, max_retry = 5, messaggio = ""):
    print("",  end = messaggio) # stampa un eventuale messaggio passato come parametro
    validated = False   # Input non ancora validato

    while not validated:
        if max_retry <= 0:  # tentativi terminati
            exit(5)

        in_str = input()    # lettura input e conteggio tentativo
        max_retry -= 1

        if not in_str:      # ammetti input vuoto
            validated = True
        elif not in_str.isalnum():        # Controllo caratteri speciali
            print('Caratteri non ammessi')
        elif len(in_str) > max_len:  # Controllo massima lunghezza
            print('Input troppo lungo')
        else:   # Se i controlli sono passati, l'input è validato
            validated = True

    return in_str


def richiedi_password():        # Chiede di scegliere una password, se non inserita, la sceglie in automatico
    passw = input_val(messaggio="Scegli una password o premi 'invio' per default password: ", max_len=32)
    if not passw:  # default password
        passw = "passwordsicura"
    return passw


def genera_portafoglio():
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)
    return private_key, acct.address
