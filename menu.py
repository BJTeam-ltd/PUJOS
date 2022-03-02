
tipo_utente={
    0 : "Admin",
    1 : "Fornitore",
    2 : "Trasformatore",
    3 : "Cliente"
}

def scelta_utente():
    print('''------------------------
Chi sei?:
  0 - Capo supremo
  1 - Fornitore
  2 - Trasformatore
  3 - Cliente
  h - Help
  q - Esci
------------------------''')

def helper():
    print("Apri il manuale")


def menu_admin():
    print('''************************
Admin:
  1 - Aggiungi Fornitore
  2 - Aggiungi Trasformatore
  3 - Aggiungi Cliente
  q - Esci
************************''')


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