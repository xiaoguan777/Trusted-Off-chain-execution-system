import web3.eth
from web3 import Web3;
from solcx import compile_source, set_solc_version_pragma
set_solc_version_pragma('0.8.17')
w3_address="HTTP://127.0.0.1:7545"
contract_address="0xa63c3Bc878DA4E78C989050A045801615a60348e"
sol_file="/home/guanfujun/毕业设计/ETH-Main/contracts/PoseManager.sol"
id=1
creationOperator=Web3.toChecksumAddress("0xE9B5f165d01C612675adB3914d368fff75160512")
poolAddress=Web3.toChecksumAddress("0x0859c770C4c9D3ec902D20Df732e1Ab0a01AE217")
print(creationOperator)
operatorNums=3
w3=None
manager=None
w3 = Web3(Web3.HTTPProvider(w3_address))
print(w3)
with open(sol_file, 'r') as f:
    source = f.read()
compiled_sol = compile_source(source)
contract_id, contract_interface = compiled_sol.popitem()
manager = w3.eth.contract(address=contract_address, abi=contract_interface["abi"])
# 获取已经注册的可信环境
# for i in range(1,4):
#     tx_hash = manager.functions.opratorNums(i).call();
tx_hash=manager.functions.initCreation(id,poolAddress,creationOperator,1,"0",operatorNums).transact({"from":"0xE9B5f165d01C612675adB3914d368fff75160512"})
# tx_hash=manager.functions.withdraw("0x8157f0fe9B6f86c79E46ea76DD2A27e8d07eD44D").transact({"from":"0x8157f0fe9B6f86c79E46ea76DD2A27e8d07eD44D"})
# print(tx_hash)
