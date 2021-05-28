

# ----------------==================creating a cryptocurrency - "Vikoin"================-------------------

import datetime
import hashlib
import json #used to encode block before hashing
from flask import Flask, jsonify, request #used to display block to postman
import requests
from uuid import uuid4
from urllib.parse import urlparse #to parse the address of the node

# ----------------=================="building a blockchain"=================-----------------------

class blockchain:
    def __init__(self):
        self.chain=[]#list of chain containing blocks
        self.transactions=[]#mempool:- (temporary storage of transactions)
        self.create_block(proof=1,prev_hash='0')#genesis block, proof of block
        self.nodes=set()#record of nodes added or joined
        
    def create_block(self,proof,prev_hash):
                #4 essential keys of the block(can be increased)
        block={'index':len(self.chain)+1,#this stores the length of blockchain
               'timestamp':str(datetime.datetime.now()),
               #stores the date & time of creation of the block
               #now means realtime data of date & time 
               'proof':proof,
               'prev_hash':prev_hash,
               'transactions': self.transactions}
        self.transactions=[]#emptying the transactions list for new transactions
        self.chain.append(block)#adds new block to the chain
        return block#returns info to the postman
    
    def get_prev_block(self):#to get last block in the chain
        return self.chain[-1]
    
    def proof_of_work(self,prev_proof):#gives a problem to miners to solve
        #using a trial and error method
        new_proof=1#starting new proof
        check_proof=False#proof is false initially as new_proof=1 is not the solution
        while check_proof is False:
            hash_operation=hashlib.sha256(str(new_proof**2 - prev_proof**2).encode()).hexdigest()
#calling sha256 from hashlib library, (new_proof**2 - prev_proof**2) this is our non-symmetrical expression
#encode() encodes into right format,hexdigest() converts into hash with 64 char
            if hash_operation[:5]=='00000':
                #if 1st 8 char are 00000 in hash then true,loop ends
                check_proof=True
            else :
                new_proof+=1
        return new_proof
    
    def hash(self,block):#takes block as input and returns its hash value for checking purpose
        encoded_block=json.dumps(block,sort_keys=True).encode()
        #dumps fn from json library converts object into string
        #sort_keys maintains the right order of the keys in block object
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self,chain):#cond.1:- checks previous hash of each block is equal to its prev block
                                   #cond.2:- also checks proof of work is valid or not
        prev_block=chain[0]#initializing
        block_index=1#initializing
        while block_index < len(chain):
            block=chain[block_index]
            if block['prev_hash'] != self.hash(prev_block):
                return False#cond.1 not satisfied
            prev_proof=prev_block['proof']#we get proof of prev block from prev block
            proof = block['proof']
            hash_operation=hashlib.sha256(str(proof**2-prev_proof**2).encode()).hexdigest()
            if hash_operation[:5] != '00000':
                return False#cond.2 not satisfied
            prev_block=block
            block_index+=1
        return True
    
    def add_transaction(self, sender, receiver, amount): #adding transactions
        self.transactions.append({'sender': sender,
                                  'receiver': receiver,
                                  'amount': amount})
        prev_block = self.get_prev_block()
        return prev_block['index'] + 1
        
    def add_node(self,address):#adds the new user or node to the network
        parsed_url=urlparse(address)#PARSES the url address
        self.nodes.add(parsed_url.netloc)
        
    def replace_chain(self):# the chain having max blocks is genuine  (concensus protocol)
        network=self.nodes#set of nodes all around the world
        longest_chain=None
        max_length=len(self.chain)#getting length of the chain
        for node in network:#getting all the chains on the network for comparision
            response = requests.get(f'http://{node}/get_chain')#request will call the get_chain() method for length of chain of that user
            #f'' is the f string fn "we can put variable 'node=127.0.0.1.:5000' in bwn the string" to get address of every particolar node
            if response.status_code== 200:
                length=response.json()['length']#to get the length of a particular chain 
                chain=response.json()['chain']#picks the chain of the same particular chain from the dictionary
                if length > max_length and self.is_chain_valid(chain):
                    max_length=length
                    longest_chain=chain
        if longest_chain:#if longest chain is replaced
            self.chain=longest_chain#making longest_chain the orignal chain
            return True
        return False
    
