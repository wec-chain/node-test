from p2pnetwork.node import Node
from PeerDiscoveryHandler import PeerDiscoveryHandler
from SocketConnector import SocketConnector
from BlockchainUtils import BlockchainUtils
import json
import os
from dotenv import load_dotenv

load_dotenv()

class SocketCommunication(Node):

    def __init__(self, ip, port):
        super(SocketCommunication, self).__init__(ip, port, None)
        self.peers = []
        self.peerDiscoveryHandler = PeerDiscoveryHandler(self)
        self.socketConnector = SocketConnector(ip, port)
        self.firstNodeIP = os.getenv('FIRST_NODE_IP')
        self.firstNodePort = int(os.getenv('FIRST_NODE_NETWORK_PORT'))

    def connectToFirstNode(self):
        if self.socketConnector.port != self.firstNodePort:
            self.connect_with_node(self.firstNodeIP, self.firstNodePort)

    def startSocketCommunication(self, node):
        self.node = node
        self.start()
        self.peerDiscoveryHandler.start()
        self.connectToFirstNode()

    def inbound_node_connected(self, connected_node):
        self.peerDiscoveryHandler.handshake(connected_node)

    def outbound_node_connected(self, connected_node):
        self.peerDiscoveryHandler.handshake(connected_node)

    def node_message(self, connected_node, message):
        message = BlockchainUtils.decode(json.dumps(message))
        if message.messageType == 'DISCOVERY':
            self.peerDiscoveryHandler.handleMessage(message)
        elif message.messageType == 'TRANSACTION':
            transaction = message.data
            self.node.handleTransaction(transaction)
        elif message.messageType == 'BLOCK':
            block = message.data
            self.node.handleBlock(block)
        elif message.messageType == 'BLOCKCHAINREQUEST':
            self.node.handleBlockchainRequest(connected_node)
        elif message.messageType == 'BLOCKCHAIN':
            blockchain = message.data
            self.node.handleBlockchain(blockchain)

    def send(self, receiver, message):
        self.send_to_node(receiver, message)

    def broadcast(self, message):
        self.send_to_nodes(message)
