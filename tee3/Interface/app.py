from flask import Flask, request,jsonify
from flask_cors import CORS
import requests
from web3 import Web3
from ecdsa import SigningKey, VerifyingKey, NIST256p
import hashlib
import json
import base64
from solcx  import compile_source, set_solc_version_pragma
app = Flask(__name__)
CORS(app)


@app.route('/check',methods=["GET"])
def check():  # put application's code here
    set_solc_version_pragma('0.8.17')
    w3_address = "HTTP://127.0.0.1:7545"
    contract_address = '0xa63c3Bc878DA4E78C989050A045801615a60348e'
    sol_file = "/home/guanfujun/毕业设计/ETH-Main/contracts/PoseManager.sol"
    w3 = Web3(Web3.HTTPProvider(w3_address))
    with open(sol_file, 'r') as f:
        source = f.read()
    compiled_sol = compile_source(source)
    contract_id, contract_interface = compiled_sol.popitem()
    manager = w3.eth.contract(address=contract_address, abi=contract_interface["abi"])
    url=None
    vk=None
    while(True):
        i=7
        resp=manager.functions.registeredOperators(i).call()
        if(resp[0]!=0):
            url=resp[3]
            vk=resp[4]
            break
    response = requests.get(url+"/votesReceived")
    json_data=json.loads(response.text)
    data=json_data["data"]
    dataSig=json_data["dataSig"]
    total=json_data["total"]
    totalSig=json_data["totalSig"]
    vk_bytes=bytes.fromhex(vk)
    verifyingKey= VerifyingKey.from_string(vk_bytes, curve=NIST256p)
    hash_obj = hashlib.sha256(str(data).encode()).digest()
    dataSig=base64.b64decode(dataSig)
    check1=verifyingKey.verify(dataSig,hash_obj)
    print(check1)
    totalSig=base64.b64decode(totalSig)
    hash_obj = hashlib.sha256(str(total).encode()).digest()
    check2 = verifyingKey.verify(totalSig, hash_obj)
    print(check2)
    if(check1 and check2):
        set_solc_version_pragma('0.8.17')
        w3_address = "HTTP://127.0.0.1:8546"
        contract_address = '0xE64Bc785EdD7eD4f80283EBdE9601b70cd22E800'
        sol_file = "/home/guanfujun/毕业设计/tee1/poseVoting/contracts/Voting.sol"
        w3 = Web3(Web3.HTTPProvider(w3_address))
        with open(sol_file, 'r') as f:
            source = f.read()
        compiled_sol = compile_source(source)
        contract_id, contract_interface = compiled_sol.popitem()
        manager = w3.eth.contract(address=contract_address, abi=contract_interface["abi"])
        piaoshu=manager.functions.totalVotesFor(json_data['data']).call()
        print(json_data['total'])
        print("piaoshu",piaoshu)
        for i in range(0,json_data['total']-piaoshu):
            print("测试")
            manager.functions.voteForCandidate(json_data['data']).transact({'from':"0xD9d958EF46A14fEf49AC708C978c29c316B5f4B9"})
        return 'right'
    else:
        set_solc_version_pragma('0.8.17')
        w3_address = "HTTP://127.0.0.1:7545"
        contract_address = '0xa63c3Bc878DA4E78C989050A045801615a60348e'
        sol_file = "/home/guanfujun/毕业设计/ETH-Main/contracts/PoseManager.sol"
        w3 = Web3(Web3.HTTPProvider(w3_address))
        with open(sol_file, 'r') as f:
            source = f.read()
        compiled_sol = compile_source(source)
        contract_id, contract_interface = compiled_sol.popitem()
        manager = w3.eth.contract(address=contract_address, abi=contract_interface["abi"])
        manager.functions.watchDogResponse(7).transact({'from':"0xE9B5f165d01C612675adB3914d368fff75160512"})
        return 'wrong'
@app.route('/votesReceived',methods=["GET"])
def votesReceived():  # put application's code here
    set_solc_version_pragma('0.8.17')
    w3_address = "HTTP://127.0.0.1:8545"
    contract_address = '0xa2972539a3B15757eaF4CAD7B9666A0D6c022E3A'
    sol_file = "/home/guanfujun/毕业设计/tee1/poseVoting/contracts/Voting.sol"
    w3 = Web3(Web3.HTTPProvider(w3_address))
    with open(sol_file, 'r') as f:
        source = f.read()
    compiled_sol = compile_source(source)
    contract_id, contract_interface = compiled_sol.popitem()
    manager = w3.eth.contract(address=contract_address, abi=contract_interface["abi"])
    sum = manager.functions.sum().call()
    data=manager.functions.data(sum-1).call()
    total=manager.functions.totalVotesFor(data).call();
    print(total)
    sk="7ead6528a5272cf9d7f7dfa2071574f62a023d3dccfdf058d636834bd9c20b01"
    sk_bytes=bytes.fromhex(sk)
    signingKey= SigningKey.from_string(sk_bytes, curve=NIST256p)
    data_encode=str(data).encode()
    total_encode=str(total).encode()
    hash_obj = hashlib.sha256(data_encode).digest()
    dataSig =signingKey.sign(hash_obj)
    dataSig=base64.b64encode(dataSig).decode("ascii")
    print(dataSig)
    print(str(dataSig))
    hash_obj = hashlib.sha256(total_encode).digest()
    totalSig = signingKey.sign(hash_obj)
    totalSig=base64.b64encode(totalSig).decode("ascii")
    send={"data":data,
          "total":total,
          "dataSig":dataSig,
          "totalSig":totalSig}
    return jsonify(send)



if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5002)
