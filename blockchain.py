from web3 import Web3
from web3.middleware import geth_poa_middleware
from variabili import *


class blockchain:

    address = ""
    tipo = 0

    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(node_url))  # indirizzo nodo1
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        with open('abi', 'r') as file:
            abi = file.read()

        self.c_instance = self.w3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=abi)


    def connessione(self):  # funzione che ritorna true se correttamente connessi all'account
        return self.w3.isConnected()


    def account_sbloccato(self):  # funzione che verifica se l'account è già sbloccato
        lst = self.w3.geth.personal.list_wallets()  # funzione che ritorna la lista dei portafogli gestiti da geth
        for i in range(len(lst)):
            if lst[i].accounts[0].address == self.address:
                if lst[i].status == "Unlocked":
                    return True     # se l'account passato è già sbloccato ritorno true
        return False


    def inserimento_account(self, priv_key, password):
        # inserisce l'account nella lista del nodo della blockchain con una nuova password
        self.w3.geth.personal.import_raw_key(private_key = priv_key, passphrase = password)


    def aggiunta_agenti(self):  # funzione che inserisce "address" alla blockchain
        self.w3.eth.defaultAccount = Web3.toChecksumAddress(admin_address)  # indirizzo account admin
        if Web3.isAddress(self.address) and Web3.isChecksumAddress(self.address):
            tx_hash = self.c_instance.functions.aggiungi_agenti(self.tipo, self.address).transact()
            tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash) # TODO è inutile?
        else:
            raise Exception("14")


    # Funzione che ritorna gli indirizzi presenti nelle liste fornitori, trasformatori e clienti
    def ricerca_agenti(self, tipo, stampa_tutto = False):
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
                if stampa_tutto:
                    agenti.append(tmp)
                elif not tmp == self.address:   # Se richiesto, non stampa se stesso
                    agenti.append(tmp)
                i = i + 1

        return agenti


    def sblocco_account(self, password):
        try:
            self.w3.geth.personal.unlock_account(account = self.address, passphrase = password, duration = 1200)
            return True
        except:
            raise Exception("15")


    def blocco_account(self):
        try:
            self.w3.geth.personal.lock_account(account = self.address)
            return True
        except:
            return False


    def crea_nft_fornitore(self, id_lotto, CO2):
        self.c_instance.functions.nft_fornitore(id_lotto, CO2).transact({'from': self.address})


    # Stampa l'ultimo nft di ogni lotto posseduto, se come parametro si passa mostra_tutti=True, stampa anche i vecchi
    def lista_nft(self, mostra_tutti=False):
        num_token = self.c_instance.functions.tokenIds().call()
        token_posseduti = []

        for i in range(num_token, 0, -1):       # chiede alla blockchain i token presenti
            if self.address == self.c_instance.functions.ownerOf(i).call():  # valuta solo i token posseduti
                dati_nft = self.c_instance.functions.lettura_impronta_da_id_nft(i).call()
                info_nft = {'id_NFT': i, 'id_lotto': dati_nft[0], 'CO2': dati_nft[1], 'NFT_precedente': dati_nft[2]}

                ultimo_nft_lotto = True
                if (i != num_token): # L'ultimo NFT per id è ovviamente l'ultimo relativo a qualunque lotto
                    for c in range(0, len(token_posseduti)):   # itera sui token salvati in lista
                        if (dati_nft[0] == token_posseduti[c]['id_lotto']):
                            ultimo_nft_lotto = False    # Se il lotto è già in lista, non è l'ultimo NFT
                            break

                # Se non richiesto da mostra_tutti, aggiungo in lista solo l'ultimo NFT di ogni lotto
                if ultimo_nft_lotto or mostra_tutti:
                    token_posseduti.append(info_nft)

        if not mostra_tutti:    # Se devo trascurare i non utilizzabili,
                                #  rimuovo anche quelli non sono ultimi relativi al lotto ma che ho ceduto ad altri
            for i in range(num_token, 0, -1):       # Richiede alla blockchain un token alla volta
                dati_nft = self.c_instance.functions.lettura_impronta_da_id_nft(i).call()
                for c in range(0, len(token_posseduti)):  # mostra l'nft più recente di ogni lotto
                    # Se trovo un nft con lo stesso lotto di uno in lista
                    if (dati_nft[0] == token_posseduti[c]['id_lotto']):
                        if i > token_posseduti[c]['id_NFT']: # Se ha id_NFT maggiore, quello in lista non è utilizzabile
                            da_rimuovere = token_posseduti[c]
                            token_posseduti.remove(da_rimuovere)
                            # Lo elimino dalla lista

        return token_posseduti


    def trasferisci_nft(self, destinatario, id_lotto):
        self.c_instance.functions.trasferimento_nft(destinatario, id_lotto).transact({'from': self.address})


    def aggiungi_azione(self, azione, id_lotto, CO2):
        self.c_instance.functions.aggiungi_azione(azione, id_lotto, CO2).transact({'from': self.address})


    def crea_nft_trasformatore(self, id_lotto):
        self.c_instance.functions.nft_trasformatore(id_lotto).transact({'from': self.address})


    def lettura_impronta_da_nft(self, id_nft):
        dati_nft = self.c_instance.functions.lettura_impronta_da_id_nft(id_nft).call()
        titolo = ['id_NFT', 'id_lotto', 'CO2', 'NFT_precedente']
        dati = [{'id_NFT': id_nft, 'id_lotto': dati_nft[0], 'CO2': dati_nft[1], 'NFT_precedente': dati_nft[2]}]
        return titolo, dati


    def lettura_impronta_da_lotto(self, id_lotto):
        id_nft = self.c_instance.functions.controllo_lotto(null_address, id_lotto).call()
        if not id_nft == 0:
            return self.lettura_impronta_da_nft(id_nft)
        else:
            return ["Lotto Inesistente"],[]
