from flask_classful import FlaskView, route
from flask import Flask, jsonify, request, render_template
from BlockchainUtils import BlockchainUtils
import os
from dotenv import load_dotenv

load_dotenv()

node = None


class NodeAPI(FlaskView):

    def __init__(self):
        self.app = Flask(__name__)

    def start(self, port):
        NodeAPI.register(self.app, route_base='/')
        self.app.run(host=os.getenv('CURRENT_NODE_IP'), port=port)

    def injectNode(self, injectedNode):
        global node
        node = injectedNode

    @route('/', methods=['GET'])
    def home(self):
        blocksCount = len(node.blockchain.toJson()['blocks'])
        nodes_count = 0

        i = 0
        for block in node.blockchain.toJson()['blocks']:
            i = i + len(block['transactions'])

        return render_template('index.html', blocksCount=blocksCount, transactionsCount=i,
                               blocks=list(reversed(node.blockchain.toJson()['blocks'])), nodes_count=nodes_count)

    @route('/transactions', methods=['GET'])
    def transactions(self):
        return render_template('transactions.html', blocks=list(reversed(node.blockchain.toJson()['blocks'])))

    @route('/blocks', methods=['GET'])
    def blocks(self):
        return render_template('blocks.html', blocks=list(reversed(node.blockchain.toJson()['blocks'])))

    @route('/info', methods=['GET'])
    def info(self):
        return 'This is a communiction interface to a nodes blockchain', 200

    @route('/blockchain', methods=['GET'])
    def blockchain(self):
        return node.blockchain.toJson(), 200

    @route('/transactionPool', methods=['GET'])
    def transactionPool(self):
        transactions = {}
        for ctr, transaction in enumerate(node.transactionPool.transactions):
            transactions[ctr] = transaction.toJson()
        return jsonify(transactions), 200

    @route('/transaction', methods=['POST'])
    def transaction(self):
        values = request.get_json()
        if not 'transaction' in values:
            return 'Missing transaction value', 400
        transaction = BlockchainUtils.decode(values['transaction'])
        node.handleTransaction(transaction)
        response = {'message': 'Received transaction'}
        return jsonify(response), 201
