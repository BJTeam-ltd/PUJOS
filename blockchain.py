from web3 import Web3
from web3.middleware import geth_poa_middleware
from menu import tipo_utente
from address import *

class blockchain:

    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:22000'))  # indirizzo nodo1
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        with open('abi', 'r') as file:
            abi = file.read()

        self.c_instance = self.w3.eth.contract(address= Web3.toChecksumAddress(contract_address), abi=abi)

    def connessione(self): #funzione che ritorna true se correttamente connessi all'account
        return self.w3.isConnected()

    def aggiunta_agenti(self, tipo, address):
        self.w3.eth.defaultAccount = Web3.toChecksumAddress(admin_address) # indirizzo account admin
        if self.c_instance.functions.aggiungi_agenti(tipo, address).transact()==address:
            print("Hai aggiunto con successo l'account", address, "come", tipo_utente.get(tipo))
        else:
            print("Errore nell'aggiunta account", tipo_utente.get(tipo))