# ----------------=================="mining our blockchain"=================-------------------------
        
    #creating a web app using flask
app=Flask(__name__)  #Flask quickstart guide
    
    #creating an address for the node on the port 5000
node_address = str(uuid4()).replace('-','')#UUID('{12345678-1234-5678-1234-567812345678}') Ex of a uuid4 code
    #to keep track and reward the miner of the block

    #creating a blockchain
blockchain=blockchain()

    #mining a new block
@app.route('/mine_block',methods=['GET'])#get keyword will get us something, @app.route is a fn of flask
#before/mine__block we will have our url from where we have to do mining. eg: (http://127.0.0.1:5000/mine_block)
def mine_block():
    prev_block=blockchain.get_prev_block()#this fn will give us the last block of the chain
    prev_proof=prev_block['proof']#we get proof of prev block from prev block
    proof=blockchain.proof_of_work(prev_proof)#this will give proof of the next block joining blockchain
    prev_hash=blockchain.hash(prev_block)#ths will give the hash of the prev block
    #now we have everything to create a new block(hash of prev block and proof of current block)
    blockchain.add_transaction(sender=node_address, receiver='Varun', amount=100)#adding transaction details to the BC
    block=blockchain.create_block(proof,prev_hash)#create a new block
    response={'message':f'New block mined. Enjoy Vikoin',
              'index':block['index'],
              'timestamp':block['timestamp'],
              'proof':block['proof'],
              'prev_hash':block['prev_hash'],
              'transactions':block['transactions']}#adding transactions to the block
              #adding keys to new block
    return jsonify(response),200#200 is the HTTP status code, standard response for successful HTTP requests. Google it for info
    #jsonify is used to return in the json format
    
#getting the full blockchain
@app.route('/get_chain',methods=['GET'])
#this will get us or show us our full blockchain
def get_chain():
    response={'chain':blockchain.chain,#return us full blockchain
              'length':len(blockchain.chain)}#returns us the length of the full blockchain
    return jsonify(response),200

# Checking if the Blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():#checks valdity of blockchain
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:#if is_valid == True
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Bro, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200

#adding a new transaction to the BC
@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all(key in json for key in transaction_keys):#if any of the sender receiver or amount is not entered
         return 'Some elements of the transaction are missing', 400
    index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount'])#json picks the values these variables hold
    response = {'message': f'This transaction will be added to Block {index}'}
    return jsonify(response), 201#201 is the standard response for successful HTTP POST requests. Google it for info


# ------------------=================== "Decentralization" =================--------------------

#connecting new nodes
@app.route('/connect_node', methods = ['POST'])
def connect_node():#connect new node to the blockchain
    json=request.get_json()
    nodes=json.get('nodes')# gives us the addresses of the various nodes in json format
    if nodes is None:
        return "No node", 400
    for node in nodes:#for adding diff nodes one by one
        blockchain.add_node(node)#using the add_node fn
    response = {'message':'Every node is connected. The nodes are: ',
                'total_nodes': list(blockchain.nodes)}#lists the total nodes in the BC
    return jsonify(response),201

#replacing the chain by longest chain if needed     (Consensus Protocol)
@app.route('/replace_chain', methods = ['GET'])
def replace_chain(): #replace those chains which are not updated with new block
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:#if is_chain_replaced == True
        response = {'message': 'Longest chain replaced the existing chain',
                    'new_chain':blockchain.chain}
    else:
        response = {'message': 'No change, the chain is valid one',
                    'actual_chain':blockchain.chain}
    return jsonify(response), 200

#running the app
app.run(host = '0.0.0.0', port = 5005)
