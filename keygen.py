#!/usr/bin/env python3

import os
import sys
import base64

def bxor(b1, b2):            # use xor for bytes
    result = bytearray()
    for b1, b2 in zip(b1, b2):
        result.append(b1 ^ b2)
    return bytes(result)

def randombytes(length, files):
    entropy = b""
    for file_name in files:
        with open(path + file_name, "rb") as f:
            entropy += f.read()

    result = bytes(length)
    while len(entropy) > length:
        result = bxor(entropy[0:length], result)
        entropy = entropy[length:]
    entropy += bytes(length - len(entropy))
    result = bxor(entropy, result)
    del entropy
    result = bxor(os.urandom(length), result)
    return result

files = os.listdir(sys.argv[1])
path = sys.argv[1] + os.sep 
key_length = int(sys.argv[2])
keys_number = int(sys.argv[3])

randomdata = randombytes(key_length * keys_number, files)

if "t" not in sys.argv:
    for f in files:
        os.remove(path + f)

    for i in range(keys_number):
        with open(path + str(i), "bw") as f:
            f.write(randomdata[0:key_length])
        randomdata = randomdata[key_length:]
else:
    for i in range(keys_number):
        print(base64.b64encode(randomdata[0:key_length]).decode())
        randomdata = randomdata[key_length:]
