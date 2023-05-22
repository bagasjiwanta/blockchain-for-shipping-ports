import hashlib
from pydantic import BaseModel
import json
from datetime import datetime
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Hash import SHA3_256
from rsa import PrivateKey, PublicKey
BASE_KEY = "keys/"
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


class Peer:
    def __init__(self, name: str):
        self.name = name
        self.chain: list[TBlock] = [
            {
                "block_contents": [],
                "current_hash": "04017c33d53cd1d768b58105544d9c4c5a56df3a1bd843ece676c8a569902aa0",
                "previous_hash": "",
                "signature": "",
                "timestamp": "2023-05-22T18:05:48.672870"
            }
        ]
        print(self.generate_sign(self.chain[0]))

    def strip_block(self, block: TBlock):
        return {
            "block_contents": block['block_contents'],
            "current_hash": block['current_hash'],
            "timestamp": block['timestamp']
        }

    def send(self, destination: str, block_contents: TContainer):
        block_contents['destination'] = destination
        block_contents['source'] = self.name

        previous_hash = self.chain[-1].get_hash()
        block_contents.destination = destination
        timestamp = datetime.now().isoformat()
        pass

    def generate_sign(self, block):
        private_key = PrivateKey.read_from_file(
            "keys/" + "main" + "/private.txt")
        string = json.dumps(self.strip_block(block), sort_keys=True)
        hash = int.from_bytes(SHA3_256.new(string.encode()).digest())
        sign = private_key.encrypt(hash)
        return sign

    def verify_sign(self, string: str, signature: bytes):
        verifier = pkcs1_15.new(RSA.import_key(
            open(BASE_KEY + "main" + "/public.txt").read()
        ))
        hasher = SHA256.new(string.encode())
        try:
            verifier.verify(hasher, signature.encode())
            return True
        except:
            return False


class Peers:
    def __init__(self):
        self.peers = []

    def add(self, peer: Peer):
        self.peers.append(peer)


if __name__ == "__main__":
    reset_data()

    # init ports
    gilimanuk = Peer("gilimanuk")
    labuan_bajo = Peer("labuan_bajo")
    rinca = Peer("rinca")
    waingapu = Peer("waingapu")

    peers = Peers()
    peers.add(gilimanuk)
    peers.add(labuan_bajo)
    peers.add(rinca)
    peers.add(waingapu)

    # do some transactions
    # gilimanuk.send("labuan_bajo", {
    #     "name": "gilimanuk - labuan bajo - 1",
    #     "items": [
    #         {
    #             "weight_kg": 200,
    #             "item_name": "Baju",
    #         }
    #     ]
    # })

    # labuan_bajo.send("rinca", {
    #     "name": "labuan bajo - rinca - 1",
    #     "items": [
    #         {
    #             "weight_kg": 400,
    #             "item_name": "pakan ternak",
    #         }, {
    #             "weight_kg": 500,
    #             "item_name": "galian c"
    #         }
    #     ]
    # })

    # labuan_bajo.send("waingapu", {
    #     "name": "labuan bajo - waingapu - 1",
    #     "items": [
    #         {
    #             "weight_kg": 800,
    #             "item_name": "baju",
    #         }, {
    #             "weight_kg": 100,
    #             "item_name": "buah kering"
    #         }
    #     ]
    # })

    # waingapu.send("rinca", {
    #     "name": "waingapu - rinca - 1",
    #     "items": [
    #         {
    #             "weight_kg": 200,
    #             "item_name": "kosmetik",
    #         }, {
    #             "weight_kg": 1000,
    #             "item_name": "tembakau"
    #         }
    #     ]
    # })

    # tamper_gilimanuk_database()

    # gilimanuk.send("labuan_bajo", {
    #     "name": "gilimanuk - labuan bajo - 2",
    #     "items": [
    #         {
    #             "weight_kg": 900,
    #             "item_name": "buah kering",
    #         }
    #     ]
    # })
