from Crypto.PublicKey import RSA
from rsa import generate_rsa


def generate_keys():
    files = [
        "main",
        "gilimanuk",
        "labuan_bajo",
        "rinca",
        "waingapu"
    ]
    for i in files:
        private_key, public_key = generate_rsa()
        # save key
        private_key.save_to_file('keys/' + i + '/private.txt')
        public_key.save_to_file('keys/' + i + '/public.txt')


generate_keys()
