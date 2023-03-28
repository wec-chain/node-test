from Node import Node
import sys
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    ip = os.getenv('CURRENT_NODE_IP')
    port = int(os.getenv('CURRENT_NODE_FLASK_PORT'))
    apiPort = int(os.getenv('CURRENT_NODE_NETWORK_PORT'))
    keyFile = None
    if len(sys.argv) > 1:
        keyFile = sys.argv[1]
    node = Node(ip, apiPort, keyFile)
    node.startP2P()
    node.startAPI(port)