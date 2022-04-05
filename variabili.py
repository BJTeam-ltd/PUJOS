
node_url = 'http://blockchain.g-ws.it:110'
#node_url = 'http://blockchain.g-ws.it:1100' #Daniele

contract_address = "0xfb895EF64e03aA76329836725dA2e02C83eBc1FA" #Indirizzo smart contract quando caricato

admin_address = "0xC9C913c8c3C1Cd416d80A0abF475db2062F161f6" #Indirizzo admin

null_address = "0x0000000000000000000000000000000000000000"

debug = True

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


stati = {
    "exit" : -100,
    "home" : -1,
    "admin" : 0,
    "aggiungi_agenti" : 1,

    "login" : 10,
    "fornitore" : 11,
    "trasformatore": 12,
    "cliente" : 13,
    "crea_nft_fornitore" : 14,
    "lista_nft" : 15,
    "trasferisci_nft" : 16,
    "aggiungi_azione" : 17,
    "crea_nft_trasformatore": 18,
    "stato_lettura_nft" : 30,
    "stato_lettura_lotto" : 31
}

tipo_utente={
    0 : "admin",
    1 : "fornitore",
    2 : "trasformatore",
    3 : "cliente"
}

id_utente={
    "admin" : 0,
    "fornitore" : 1,
    "trasformatore" : 2,
    "cliente" : 3
}

comandi_menu_home = {
    "titolo" : "Chi sei?:",
    "0" : "Admin",
    "1" : "Fornitore",
    "2" : "Trasformatore",
    "3" : "Cliente",
    "q" : "Termina esecuzione"
}

comandi_menu_admin = {
    "titolo" : "Admin:",
    "1" : "Aggiungi Fornitore",
    "2" : "Aggiungi Trasformatore",
    "3" : "Aggiungi Cliente",
    "b" : "Elenco indirizzi",
    "q" : "Logout"
}

comandi_menu_fornitore = {
    "titolo" : "Fornitore:",
    "1" : "Crea il tuo NFT",
    "2" : "I tuoi NFT",
    "3" : "Trasferisci NFT ad un trasformatore",
    "q" : "Logout"
}

comandi_menu_trasformatore = {
    "titolo" : "Trasformatore:",
    "1" : "Aggiungi un nuovo contributo di CO2 ad uno dei tuoi lotti",
    "2" : "Crea il tuo NFT",
    "3" : "I tuoi NFT",
    "4" : "Trasferisci NFT ad un trasformatore o cliente",
    "q" : "Logout"
}

comandi_menu_cliente = {
    "titolo" : "Cliente:",
    "1" : "Lettura impronta tramite id NFT",
    "2" : "Lettura impronta tramite id lotto",
    "q" : "Logout"
}

menu = {
    -1 : comandi_menu_home,
    0 :  comandi_menu_admin,
    11 : comandi_menu_fornitore,
    12 : comandi_menu_trasformatore,
    13 : comandi_menu_cliente,
}
