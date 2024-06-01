// SPDX-License-Identifier: MIT
pragma solidity^ 0.8.17;
contract PoseManager{
    struct Operator{
        uint id;
        string excuteContractIp;
        string privateKey; 
        string commandIp;
        string teeEncryptionKey;
        string contractAddress;
    }
    struct Contract {
        uint id;
        address payable poolAddress;
        address creationOperator;
        uint operatorNums;  
    }
    mapping (uint => Operator)public  registeredOperators;
    uint[] public  opratorNums;
    mapping (uint => Contract) public  contracts;
    uint[] public  contractNums;
    function register(uint id,string memory excuteContractIp,string memory privateKey,string memory commandIp,string memory teeEncryptionKey,string memory contractAddress) public {
        require(verifyOpRepeadId(id),"OpId repead");
        registeredOperators[id]=Operator(id,excuteContractIp,privateKey,commandIp,teeEncryptionKey,contractAddress);
        opratorNums.push(id);
        
    }
    function initCreation(uint id,address payable poolAddress,address creationOperator,uint Oid,string memory contractAddress,
    uint operatorNums) public {
        require(verifyCoRepeadId(id),"CoId repead");
        contracts[id]=Contract(id,poolAddress,creationOperator,operatorNums);
        contractNums.push(id);

    }
    function watchDogResponse(uint id) public {
        require(!verifyOpRepeadId(id),"No OpId");
        uint index;
        for(uint i=0;i<opratorNums.length;i++){
            if(opratorNums[i]==id){
                index=i;
                break ;
            }
        }
        for(uint i =index;i<opratorNums.length-1;i++){
            opratorNums[i]=opratorNums[i+1];
        }
        opratorNums.pop();
        registeredOperators[id]=Operator(0,"","","","","");
    }
    function depositToContract(uint id) public payable {
        contracts[id].poolAddress.transfer(msg.value);
    }
    function withdraw(address payable receiver) public payable{
        receiver.transfer(msg.value);
    }
    function verifyOpRepeadId(uint id) public view returns  (bool){
        for(uint i=0;i<opratorNums.length;i++){
            if(opratorNums[i]==id){
                return false;
            }
        }
        return true;
    }
     function verifyCoRepeadId(uint id) public view returns  (bool){
        for(uint i=0;i<contractNums.length;i++){
            if(contractNums[i]==id){
                return false;
            }
        }
        return true;
    }   

}