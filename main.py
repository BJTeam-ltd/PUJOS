tipo_utente = {
    0 : "Capo supremo",
    1 : "Fornitore",
    2 : "Trasformatore",
    3 : "Cliente"
}
print("Benvenuto nella Dapp")
utente = 4;
while (utente < 0 or utente > 3):
    utente = int(input("Inserisci: \n 0 - Capo supremo \n 1 - Fornitore\n 2 - Trasformatore\n 3 - Cliente\n"))
    if (utente < 0 or utente > 3):
        print("Inserisci un numero valido")
print("Benvenuto " + tipo_utente.get(utente))
