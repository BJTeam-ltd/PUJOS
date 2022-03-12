from funzioni import input_val

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

tipo_utente={
    0 : "Admin",
    1 : "Fornitore",
    2 : "Trasformatore",
    3 : "Cliente"
}


def scelta_utente():
    print('''------------------------
Chi sei?:
 \033[93m 0\033[0m - Admin
 \033[93m 1\033[0m - Fornitore
 \033[93m 2\033[0m - Trasformatore
 \033[93m 3\033[0m - Cliente
 \033[96m h\033[0m - Help
 \033[96m q\033[0m - Esci
------------------------''')
    return input_val(max_len=1)


def helper():
    print("Apri il manuale")


def menu_admin():
    print('''************************
Admin:
 \033[93m 1\033[0m - Aggiungi Fornitore
 \033[93m 2\033[0m - Aggiungi Trasformatore
 \033[93m 3\033[0m - Aggiungi Cliente
 \033[96m b\033[0m - Elenco indirizzi
 \033[96m q\033[0m - Logout
************************''')
    return input_val(max_len=1)


def menu_fornitore():
    print('''************************
Fornitore:
 \033[93m 1\033[0m - Crea il tuo NFT
 \033[93m 2\033[0m - I tuoi NFT 
 \033[93m 3\033[0m - Trasferisci NFT ad un trasformatore
 \033[96m q\033[0m - Logout
************************''')
    return input_val(max_len=1)
