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
    
    mapping (uint256 => nft) token;                     // Dati collegati agli nft, contengono id, CO2, old_id
    mapping (uint256 => address) public fornitori;      // lista fornitori registrati nel sistema
    mapping (uint256 => address) public trasformatori;  // lista trasformatori
    mapping (uint256 => address) public clienti;        // lista clienti
    mapping (uint256 => uint) temp_CO2;                 // variabili incrementali per calcolo CO2
    
    uint public num_fornitori = 0;                      // numero CO2_totale fornitori registrati
    uint public num_trasformatori = 0;                  // idem
    uint public num_clienti = 0;                        // idem con patate

    event azione_trasformatore(string _nome_azione, uint256 _id_lotto, uint _CO2); // Evento per emissione azione

    constructor() ERC721("CarbonFootprint", "CFP") { 
    }


    // Funzione generica sia per aggiungere fornitori (1), trasformatori (2), clienti (3)
    // _nuovo_account è l'indirizzo dell'account da aggiungere
    function aggiungi_agenti(uint8 _tipo, address _nuovo_account) public onlyOwner returns (address) {
        
        //Controllo che l'account non sia già registrato
        require(!controllo_account(_nuovo_account, 1) && !controllo_account(_nuovo_account, 2) && !controllo_account(_nuovo_account, 3), "1"); //L'account esiste gia

        //Controllo che l'account non sia nullo (indirizzo non valido)
        require(_nuovo_account != address(0), "2"); //Non si puo inserire un account nullo

        // Posso creare fornitori (1), trasformatori (2), clienti (3)
        assert(_tipo >=1 && _tipo <= 3);
        
        // Le liste partono da indice = 1 --> prima ++ poi assegnazione
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


    // Creazione nuovo nft, restituisce il nuovo id
    function createItem(address tokenOwner, uint256 _id_lotto, uint256 _CO2, uint256 _old_nft_id) private {
        tokenIds++; //non serve controllo overflow https://docs.soliditylang.org/en/v0.8.11/control-structures.html#checked-or-unchecked-arithmetic
        
        token[tokenIds].id_lotto = _id_lotto;      // Assegnazione contenuti al nuovo nft
        token[tokenIds].CO2 = _CO2;
        token[tokenIds].old_nft_id = _old_nft_id;
        
        _mint(tokenOwner, tokenIds);               // Creazione nft
    }


    // Creazione nft del fornitore
    // Solo il fornitore può creare un nft da zero, il suo nft non punta a nessun altro nft. Non può ricevere nft.
    function nft_fornitore(uint256 _id_lotto, uint256  _CO2) public {
        require(controllo_account(msg.sender, 1), "3"); //Non sei un fornitore
        require(controllo_lotto(address(0), _id_lotto) == 0, "4"); //Questo ID lotto e' gia' associato ad un altro nft
        createItem(msg.sender, _id_lotto, _CO2, 0);
    }


    // Creazione nft del trasformatore
    // Deve possedere l'nft piu recente associato al lotto per creare un nuovo nft associato allo stesso lotto.
    // Può a sua volta inviare l'nft ad un nuovo trasformatore.
    // Il suo nft punta sempre ad un altro nft, quello precedente associato al lotto.
    function nft_trasformatore(uint256 _id_lotto) public {
        require(controllo_account(msg.sender, 2), "5"); //Non sei un trasformatore

        //Il trasformatore può usare solo gli nft nel suo portafoglio
        uint256 _old_nft_id = controllo_lotto(msg.sender, _id_lotto);
        require(_old_nft_id != 0, "6"); //Non sei il proprietario dell'ultimo NFT associato al lotto o il lotto e' inesistente

        // Somma contributi di CO2 relativi all'id prodotto
        uint256 CO2_totale = token[_old_nft_id].CO2 + temp_CO2[_id_lotto];
        temp_CO2[_id_lotto] = 0;

        createItem(msg.sender, _id_lotto, CO2_totale, _old_nft_id);
    }


    // Controllo esistenza account: restituisce 1 se l'account è presente in lista, 0 se non lo è
    // Prende come parametri l'indirizzo dell'account da controllare e
    //  un bool con true se devo cercare tra i trasformatori, false se tra i fornitori
    function controllo_account(address _account, uint8 _tipo) private view returns (bool) {
        // Posso creare fornitori (1), trasformatori (2), clienti (3)
        assert(_tipo >=1 && _tipo <= 3);

        if (_tipo == 1) {
            for (uint i = 1; i <= num_fornitori; i++) {
                if (_account == fornitori[i]) {
                    return true;
                }
            }
        }
        else if (_tipo == 2) {
            for (uint i = 1; i <= num_trasformatori; i++) {
                if (_account == trasformatori[i]) {
                    return true;
                }
            }
        }
        else if (_tipo == 3) {
            for (uint i = 1; i <= num_clienti; i++) {
                if (_account == clienti[i]) {
                    return true;
                }
            }
        }

        return false;   // Se arrivo fin quì l'account non è presente in lista
    }


    // Per conoscere l'impronta, restituisce i dati relativi
    function lettura_impronta_da_id_nft(uint256 _id_nft) public view returns (uint256, uint256, uint256) {
        require(_id_nft != 0 && _id_nft <= tokenIds, "7"); //Questo token non esiste

        return (token[_id_nft].id_lotto, token[_id_nft].CO2, token[_id_nft].old_nft_id);
    }


    // Trasferimento nft, solo trasformatori e clienti possono riceverlo
    function trasferimento_nft(address _to, uint256 _id_lotto) public {
        require(msg.sender != _to, "8"); //Stai trasferendo questo NFT a te stesso
        require(controllo_account(_to, 2) || controllo_account(_to, 3), "9"); //Il destinatario e' un fornitore, non puo' ricevere nft
        require(!controllo_account(msg.sender, 3), "10"); //Sei un cliente, non puoi trasferire nft


        uint256 _nftId = controllo_lotto(msg.sender, _id_lotto);
        require(_nftId != 0, "6"); //Non sei il proprietario dell'ultimo NFT associato al lotto o il lotto e' inesistente

        safeTransferFrom(msg.sender, _to, _nftId);
    }


    // Aggiunta CO2 al conteggio totale della CO2 del lotto ed emit azione
    function aggiungi_azione(string memory _nome_azione , uint256 _id_lotto, uint _CO2 ) public returns (bool) {
        require(controllo_account(msg.sender, 2), "5"); //Non sei un trasformatore
        require(controllo_lotto(msg.sender, _id_lotto) != 0, "11"); //Non possiedi l'ultimo NFT creato di questo lotto, non puoi fare azioni

        temp_CO2[_id_lotto] += _CO2;
        emit azione_trasformatore(_nome_azione, _id_lotto, _CO2);
        return true;
    }


    // Restituisce l'id NFT se il lotto esiste e l'ultimo nft associato è di _sender, 0 altrimenti
    // Se _sender = 0 restituisce l'id dell'ultimo NFT se il lotto già esiste, 0 altrimenti
    function controllo_lotto(address _sender, uint256 _id_lotto) private view returns (uint256) {
        for (uint256 id = tokenIds; id >= 1; id--){ // Procede dall'ultimo creato verso il primo
           if (token[id].id_lotto == _id_lotto){
               // entro qui se esiste il lotto
               if (_sender == address(0)){
                   return id;   // il lotto esiste
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
