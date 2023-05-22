import math
import random

first_primes_list = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
    31, 37, 41, 43, 47, 53, 59, 61, 67,
    71, 73, 79, 83, 89, 97, 101, 103,
    107, 109, 113, 127, 131, 137, 139,
    149, 151, 157, 163, 167, 173, 179,
    181, 191, 193, 197, 199, 211, 223,
    227, 229, 233, 239, 241, 251, 257,
    263, 269, 271, 277, 281, 283, 293,
    307, 311, 313, 317, 331, 337, 347, 349
]
'''prime awal yang akan ditest untuk pembagian'''


def get_shallow_tested_prime(n: int) -> int:
    '''tes kandidat prima dengan first_prime_list'''

    while True:
        prime_candidate = generate_large_n_size_number(n)
        for prime_divisor in first_primes_list:
            divisable = prime_candidate % prime_divisor == 0
            if divisable:
                break
        else:
            return prime_candidate


def miller_rabin_test(candidate: int) -> bool:
    '''Menguji prima dengan miller rabin test dengan 20 percobaan dengan kemungkinan non prima sekitar 4^-20'''
    maxDivisionsByTwo = 0
    even_component = candidate-1
    while even_component % 2 == 0:
        even_component >>= 1
        maxDivisionsByTwo += 1
    assert (2 ** maxDivisionsByTwo * even_component == candidate - 1)

    def trialComposite(round_tester):
        if pow(round_tester, even_component, candidate) == 1:
            return False
        for i in range(maxDivisionsByTwo):
            if pow(round_tester, 2 ** i * even_component, candidate) == candidate - 1:
                return False
        else:
            return True

    trials = 20
    for i in range(trials):
        round_tester = random.randrange(2, candidate)
        if trialComposite(round_tester):
            return False
    return True


def generate_large_n_size_number(n: int) -> int:
    '''menghasilkan random number dengan size n'''
    return random.getrandbits(n)


def generate_rsa_keys(p: int, q: int, length: int = 256) -> tuple[int, int, int]:
    '''menghasilkan key rsa (n, e, d) dari bilangan prima p dan q. d dan e besarnya length bit'''

    n = p * q
    totient_n = (p - 1) * (q - 1)
    e = generate_large_n_size_number(length)
    while e > totient_n or math.gcd(e, totient_n) != 1:
        e = generate_large_n_size_number(length)

    d = modular_multiplicative_inverse(e, totient_n)
    return (n, e, d)


g_x, g_y = 0, 1


def modified_gcd(a: int, b: int) -> int:
    '''menghitung gcd untuk angka yang relatif besar dengan rekursif'''
    global g_x, g_y

    if (a == 0):
        g_x = 0
        g_y = 1
        return b

    gcd = modified_gcd(b % a, a)
    x1 = g_x
    y1 = g_y

    g_x = y1 - (b // a) * x1
    g_y = x1
    return gcd


def modular_multiplicative_inverse(A: int, M: int) -> int:
    '''Menyelesaikan permasalahan Ax kongruen 1 (mod M) dengan A dan M coprime'''
    g = modified_gcd(A, M)
    if (g != 1):
        return None

    else:
        result = (g_x % M + M) % M
        return result


def generate_large_prime(n: int) -> int:
    '''Membangkitkan bilangan prima besar sebanyak n bit'''
    while True:
        prime_candidate = get_shallow_tested_prime(n)
        if not miller_rabin_test(prime_candidate):
            continue
        else:
            return prime_candidate


class PrivateKey:
    def __init__(self, n, d):
        self.key = (n, d)
        self.n = n
        self.d = d

    def encrypt(self, message):
        (n, d) = self.key
        return pow(message, d, n)

    @staticmethod
    def read_from_file(file_name: str):
        try:
            with open(file_name, "r") as f:
                keys = f.read()

                (n, d) = keys.split(",")
                return PrivateKey(int(n), int(d))
        except:
            pass

    def save_to_file(self, file_name: str):
        try:
            with open(file_name, "w") as f:
                f.write(str(self.n) + "," + str(self.d))
        except Exception as e:
            raise e


class PublicKey:
    def __init__(self, n, e):
        self.key = (n, e)
        self.n = n
        self.e = e

    def decrypt(self, message):
        (n, e) = self.key
        return pow(message, e, n)

    @staticmethod
    def read_from_file(file_name):
        try:
            with open(file_name, "r") as f:
                keys = f.read()

                (n, e) = keys.split(",")
                return PublicKey(int(n), int(e))
        except:
            pass

    def save_to_file(self, file_name: str):
        try:
            with open(file_name, "w") as f:
                f.write(str(self.n) + "," + str(self.e))
        except Exception as e:
            raise e


def generate_rsa() -> tuple[PrivateKey, PublicKey]:
    '''Membangkitkan objek PrivateKey dan PublicKey'''
    p = generate_large_prime(135)
    q = generate_large_prime(135)
    keys = generate_rsa_keys(p, q, 270)
    (n, e, d) = keys
    return (
        PrivateKey(n, d),
        PublicKey(n, e)
    )
