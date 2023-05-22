import hashlib
from pydantic import BaseModel
import json
from datetime import datetime
import os

INITIAL_DATA = '''[
  {   
    "block_contents": [],
    "previous_hash": "",
    "timestamp": "2023-05-22T18:05:48.672870"
  }
]'''


def reset_data():
    files = [
        "gilimanuk.json",
        "labuan_bajo.json",
        "rinca.json",
        "waingapu.json"
    ]

    for i in files:
        with open(os.path.join(os.getcwd(), "ports", i), "w") as f:
            f.write(INITIAL_DATA)


class TContainerItem(BaseModel):
    weight_kg: float
    item_name: str
    item_description: str


class TContainer(BaseModel):
    items: list[TContainerItem]
    name: str
    source: str
    destination: str


class TBlock(BaseModel):
    timestamp: datetime.now().isoformat()
    block_contents: list[TContainer]
    previous_hash: str


class ShippingTransactionBlock:
    def __init__(self, previous_hash: str, block_contents: list[TContainer], timestamp=datetime.now()):
        self.previous_hash = previous_hash
        self.block_contents = block_contents
        self.timestamp = timestamp

    def get_hash(self):
        string = json.dumps(self, sort_keys=True)
        digest = hashlib.sha512(string.encode()).hexdigest()
        return digest


def tamper_gilimanuk_database():
    with open(os.path.join(os.getcwd(), "ports", "gilimanuk.json"), "r") as f:
        chain = json.loads(f.read())


class Peer:
    def __init__(self, name: str):
        self.name = name
        self.chain = None
        self.refresh_chain()

    def refresh_chain(self):
        with open(os.path.join(os.getcwd(), "ports", self.name + ".json"), "r") as f:
            chain = json.loads(f.read())
            self.chain = chain
            print(chain)

    def send(self, destination: str, block_contents: list[TContainer]):
        pass


class Peers:
    def __init__(self):
        self.peers = []

    def add(self, peer: Peer):
        self.peers.append(peer)

    def mine(self):
        solution = 1


if __name__ == "__main__":
    reset_data()

    # init ports
    gilimanuk = Peer()
    labuan_bajo = Peer()
    rinca = Peer()
    waingapu = Peer()

    peers = Peers()
    peers.add(gilimanuk)
    peers.add(labuan_bajo)
    peers.add(rinca)
    peers.add(waingapu)

    # do some transactions
    gilimanuk.send()

    # gilimanuk tries to modify past data and sends new block

    # new block gets rejected
