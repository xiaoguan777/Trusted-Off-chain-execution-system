from web3 import Web3;
import os;
from solcx import compile_standard, install_solc
import json
w3=Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8547"))
with open("/home/guanfujun/毕业设计/ETH-Main/contracts/PoseManager.sol","r") as file:
    simple_storage_file=file.read()
    install_solc("0.8.17")
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"PoseManager.sol": {"content": simple_storage_file}},
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            },
        },
        solc_version="0.8.17",
    )
    with open("compiled.json", "w") as file:
        json.dump(compiled_sol, file)
        # get bytecode
        bytecode = compiled_sol["contracts"]["PoseManager.sol"]["PoseManager"]["evm"][
            "bytecode"
        ]["object"]

        # get abi
        abi = compiled_sol["contracts"]["PoseManager.sol"]["PoseManager"]["abi"]
        SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
        nonce = w3.eth.get_transaction_count("0x291408AB95E278C3721E8309f176fCDDb2ECE2a2")

        transaction = SimpleStorage.constructor().buildTransaction(
            {
                "chainId": 1337,
                "gasPrice": w3.eth.gas_price,
                "from": "0x291408AB95E278C3721E8309f176fCDDb2ECE2a2",
                "nonce": nonce,
            }
        )
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key="0xe9d10dba5acd80669decec54d597ac089bea6e769730c128109f6acb8e43016f")
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(tx_receipt.contractAddress)




