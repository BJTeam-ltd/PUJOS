// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/access/Ownable.sol";


contract NFT is ERC721, Ownable {

    uint256 private tokenIds;
    
    //EDIT
    struct nft {
        uint256 id_lotto;
        uint256 CO2;
        uint256 old_nft_id;
    }
    
    mapping (uint256 => nft)  token; // indirizzo nft fornitore
    mapping (uint256 => address)  public fornitori; // lista fornitori
    mapping (uint256 => address)  public trasformatori; // lista trasformatori
    mapping (uint256 => address)  public clienti; // lista clienti
    mapping (uint256 => uint)     temp_CO2; //variabile temporanea per calcolo CO2
    uint public num_fornitori = 0;     //per sapere quanti ne sono
    uint public num_trasformatori = 0; //idem
    uint public num_clienti = 0;       //idem con patate

    constructor() ERC721("CarbonFootprint", "CFP") { 
    }
    //funzione generica sia per aggiungere fornitori (1), trasformatori (2), clienti (3)
    //_nuovo_account è l'indirizzo dell'account da aggiungere
    function aggiungi_agenti(uint8 _tipo, address _nuovo_account) public onlyOwner returns(string memory) {
        //Controllo che l'account non sia già registrato
        require(!controllo_account(_nuovo_account, 1) && !controllo_account(_nuovo_account, 2) && !controllo_account(_nuovo_account, 3), "L'account esiste gia");

        //Controllo che l'account non sia nullo (indirizzo non valido)
        require(_nuovo_account != address(0), "Non si puo inserire un account nullo");

        //require(_tipo >=1 && _tipo <= 3, "Tipo non valido");
        assert(_tipo >=1 && _tipo <= 3);
        //Lasciamo libero trasformatori[0] e fornitori[0] per l'id vuoto
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
        return "L'account ha i permessi";
    } 

    function createItem(address tokenOwner, uint256 _id_lotto, uint256 _CO2, uint256 _old_nft_id) private returns (uint256) {
        tokenIds++; //non serve controllo overflow https://docs.soliditylang.org/en/v0.8.11/control-structures.html#checked-or-unchecked-arithmetic
        uint256 newItemId = tokenIds;
        token[newItemId].id_lotto = _id_lotto;
        token[newItemId].CO2 = _CO2;
        token[newItemId].old_nft_id = _old_nft_id;
        _mint(tokenOwner, newItemId);
        return newItemId;
    }

    //crea l'nft del fornitore
    //Il fornitore crea un nft da zero, il suo nft non punta a nessun altro nft. Non puo ricevere nft.
    function nft_fornitore(uint256 _id_lotto, uint256  _CO2) public {
        require(controllo_account(msg.sender, 1), "Non sei un fornitore");
        createItem(msg.sender, _id_lotto, _CO2, 0);
    }
    
    //crea l'nft del trasformatore
    //deve possedere l'nft piu recente associato al lotto per creare un nuovo nft. Puo a suo volta inviate l'nft ad un nuovo
    //trasformatore. Il suo nft punta sempre ad un altro nft, quello precedente associato al lotto.
    function nft_trasformatore(uint256 _old_nft_id, uint256 _id_lotto) public { 
        require(controllo_account(msg.sender, 2), "Non sei un trasformatore");

        require(controllo_lotto(msg.sender,token[_old_nft_id].id_lotto) == _old_nft_id, "Non stai lavorando sull'ultimo nft di questo lotto");

        //Il trasformatore può usare solo gli nft nel suo portafoglio
        require(ERC721.ownerOf(_old_nft_id) == msg.sender, "Non sei il proprietario dell'NFT"); 

        //Sommo i contributi
        uint256 totale = token[_old_nft_id].CO2 + temp_CO2[_id_lotto];
        temp_CO2[_id_lotto]=0;

        createItem(msg.sender, token[_old_nft_id].id_lotto, totale, _old_nft_id);
    }

    //restituisce 1 se l'account è presente in lista, 0 se non lo è
    //prende come parametri l'indirizzo dell'account da controllare e un bool con true se devo cercare tra i trasformatori, false se tra i fornitori
    function controllo_account(address _account, uint8 _tipo) private view returns (bool) {
        //require(_tipo >=1 && _tipo <= 3, "Tipo non valido");
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
        return false;
    }

    // Chiamata dal cliente per conoscere l'impronta
    function lettura_impronta_da_id_nft(uint256 _id_nft) public view returns (uint256,uint256,uint256) {
        require(_id_nft != 0 && _id_nft <= tokenIds, "Questo token non esiste");
        return (token[_id_nft].id_lotto, token[_id_nft].CO2, token[_id_nft].old_nft_id);
    }


    //solo trasformatori e clienti possono ricevere un nft
    function trasferimento_nft(address _to, uint256 _nftId) public {
        require(ERC721.ownerOf(_nftId) == msg.sender, "Non sei il proprietario dell'NFT");
        require(controllo_account(_to, 2) || controllo_account(_to, 3), "Destinatario e' un fornitore, non puo ricevere nft"); //solo trasformatori e clienti possono ricevere un nft
        require(!controllo_account(msg.sender, 3), "Sei un cliente, non puoi staferire nft");
        require(msg.sender != _to, "Sei gia' possessore di questo nft");       


        require(controllo_lotto(msg.sender,token[_nftId].id_lotto) == _nftId, "Puoi trasferire solo l'ultimo NFT creato di questo lotto");
        safeTransferFrom(msg.sender, _to, _nftId);
    }

    // Evento per emissione azione 
    event azione_trasformatore(string _nome_azione, uint256 _id_lotto, uint _CO2);

    function aggiungi_azione(string memory _nome_azione , uint256 _id_lotto, uint _CO2 ) public returns (bool) {
        require(controllo_account(msg.sender, 2), "Non sei un trasformatore");
        //EDIT
        require(controllo_lotto(msg.sender,_id_lotto) !=0, "Non possiedi l'ultimo NFT creato di questo lotto, non puoi fare azioni");
        temp_CO2[_id_lotto] += _CO2;
        emit azione_trasformatore(_nome_azione, _id_lotto, _CO2);
        return true;
    }

    function controllo_lotto (address _sender, uint256 _id_lotto) private view returns (uint256) {
        for (uint256 id = tokenIds; id >= 1; id--){
           if (token[id].id_lotto == _id_lotto){
               if (_sender == ownerOf(id)){
                    return id;
                } 
                else {
                return 0;
                }
            }
        }
        return 0;
    }

    //Ritorna l'ultimo nft associato ad un certo id_lotto
    function ricerca_lotto(uint256 _id_lotto) public view returns (uint256) {
        for (uint256 id = tokenIds; id >= 1; id--){
            if (token[id].id_lotto == _id_lotto){
                    return id;
            } 
        }
        return 0;
    }

}
/**    function aggiungi_azione(string memory _nome_azione , uint256 _id_lotto, uint _CO2 ) public returns (bool) {
            require(controllo_account(msg.sender, true), "Non sei un trasformatore");
            //EDIT
            bool esito;
            address account_owner;
            (uint256 _id_nft, ) = ricerca_lotto(_id_lotto);
            if (_id_nft != 0){
                account_owner = ownerOf(_id_nft);
            }
            else {
                account_owner = address(0);
            }
            if (msg.sender == account_owner){
                temp_CO2[_id_lotto] += _CO2;
                emit azione_trasformatore(_nome_azione, _id_lotto, _CO2);
                esito = true;
            }
            else {
                esito = false;
            }
            return esito; //true se il lotto c'è, false se non c'è
        }


    
    //EDIT
    function ricerca_lotto(uint256 _id_lotto) public view returns (uint256, uint256) {
        uint256 id_nft_fornitore = 0;
        uint256 id_nft_trasformatore = 0;

        for (uint256 id; id <= tokenIds; id++){
            if (token[id].id_lotto == _id_lotto){
                if (token[id].old_nft_id == 0){
                    id_nft_fornitore = id;
                }
                else {
                    id_nft_trasformatore = id;
                }
            }
        }
        return (id_nft_fornitore, id_nft_trasformatore); 
    }


}

*/


//TODO
//Rendere interne le funzioni pubbliche ereditate da ERC721 (sennò posso passare token da trasf. a fornitore, ad esempio)
//Risolvere warning

//sulla relazione mettere cosa fare degli nft usati
//sulla relazione dire che solisity 0.8.0 controlla overflow e underflow

