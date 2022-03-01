
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