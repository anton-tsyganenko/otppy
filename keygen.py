#!/usr/bin/env python3

# Copyright (c) 2014 Anton Tsyganenko
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

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
