from web3 import Web3
from solcx import compile_source, set_solc_version_pragma
set_solc_version_pragma('0.8.17')
id=7
excuteContractIp="HTTP://127.0.0.1:8545"
privateKey="0x908b52eff975958dcb0ce5bb97be27b26048ab60e1229f7768a7f3ed86d61bf7"
commandIp="http://127.0.0.1:5000"
teeEncryptionKey="5ae0af3a9c6f8b6e62ad8c6ec76c6cf796a4bf75452c2cd58e1d811e78dac56fc23f86355dd4a81f826a8879b144e48079a0eb3873146ff4cf85409af2909d4c"


w3_address="HTTP://127.0.0.1:7545"
contract_address="0xa63c3Bc878DA4E78C989050A045801615a60348e"
sol_file="/home/guanfujun/毕业设计/ETH-Main/contracts/PoseManager.sol"
w3=None
manager=None
w3 = Web3(Web3.HTTPProvider(w3_address))
print(w3)
with open(sol_file, 'r') as f:
    source = f.read()
compiled_sol = compile_source(source)
contract_id, contract_interface = compiled_sol.popitem()
manager = w3.eth.contract(address=contract_address, abi=contract_interface["abi"])
tx_hash=manager.functions.register(id,excuteContractIp,privateKey,commandIp,teeEncryptionKey,"0xa2972539a3B15757eaF4CAD7B9666A0D6c022E3A").transact({"from":"0xE9B5f165d01C612675adB3914d368fff75160512"})
# tx_hash=manager.functions.registeredOperators(3).call();
print(tx_hash)