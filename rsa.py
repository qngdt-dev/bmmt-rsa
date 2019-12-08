import math
import binascii


def is_prime(n):
    if n == 2:
        return True
    if n % 2 == 0 or n <= 1:
        return False

    sqr = int(math.sqrt(n)) + 1

    for divisor in range(3, sqr, 2):
        if n % divisor == 0:
            return False
    return True


def factors(number):
    i = 2
    factors = []
    while i <= number:
        if (number % i) == 0:
            number = number / i
            factors.append(str(i))
        else:
            i = i + 1
    return factors


def split_str(seq, chunk, skip_tail=False):
    lst = []
    if chunk <= len(seq):
        lst.extend([seq[:chunk]])
        lst.extend(split_str(seq[chunk:], chunk, skip_tail))
    elif not skip_tail and seq:
        lst.extend([seq])
    return lst


def padhexa(s):
    return '0x' + s[2:].zfill(8)


def modInverse(a, m):
    m0 = m
    y = 0
    x = 1

    if (m == 1):
        return 0

    while (a > 1):
        # q is quotient
        # print('m:', m)
        q = a // m
        # print('q:', q)
        t = m
        # m is remainder now, process same as Euclid's algo
        m = a % m
        a = t
        t = y
        # Update x and y
        y = x - q * y
        x = t
        # print(x, y, a)

    # Make x positive
    if (x < 0):
        x = x + m0

    return x


class RSA:
    def __init__(self, p, q):
        self.p = p
        self.q = q
        self.n = p*q
        self.r = (p-1)*(q-1)
        self.range = 0

    def generate_ed(self):
        k_list = []
        for i in range(1, 10):
            K = i*self.r + 1
            factor_str = 'x'.join(factors(K))
            # print(factor_str)
            # factor_str = factor_str.replace(',', 'x')
            # print(factor_str)
            tmp_str = f'{K} = {factor_str}'
            k_list.append(tmp_str)
        return k_list

    def check_valid_key(self, e, d):
        if(math.gcd(e, self.r) != 1):
            return False
        if(math.gcd(d, self.r) != 1):
            return False
        if(e*d % self.r != 1):
            return False
        return True

    def encode_message(self, message):
        max_range = 0
        hex_data = binascii.hexlify(message[0].encode())
        plain_text_part = int(hex_data, 16)
        while(plain_text_part < self.n):
            max_range += 2
            hex_data = binascii.hexlify(message[0:max_range].encode())
            plain_text_part = int(hex_data, 16)
            if(plain_text_part - self.n > 0):
                max_range -= 2
                break
        encoded_message = []
        for str_part in split_str(message, max_range):
            hex_data = binascii.hexlify(str_part.encode())
            encoded_message.append(int(hex_data, 16))
        return encoded_message

    def encrypt_message(self, encoded_message, e):
        encrypted_message = []
        for (index, msg_part) in enumerate(encoded_message):
            encrypted_message.append(pow(encoded_message[index], e, self.n))
        return encrypted_message

    def decrypt_message(self, encrypted_message, d):
        decrypted_result = []
        for encrypted_part in encrypted_message:
            decrypted_hex = pow(encrypted_part, d, self.n)
            decrypted_result.append(binascii.unhexlify(
                hex(decrypted_hex)[2:]).decode())
        return ''.join(decrypted_result)


class RSA_Cracker:
    def __init__(self, e, n):
        self.e = e
        self.n = n
        self.p = 0
        self.q = 0
        self.phin = 0
        self.d = 0

    def find_pq(self):
        start_point = int(math.sqrt(self.n))
        print(start_point)
        while(True):
            # print(self.n % start_point)
            if(self.n % start_point == 0):
                self.p = start_point
                self.q = int(self.n / start_point)
                self.phin = (self.p-1)*(self.q-1)
                return (self.p, self.q, self.phin)
            else:
                start_point -= 2


# rsa_ins = RSA(239, 8219)
# print('n:', rsa_ins.n)
# print('r', rsa_ins.r)
# e = 5
# d = 391177
# n = rsa_ins.n

# message = 'We can remove the second term on left side as my mod m would always be 0 for an integer y.'
# print('Message:', message)
# print(rsa_ins.check_valid_key(e, d))
# encoded_message = rsa_ins.encode_message(message)
# encrypted_message = rsa_ins.encrypt_message(encoded_message, e)
# # print('Encrypted message:', encrypted_message)
# print('Decrypted message:', rsa_ins.decrypt_message(encrypted_message, d))

# rsa_cracker_ins = RSA_Cracker(e, n)
# p, q, phin = (rsa_cracker_ins.find_pq())
# print(p, q, phin)
# d = modInverse(rsa_cracker_ins.e, rsa_cracker_ins.phin)
# print(d)
