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
            self.w3.parity.personal.importRawKey(priv_key, password)
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


    # Funzione che ritorna gli indirizzi presenti nelle liste fornitori, trasformatori e clienti
    def ricerca_agenti(self, tipo, address = None):
        agenti = []
        i = 1

        while True:     # Itera su tutti gli agenti del tipo richiesto
            if tipo == 1:
                tmp = self.c_instance.functions.fornitori(i).call()
            elif tipo == 2:
                tmp = self.c_instance.functions.trasformatori(i).call()
            elif tipo == 3:
                tmp = self.c_instance.functions.clienti(i).call()

            if "0x0000000000000000000000000000000000000000" == tmp:
                break   # Ferma il loop quando arriva a fine mapping
            else:
                if not tmp == address:  # Se richiesto, non stampa se stesso
                    agenti.append(tmp)
                i = i + 1
        return agenti


    def sblocco_account(self, address, password):
        try:
            self.w3.parity.personal.unlockAccount(address, password) #duration = 1200
            return True
        except Exception as problema:
            print(str(problema))
            return False


    def blocco_account(self, address):
        try:
            #self.w3.geth.personal.lock_account(account = address)
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


    # Stampa l'ultimo nft di ogni lotto posseduto, se come parametro si passa mostra_tutti=True, stampa anche i vecchi
    def lista_nft(self, address, mostra_tutti=False):
        num_token = self.c_instance.functions.tokenIds().call()
        token_posseduti = []

        for i in range(num_token, 0, -1):       # chiede alla blockchain i token presenti
            if address == self.c_instance.functions.ownerOf(i).call():  # valuta solo i token posseduti
                dati_nft = self.c_instance.functions.lettura_impronta_da_id_nft(i).call()
                info_nft = {'id_NFT': i, 'id_lotto': dati_nft[0], 'CO2': dati_nft[1], 'NFT_precedente': dati_nft[2]}

                ultimo_nft_lotto = True
                if (i != num_token):
                    for c in range(0, len(token_posseduti)):   # mostra l'nft più recente di ogni lotto
                        if (dati_nft[0] == token_posseduti[c]['id_lotto']):
                            ultimo_nft_lotto = False
                            break
                # Se non richiesto da mostra_tutti, considero solo l'ultimo token di ogni lotto
                if ultimo_nft_lotto or mostra_tutti:
                    token_posseduti.append(info_nft)
        return token_posseduti


    def trasferisci_nft(self, destinatario, id_lotto, address):
        try:
            self.c_instance.functions.trasferimento_nft(destinatario, id_lotto).transact({'from': address})
            return True
        except Exception as problema:
            print(str(problema))
            return False


    def aggiungi_azione(self, address, azione, id_lotto, CO2):
        try:
            self.c_instance.functions.aggiungi_azione(azione, id_lotto, CO2).transact({'from': address})
            return True
        except Exception as problema:
            print(str(problema))
            return False


    def crea_nft_trasformatore(self, address, id_lotto):
        try:
            self.c_instance.functions.nft_trasformatore(id_lotto).transact({'from': address})
            return True
        except:
            return False


    def lettura_impronta_da_nft(self, id_nft):
        try:
            dati_nft = self.c_instance.functions.lettura_impronta_da_id_nft(id_nft).call()
            info_nft = {'id_NFT': id_nft, 'id_lotto': dati_nft[0], 'CO2': dati_nft[1], 'NFT_precedente': dati_nft[2]}
            return info_nft
        except Exception as problema:
            return problema


    def lettura_impronta_da_lotto(self, id_lotto):
        id_nft = self.c_instance.functions.controllo_lotto(null_address, id_lotto).call()
        if not id_nft == 0:
            return self.lettura_impronta_da_nft(id_nft)
        else:
            return "Lotto inesistente"


    #TODO vedere se si può usare questa funzione in lista_nft()

    #TODO gestione errori con variabile debug
