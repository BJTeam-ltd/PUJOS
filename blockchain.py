from hexbytes import HexBytes
from web3 import Web3
from web3.middleware import geth_poa_middleware
from menu import tipo_utente, bcolors
from address import *

class blockchain:

    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider('http://blockchain.g-ws.it:22000'))  # indirizzo nodo1
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        with open('abi', 'r') as file:
            abi = file.read()

        self.c_instance = self.w3.eth.contract(address= Web3.toChecksumAddress(contract_address), abi=abi)

    def connessione(self): #funzione che ritorna true se correttamente connessi all'account
        return self.w3.isConnected()

    def aggiunta_agenti(self, tipo, address):
        self.w3.eth.defaultAccount = Web3.toChecksumAddress(admin_address) # indirizzo account admin
        try:
            tx_hash= self.c_instance.functions.aggiungi_agenti(tipo, address).transact()
            tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
            print(bcolors.OKGREEN + "Aggiunta account "+ str(tipo_utente.get(tipo)) + " riuscita" + bcolors.ENDC)
        except Exception as problema:
            print(bcolors.FAIL + str(problema) + bcolors.ENDC)

    def ricerca_agenti(self,tipo):  #funzione che ritorna gli indirizzi presenti nelle liste fornitori, trasformatori e clienti
        agenti = []
        i = 1
        if tipo==1:
            tmp = self.c_instance.functions.fornitori(i).call()
            while "0x0000000000000000000000000000000000000000" != tmp:
                agenti.append(tmp)
                i = i+1
                tmp = self.c_instance.functions.fornitori(i).call()
        elif tipo==2:
            tmp = self.c_instance.functions.trasformatori(i).call()
            while "0x0000000000000000000000000000000000000000" != tmp:
                agenti.append(tmp)
                i = i+1
                tmp = self.c_instance.functions.trasformatori(i).call()
        else:
            tmp = self.c_instance.functions.clienti(i).call()
            while "0x0000000000000000000000000000000000000000" != tmp:
                agenti.append(tmp)
                i = i+1
                tmp = self.c_instance.functions.clienti(i).call()
        return agenti
