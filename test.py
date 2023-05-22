from Crypto.PublicKey import RSA


def generate_keys():
    files = [
        "gilimanuk",
        "labuan_bajo",
        "rinca",
        "waingapu"
    ]
    for i in files:
        key = RSA.generate(1024)
        private_key = key.export_key()
        file_out = open("ports/keys/" + i + "/private.pem", "wb")
        file_out.write(private_key)
        file_out.close()

        public_key = key.publickey().export_key()
        file_out = open("ports/keys/" + i + "/public.pem", "wb")
        file_out.write(public_key)
        file_out.close()


generate_keys()
