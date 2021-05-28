# Blockchain
# Tools
Written and complied using Spyder
Flask
Postman
Remix Ethereum
Blockchain With Cryptocurrency Demo
Connect the blockchain nodes, exchange 'Hadcoins', and mine blocks. For any blocks added, get consensus by calling replace_chain. Get the blockchain and check if it is valid.

Run hadcoin_node_[port].py in separate consoles.
Using Postman, send requests to http://127.0.0.1:[port]/
Send POST connect_node requests to all nodes. Paste nodes.json in request body. Remove receiving node from the post request body. For example, if sending POST connect_node to http://127.0.0.1:5001/ remove http://127.0.0.1:5001/ from the request body.
Send GET mine-block to any node.
Send POST replace_chain on other nodes.
Send POST add_transaction to any node. Paste transaction.json in request body. Replace sender and receiver strings with any name, and amount with any integer.
Send GET mine_block to mine the transaction to the blockchain.
Send POST replace_chain on other nodes to update the blockchain.
GET methods
get_chain - gets the full blockchain.
mine_block - adds a block to the blockchain.
is_valid - checks if the blockchain is valid.
POST methods
connect_node - connects a node to the blockchain
add_transaction - adds a new transaction to the blockchain
replace_chain - replaces the chain with the longest chain if needed
Ethereum Smart Contract
A smart contract written in Solidity for the Ethereum blockchain. Compile, deploy, and run transactions using Remix Ethereum. Paste hadcoins_ico.sol into main panel
