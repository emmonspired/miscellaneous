#
# Dan Clark
# https://github.com/dandclark
#
# Udacity Applied Cryptography
# HW4-05 Version 1
#
# Use RSA and OAEP padding to decrypt the ciphertext below
# Put your answer in the plaintext variable
#

from hashlib import sha512
from unit4_util import bits_to_int, string_to_bits, bits_to_string, convert_to_bits, pad_bits

# private key
#n = 163337384206254196136256905164215818685586918951141221126394408668809777452520349668859723974634222518738526976760766017511678181884780117277802125689306872778510779111021304067611411071215920387754683047176920988231245806047339117003013267749350166593203943400463471064009273107286997981419079779353871913613

#d = 72306394717363424299328399722663981135942256932885379363091911199772788859003622146161074079559455936549462817183931881228142994229843306261555995399517375703257594404049732148740472823878934537674252191478702048647471522520082576645795404386769847966042578016616602577622451300338631726401289028172301100673

# public key
#e = 65537

# variables used in padding
#g = 512
#h = 512

def hash(input_, length):
    input_string = bits_to_string(input_).encode(encoding='latin-1')
    h = sha512(input_string).digest()
    return string_to_bits(h)[:length]

def xor(a, b):
    assert len(a) == len(b)
    return [aa^bb for aa, bb in zip(a, b)]

def oaep_pad(message, nonce, g, h):
    mm = message + [0] * (g - len(message))
    G = xor(mm, hash(nonce, g))
    H = xor(nonce, hash(G, h))
    return G + H
    
def encrypt(message, n, public_key, nonce, g, h):
    oaep = oaep_pad(message, nonce, g, h)
    m_int = bits_to_int(oaep)
    return convert_to_bits(pow(m_int, public_key, n))

##################
# ciphertext was created by calling
# `encrypt` where message and nonce are secret

ciphertext = string_to_bits("\x98WRQ5\xf4\xe5L$a\xf4\xbf\xecV\\\xb1\xe4\x18\xf1It\x01\xca\xdc\xd0@\xc8\xf6\x97\xf9K\xb8\x1b\x9a\x17\x89\xa9\xcap\x9a\xb5\xb4\x12\xf6\x01\x9avd\xedc*\xcbELRi\xf7.?\x82H\xd3Ci\xd7\xaea7\xbc\x00+\xf04\x13>\xe6q\xf3\xedg\xc4VWB\x8a\x9f\xdf%-8\xf3\x08\xc59\x84\xec\xf8G\xbe\xd2Ub\xf9K4\xa0\xa4(\xeaI\x19T\x1fM\xa6+\x81\xb0\x8d\x04\x99<%o3C-\xc6")

plaintext = "Where is the ANY key? -Homer Simpson" # YOUR ANSWER HERE

def decrypt(ciphertext, n, private_key, g, h):
    """
    Decrypts the specified ciphertext.
    Assumes that ciphertext was obtained by applying OAEP padding to a message
    (using parameters g and h), and then RSA-encrypted with parameter n and public
    key corresponding to the specified private_key.
    """
    ciphertext_int = bits_to_int(ciphertext)
    plaintext_int = pow(ciphertext_int, private_key, n)
    return decode_oaep(plaintext_int + n, g, h)
    
def decode_oaep(oaep_padded_int, g, h):
    """
    Given the specified OAEP-padded plaintext as an integer (with OAEP using parameters
    g and h), returns the corresponding plaintext bits with the padding removed.
    """
    plaintext_bits = pad_bits(convert_to_bits(oaep_padded_int), g + h)
    
    first_chunk = plaintext_bits[0:g]
    second_chunk = plaintext_bits[g:g + h]

    assert len(plaintext_bits) == g + h
    assert len(first_chunk) == g
    assert len(second_chunk) == h

    first_chunk_H = hash(first_chunk, h)
    r = xor(first_chunk_H, second_chunk)
    G_r = hash(r, g)
    m_prime = xor(first_chunk, G_r)
    return m_prime    
    
if __name__ == "__main__":
    print("Decrypting...")
    plaintext_bits = decrypt(ciphertext, n, d, g, h)
    plaintext = bits_to_string(plaintext_bits).strip('\x00')
    print("Message:", plaintext)