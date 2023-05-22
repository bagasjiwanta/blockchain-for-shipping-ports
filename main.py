import hashlib
from pydantic import BaseModel
import json
from datetime import datetime
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
BASE_KEY = "ports/keys/"
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


class TContainer(BaseModel):
    items: list[TContainerItem]
    name: str
    source: str
    destination: str


class TBlock(BaseModel):
    timestamp: datetime
    block_contents: TContainer
    previous_signature: str
    current_signature: str


class Block:
    def __init__(self, block: TBlock):
        self.previous_hash = block.previous_signature
        self.block_contents = block.block_contents
        self.timestamp = block.timestamp
        self.current_hash = block.current_signature


def tamper_gilimanuk_database():
    with open(os.path.join(os.getcwd(), "ports", "gilimanuk.json"), "r") as f:
        chain = json.loads(f.read())


class Peer:
    def __init__(self, name: str):
        self.name = name
        self.chain: list[Block] = [
            {
                "block_contents": [],
                "current_hash": "988569fbbca72b69e533075ca1ae154dc064d1ae39b45caa67ec42f92096897cabe966c300be2baaa8bc1d5038ec0d1280b3fd2ba2978838ff98e6df2ea97bc6",
                "previous_hash": "",
                "signature": "",
                "timestamp": datetime.fromisoformat("2023-05-22T18:05:48.672870")
            }
        ]
        self.private_key = RSA.generate(1024)
        self.public_key = self.private_key.public_key()

    def send(self, destination: str, block_contents: TContainer):
        block_contents['destination'] = destination
        block_contents['source'] = self.name

        previous_hash = self.chain[-1].get_hash()
        block_contents.destination = destination
        timestamp = datetime.now().isoformat()
        block = Block()
        pass

    def generate_sign(self, string: str):
        signer = pkcs1_15.new(RSA.import_key(
            open(BASE_KEY + self.name + "/private.pem").read()))
        hasher = SHA256.new()
        hasher.update(string.encode())
        signature = signer.sign(hasher)
        return signature

    def verify_sign(self, string: str, signature: bytes):
        verifier = pkcs1_15.new(RSA.import_key(
            open(BASE_KEY + self.name + "/public.pem")
        ))
        hasher = SHA256.new()
        hasher.update(string.encode())
        try:
            verifier.verify(hasher, signature.encode())
            return True
        except:
            return False


class Peers:
    def __init__(self, name: str):
        self.peers = []

    def add(self, peer: Peer):
        self.peers.append(peer)


def sign_genesis_block():
    files = [
        "gilimanuk.json",
        "labuan_bajo.json",
        "rinca.json",
        "waingapu.json"
    ]

    for i in files:
        with open(os.path.join(os.getcwd(), "ports", i), "r") as f:
            chain = json.loads(f.read())


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
    gilimanuk.send("labuan_bajo", {
        "name": "gilimanuk - labuan bajo - 1",
        "items": [
            {
                "weight_kg": 200,
                "item_name": "Baju",
            }
        ]
    })

    labuan_bajo.send("rinca", {
        "name": "labuan bajo - rinca - 1",
        "items": [
            {
                "weight_kg": 400,
                "item_name": "pakan ternak",
            }, {
                "weight_kg": 500,
                "item_name": "galian c"
            }
        ]
    })

    labuan_bajo.send("waingapu", {
        "name": "labuan bajo - waingapu - 1",
        "items": [
            {
                "weight_kg": 800,
                "item_name": "baju",
            }, {
                "weight_kg": 100,
                "item_name": "buah kering"
            }
        ]
    })

    waingapu.send("rinca", {
        "name": "waingapu - rinca - 1",
        "items": [
            {
                "weight_kg": 200,
                "item_name": "kosmetik",
            }, {
                "weight_kg": 1000,
                "item_name": "tembakau"
            }
        ]
    })

    tamper_gilimanuk_database()

    gilimanuk.send("labuan_bajo", {
        "name": "gilimanuk - labuan bajo - 2",
        "items": [
            {
                "weight_kg": 900,
                "item_name": "buah kering",
            }
        ]
    })

    # gilimanuk tries to modify past data and sends new block

    # new block gets rejected
