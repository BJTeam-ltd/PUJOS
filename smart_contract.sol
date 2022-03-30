// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/access/Ownable.sol";

contract NFT is ERC721, Ownable {

    uint256 public tokenIds;
    
    struct nft {            // Struttura dati associata ad ogni nft e salvati in storage
        uint256 id_lotto;   // ID lotto del prodotto associato 
        uint256 CO2;        // CO2 emessa per quel prodotto
        uint256 old_nft_id; // ID dell'nft dal quale deriva il prodotto
    }
    
    mapping (uint256 => nft) token;                     // Dati collegati agli NFT, contengono id, CO2, old_id
    mapping (uint256 => address) public fornitori;      // Lista fornitori registrati nel sistema
    mapping (uint256 => address) public trasformatori;  // Lista trasformatori
    mapping (uint256 => address) public clienti;        // Lista clienti
    mapping (uint256 => uint) temp_CO2;                 // Variabili incrementali per calcolo CO2
    
    uint public num_fornitori = 0;                      // Numero totale fornitori registrati
    uint public num_trasformatori = 0;                  // Numero totale trasformatori registrati
    uint public num_clienti = 0;                        // Numero totale clienti registrati

    event azione_trasformatore(string _nome_azione, uint256 _id_lotto, uint _CO2); // Evento per emissione azione

    constructor() ERC721("CarbonFootprint", "CFP") { 
    }


    // Funzione generica per aggiungere fornitori (_tipo = 1), trasformatori (2) o clienti (3)
    // _nuovo_account è l'indirizzo dell'account da aggiungere
    function aggiungi_agenti(uint8 _tipo, address _nuovo_account) public onlyOwner returns (address) {
        
        // Controllo che l'account non sia già registrato
        require(!controllo_account(_nuovo_account, 1), "1"); // L'account esiste già
        require(!controllo_account(_nuovo_account, 2), "1"); // L'account esiste già
        require(!controllo_account(_nuovo_account, 3), "1"); // L'account esiste già

        // Controllo che l'account non sia nullo (indirizzo non valido)
        require(_nuovo_account != address(0), "2"); // Non si può inserire un account nullo

        // Posso creare fornitori (1), trasformatori (2), clienti (3)
        require(_tipo >=1 && _tipo <= 3, "12");
            // Puoi creare solamente fornitori (1), trasformatori (2), clienti (3), inserisci un numero valido
        
        // Le liste partono da indice = 1 --> prima incremento poi assegnazione
        if (_tipo == 1) {
            num_fornitori++;
            fornitori[num_fornitori] = _nuovo_account;
        }
        else if (_tipo == 2) {
            num_trasformatori++;
            trasformatori[num_trasformatori] = _nuovo_account;
        }
        else if (_tipo == 3) {
            num_clienti++;
            clienti[num_clienti] = _nuovo_account;
        }

        return _nuovo_account;
    } 


    // Creazione nuovo NFT
    function createItem(address tokenOwner, uint256 _id_lotto, uint256 _CO2, uint256 _old_nft_id) private {
        tokenIds++; // Non serve controllo overflow con le versioni recenti di Solidity
        
        token[tokenIds].id_lotto = _id_lotto;      // Assegnazione contenuti al nuovo NFT
        token[tokenIds].CO2 = _CO2;
        token[tokenIds].old_nft_id = _old_nft_id;
        
        _mint(tokenOwner, tokenIds);                // Creazione NFT
        assert(ownerOf(tokenIds) == tokenOwner);    // Controllo della giusta assegnazione del nuovo NFT
    }


    // Creazione NFT del fornitore
    // Solo il fornitore può creare il primo NFT riferito ad un lotto,
        // il suo NFT non punta a nessun altro NFT. Non può ricevere NFT.
    function nft_fornitore(uint256 _id_lotto, uint256  _CO2) public {
        require(controllo_account(msg.sender, 1), "3");     // Non sei un fornitore, non puoi creare il primo NFT riferito al lotto.
        require(controllo_lotto(address(0), _id_lotto) == 0, "4");  // Questo ID lotto e' esistente e gia' associato ad un altro NFT
        createItem(msg.sender, _id_lotto, _CO2, 0);
    }


    // Creazione NFT del trasformatore
    // Deve possedere l'NFT piu recente associato al lotto per creare un nuovo NFT associato allo stesso lotto.
    // Gli NFT creati puntano sempre ad un altro NFT, quello precedente associato al lotto.
    function nft_trasformatore(uint256 _id_lotto) public {
        require(controllo_account(msg.sender, 2), "5"); // Non sei un trasformatore

        // Il trasformatore può usare solo gli nft nel suo portafoglio
        uint256 _old_nft_id = controllo_lotto(msg.sender, _id_lotto);
        require(_old_nft_id != 0, "6"); // Non sei il proprietario dell'ultimo NFT associato al lotto o il lotto e' inesistente

        // Somma contributi di CO2 relativi all'id lotto
        uint256 CO2_totale = token[_old_nft_id].CO2 + temp_CO2[_id_lotto];
        temp_CO2[_id_lotto] = 0;

        createItem(msg.sender, _id_lotto, CO2_totale, _old_nft_id);
    }


    // Controllo esistenza account: restituisce True se l'account è presente in lista, False se non lo è
    // Prende come parametri l'indirizzo dell'account da controllare ed un numero:
        // 1 per fornitori, 2 per trasformatori, 3 per clienti
    function controllo_account(address _account, uint8 _tipo) private view returns (bool) {
        // Si possono creare fornitori (1), trasformatori (2), clienti (3)
        assert(_tipo >=1 && _tipo <= 3);

        if (_tipo == 1) {
            for (uint i = 1; i <= num_fornitori; i++) {
                if (_account == fornitori[i]) {
                    return true;    // L'account è un fornitore
                }
            }
        }
        else if (_tipo == 2) {
            for (uint i = 1; i <= num_trasformatori; i++) {
                if (_account == trasformatori[i]) {
                    return true;    // L'account è un trasformatore
                }
            }
        }
        else if (_tipo == 3) {
            for (uint i = 1; i <= num_clienti; i++) {
                if (_account == clienti[i]) {
                    return true;    // L'account è un cliente
                }
            }
        }

        return false;   // L'account non è presente in lista
    }


    // Per conoscere il valore dell'impronta di un NFT, restituisce i dati relativi
    function lettura_impronta_da_id_nft(uint256 _id_nft) public view returns (uint256, uint256, uint256) {
        require(_id_nft != 0 && _id_nft <= tokenIds, "7"); // Questo token non esiste

        return (token[_id_nft].id_lotto, token[_id_nft].CO2, token[_id_nft].old_nft_id);
    }


    // Trasferimento NFT, solo trasformatori e clienti possono riceverlo
    function trasferimento_nft(address _to, uint256 _id_lotto) public {
        require(msg.sender != _to, "8"); // Stai trasferendo questo NFT a te stesso
        require(controllo_account(_to, 2) || controllo_account(_to, 3), "9"); // Il destinatario e' un fornitore, non puo' ricevere nft
        require(!controllo_account(msg.sender, 3), "10"); // Sei un cliente, non puoi trasferire NFT

        uint256 _nftId = controllo_lotto(msg.sender, _id_lotto);
        require(_nftId != 0, "6"); // Non sei il proprietario dell'ultimo NFT associato al lotto o il lotto e' inesistente

        safeTransferFrom(msg.sender, _to, _nftId);      // Trasferimento NFT
        assert(ownerOf(_nftId) == _to);                 // Controllo avvenuto trasferimento
    }


    // Aggiunta CO2 al conteggio totale della CO2 del lotto ed emit azione
    function aggiungi_azione(string memory _nome_azione , uint256 _id_lotto, uint _CO2 ) public returns (bool) {
        require(controllo_account(msg.sender, 2), "5"); // Non sei un trasformatore
        require(controllo_lotto(msg.sender, _id_lotto) != 0, "11");
            // Non possiedi l'ultimo NFT creato di questo lotto, non puoi fare azioni su di esso

        temp_CO2[_id_lotto] += _CO2;
        emit azione_trasformatore(_nome_azione, _id_lotto, _CO2);

        return true;
    }


    // Restituisce l'id NFT se il lotto esiste e l'ultimo NFT associato è di _sender, 0 altrimenti
    // Se il parametro in input _sender è 0 restituisce l'id dell'ultimo NFT se il lotto passato già esiste, 0 altrimenti
    function controllo_lotto(address _sender, uint256 _id_lotto) public view returns (uint256) {
        for (uint256 id = tokenIds; id >= 1; id--){ // Procede dall'ultimo creato verso il primo
            assert(id != 0);
            if (token[id].id_lotto == _id_lotto){    // if lotto esiste già
                if (_sender == address(0)){
                    return id;   // Il lotto esiste già
                }
                else if (_sender == ownerOf(id)){
                    return id;  // Il lotto esiste e l'ultimo nft associato è di _sender
                }
                else {
                    return 0;   // Il lotto esiste ma l'ultimo nft associato non è di _sender
                }
            }
        }
        return 0;   // Il lotto non esiste
    }
}
