from blockchain import Blockchain
from variabili import *
from funzioni import *

bch = Blockchain()
stato = stati["home"]  # Si imposta lo stato iniziale a "home"

if __name__ == "__main__":
    try:
        # Stampe inziali, Benvenuto e controllo connessione blockchain
        print(Bcolors.HEADER + "Benvenuto nella Dapp" + Bcolors.ENDC)

        # Tentativo di Connessione al nodo Blockchain, se l'esito è negativo termina l'esecuzione del programma
        if bch.connessione():
            print("Sei connesso alla blockchain")
        else:
            print("Connessione fallita")
            exit(10)

        while True:

            if stato == stati["home"]:
                try:
                    stato = stato_home(bch, stato)
                except Exception as problema:
                    stato = gestione_errori(problema, bch, stato)

            elif stato == stati["admin"]:
                try:
                    stato = stato_admin_home(bch, stato)
                except Exception as problema:
                    stato = gestione_errori(problema, bch, stato)

            elif stato == stati["login"]:
                try:
                    stato = stato_login(bch)
                except Exception as problema:
                    stato = gestione_errori(problema, bch, stato)

            elif stato == stati["fornitore"]:
                try:
                    stato = stato_fornitore_home(bch, stato)
                except Exception as problema:
                    stato = gestione_errori(problema, bch, stato)

            elif stato == stati["trasformatore"]:
                try:
                    stato = stato_trasformatore_home(bch, stato)
                except Exception as problema:
                    stato = gestione_errori(problema, bch, stato)

            elif stato == stati["aggiungi_azione"]:
                try:
                    stato = stato_aggiungi_azione(bch)
                except Exception as problema:
                    stato = gestione_errori(problema, bch, stato)

            elif stato == stati["crea_nft_trasformatore"]:
                try:
                    stato = stato_crea_nft_trasformatore(bch)
                except Exception as problema:
                    stato = gestione_errori(problema, bch, stato)

            elif stato == stati["aggiungi_agenti"]:
                try:
                    stato = stato_aggiungi_agenti(bch)
                except Exception as problema:
                    stato = gestione_errori(problema, bch, stato)

            elif stato == stati["crea_nft_fornitore"]:
                try:
                    stato = stato_crea_nft_fornitore(bch)
                except Exception as problema:
                    stato = gestione_errori(problema, bch, stato)

            elif stato == stati["lista_nft"]:
                try:
                    stato = stato_lista_nft(bch)
                except Exception as problema:
                    stato = gestione_errori(problema, bch, stato)

            elif stato == stati["trasferisci_nft"]:
                try:
                    stato = stato_trasferisci_nft(bch)
                except Exception as problema:
                    stato = gestione_errori(problema, bch, stato)

            elif stato == stati["cliente"]:
                try:
                    stato = stato_cliente_home(bch, stato)
                except Exception as problema:
                    stato = gestione_errori(problema, bch, stato)

            elif stato == stati["stato_lettura_nft"]:
                try:
                    stato = stato_lettura_nft(bch)
                except Exception as problema:
                    stato = gestione_errori(problema, bch, stato)

            elif stato == stati["stato_lettura_lotto"]:
                try:
                    stato = stato_lettura_lotto(bch)
                except Exception as problema:
                    stato = gestione_errori(problema, bch, stato)

            elif stato == stati["exit"]:
                if bch.blocco_account():
                    print(Bcolors.OKCYAN + "Logout eseguito" + Bcolors.ENDC)
                exit("Arrivederci!!")

    except KeyboardInterrupt:
        # se viene interrotta l'esecuzione
        try:
            if bch.blocco_account():
                print(Bcolors.OKCYAN + "Logout eseguito" + Bcolors.ENDC)
        except:
            print("Errore nella chiusura programma")
        exit("Arrivederci!!")
