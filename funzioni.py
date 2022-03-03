from eth_account import Account
import secrets

# Validazione input: controlla la lunghezza e restituisce la stringa validata
# Continua a chiedere l'input per 5 volte
def input_val(max_len = 43, max_retry = 5):
    c = 1
    validated = False   # Input non ancora validato

    while not validated:
        in_str = input()
        if len(in_str) < max_len:   # Controllo massima lunghezza
            validated = True
        elif c > max_retry:
            exit(5)
        else:
            print('Invalid input')
            c += 1

    return in_str


def suggerimento_address_utente():
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)
    return private_key, acct.address

