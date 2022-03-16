from hexbytes import HexBytes
from web3 import Web3
from web3.middleware import geth_poa_middleware
from menu import tipo_utente, bcolors
from address import *


class blockchain:

    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider('http://blockchain.g-ws.it:110'))  # indirizzo nodo1
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        with open('abi', 'r') as file:
            abi = file.read()

        self.c_instance = self.w3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=abi)


    def connessione(self):  # funzione che ritorna true se correttamente connessi all'account
        return self.w3.isConnected()

    def account_sbloccato(self, account):  # funzione che verifica se l'account è già sbloccato
        lst = self.w3.geth.personal.list_wallets()  # funzione che ritorna la lista dei portafogli gestiti da geth
        for i in range(len(lst)):
            if lst[i].accounts[0].address == account:
                if lst[i].status == "Unlocked":
                    return True     # se l'account passato è già sbloccato ritorno true
        return False


    def inserimento_account(self, priv_key, password):
        try:
            # inserisce l'account nella lista del nodo della blockchain con una nuova password
            self.w3.geth.personal.import_raw_key(private_key = priv_key, passphrase = password)
            return True  # ritorna vero se l'inserimento è riuscito
        except:
            return False

          
    def aggiunta_agenti(self, tipo, address):  # funzione che inserisce "address" alla blockchain
        self.w3.eth.defaultAccount = Web3.toChecksumAddress(admin_address)  # indirizzo account admin

        try:
            tx_hash = self.c_instance.functions.aggiungi_agenti(tipo, address).transact()
            tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
            print(bcolors.OKGREEN + "Aggiunta account " + str(tipo_utente.get(tipo)) + " riuscita" + bcolors.ENDC)
        except Exception as problema:
            print(bcolors.FAIL + str(problema)+ bcolors.ENDC)


    def ricerca_agenti(self, tipo):  # funzione che ritorna gli indirizzi presenti nelle liste fornitori, trasformatori e clienti
        agenti = []
        i = 1
        if tipo == 1:
            tmp = self.c_instance.functions.fornitori(i).call()
            while "0x0000000000000000000000000000000000000000" != tmp:
                agenti.append(tmp)
                i = i + 1
                tmp = self.c_instance.functions.fornitori(i).call()
        elif tipo == 2:
            tmp = self.c_instance.functions.trasformatori(i).call()
            while "0x0000000000000000000000000000000000000000" != tmp:
                agenti.append(tmp)
                i = i + 1
                tmp = self.c_instance.functions.trasformatori(i).call()
        else:
            tmp = self.c_instance.functions.clienti(i).call()
            while "0x0000000000000000000000000000000000000000" != tmp:
                agenti.append(tmp)
                i = i + 1
                tmp = self.c_instance.functions.clienti(i).call()
        return agenti


    def sblocco_account(self, address, password):
        try:
            self.w3.geth.personal.unlock_account(account = address, passphrase = password, duration = 1200)
            return True
        except Exception as problema:
            print(str(problema))
            return False

    def blocco_account(self, address):
        try:
            self.w3.geth.personal.lock_account(account = address)
            return True
        except Exception as problema:
            print(str(problema))
            return False

    def crea_nft_fornitore(self, address, id_lotto, CO2):
        try:
            self.c_instance.functions.nft_fornitore(id_lotto, CO2).transact({'from': address})
            return True
        except:
            return False

    def lista_nft(self, address):
        num_token = self.c_instance.functions.tokenIds().call()
        token_posseduti = []
        for i in range(1,num_token+1):
            if address == self.c_instance.functions.ownerOf(i).call():
                dati_nft = self.c_instance.functions.lettura_impronta_da_id_nft(i).call()
                info_nft = {'id_NFT': i, 'id_lotto': dati_nft[0], 'CO2': dati_nft[1], 'NFT_precedente': dati_nft[2]}
                token_posseduti.append(info_nft)
        return token_posseduti

    def trasferisci_nft(self, destinatario, id_nft, address):
        try:
            self.c_instance.functions.trasferimento_nft(destinatario, id_nft).transact({'from': address})
            return True
        except Exception as problema:
            print(str(problema))
            return False

        #TODO gestione errori con variabile debug
