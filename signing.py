from Crypto.Hash import SHA3_256
from lib.rsa import PublicKey, PrivateKey
from lib.exception import SignatureNotFound, SignatureCorrupted, FileOrKeyModified

BUFFER_SIZE = 65536

def sign_binary_file(input_file_name: str, key_file_name: str, public_key: PrivateKey):
    '''menambahkan digital signature dari file binary ke file text'''
    with open(input_file_name, "rb") as f:
        content = f.read(BUFFER_SIZE)
    
    hash = int.from_bytes(SHA3_256.new(content).digest())
    signature = public_key.decrypt(hash)
    output = "<ds>" + str(signature) + "</ds>\n"

    with open(key_file_name, "w") as f:
        f.write(output)


def sign_text_file(input_file_name:str, output_file_name:str, public_key: PrivateKey):
    '''menambahkan digital signature ke file text'''
    with open(input_file_name, "r") as f:
        content = f.read()

    hash = int.from_bytes(SHA3_256.new(content.encode()).digest())
    signature = public_key.decrypt(hash)
    output = content+ "\n<ds>" + str(signature) + "</ds>"

    with open(output_file_name, "w") as f:
        f.write(output)
    

def verify_binary_file(input_file_name: str, key_file_name: str, private_key: PublicKey):

    with open(key_file_name, "r") as f:
        content = f.read()
    
    start_tag = content.find("<ds>")
    if start_tag == -1:
        raise SignatureNotFound
    
    end_ds = content.find("</ds>")
    if end_ds == -1:
        raise SignatureCorrupted
    
    start_ds = start_tag + len("<ds>")
    signature = int(content[start_ds:end_ds])

    with open(input_file_name, "rb") as f:
        content = f.read(BUFFER_SIZE)

    hash = int.from_bytes(SHA3_256.new(content).digest())
    decrypted = private_key.encrypt(signature)
    if decrypted != hash:
        raise FileOrKeyModified
    return True


def verify_text_file(input_file_name: str, private_key: PublicKey):
    '''memeriksa keasilan file text dengan menguji digital signaturenya'''
    with open(input_file_name, "r") as f:
        content = f.read()
    
    start_tag = content.find("\n<ds>")
    if start_tag == -1:
        raise SignatureNotFound
    
    end_ds = content.find("</ds>")
    if end_ds == -1:
        raise SignatureCorrupted
    
    start_ds = start_tag + len("\n<ds>")
    end_tag = end_ds + len("</ds>")

    signature = int(content[start_ds:end_ds])
    real_content = content[:start_tag]
    hash = int.from_bytes(SHA3_256.new(real_content.encode()).digest())
    decrypted = private_key.encrypt(signature)
    if decrypted != hash:
        raise FileOrKeyModified
    return True

    