#!/usr/bin/env python3

# Copyright © 2014 Anton Tsyganenko
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


def randombytes(length):
    result = bytes(length)
    with open("mixed", "rb") as mixed:
        for i in range(os.stat("mixed").st_size//length):
            result = bxor(result, mixed.read(length))
    result = bxor(os.urandom(length), result)
    return result

def mixfiles():
    maxlen = max(os.stat(f).st_size for f in fileslist)
    with open("mixed", "wb") as mixed:
        for i in range(maxlen//256):
            for file in files:
                mixed.write(file.read(256))
    
    for file in fileslist:
        os.remove(file)
        
        

os.chdir(sys.argv[1])
fileslist = os.listdir()
files = []
for file in fileslist:
    files.append(open(file, "rb"))

keys_number = int(sys.argv[2])
key_length = int(sys.argv[3])

mixfiles()
randomdata = randombytes(key_length * keys_number)
os.remove("mixed")

keys = []
for i in range(keys_number):
    keys.append(randomdata[0:key_length])
    randomdata = randomdata[key_length:]


if "t" not in sys.argv:
    i = 0
    for key in keys:
        with open(str(i), "bw") as f:
            f.write(key)
        i += 1
else:
    for key in keys:
        print(base64.b64encode(key).decode())
