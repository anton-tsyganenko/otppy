#!/usr/bin/python3

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



################ OPTIONS

fileout = False
filein = False
keyfile = False
binmode = False
genkey = False

if "-o" in sys.argv:
    fileout = True

if "-i" in sys.argv:
    filein = True

if "-ki" in sys.argv:
    keyfile = True

if "--bin" in sys.argv:
    binmode = True

if "--gen-key" in sys.argv:
    genkey = True

if "--no-spaces" in sys.argv:
    space = ""
else:
    space = " "

decryption = False



################ FUNCTIONS

def bytesToString(bytes):
    return "".join(chr(x) for x in bytes)

def nextarg(arg): # just for better readability
    return sys.argv[sys.argv.index(arg) + 1]

def bxor(b1, b2): # use xor for bytes
    result = b""
    for b1, b2 in zip(b1, b2):
        result += bytes([b1 ^ b2])
    return result

def validate_key(key, text): # don't let user to use short key
    if len(key) < len(text):
        print("the key must have the text length or be longer")
        exit()
    return key

def binOut(data):
    if not binmode:
        result = b""
        result += bytes(space.join('{:02x}'.format(x) for x in data), "utf-8")
        return result
    else:
        return data

def out(output):
    if fileout: # output to a file
        with open(nextarg("-o"), "bw") as outFile:
            outFile.write(output)
    else:
        print(bytesToString(output))



################ KEY GENERATION

if genkey: # function for keys generation
    number = int(input("number of keys > "))
    len = int(input("key length > "))
    result = b""
    for i in range(number):
        result += binOut(os.urandom(len))
        result += b"\n"
    out(result)
    exit()



################ TEXT INPUT

if filein:
    with open(nextarg("-i"), "rb") as file:
        text = file.read()
else:
    text = bytes(input("enter the text > "), "utf-8")

try:
    text = bytes.fromhex(text.replace(b" ", b"").decode("utf-8"))
    decryption = True
except:
    pass



################ KEY INPUT

if keyfile:
    with open(nextarg("-ki"), "rb") as file:
        key = file.read()
else:
    key = bytes.fromhex(input("enter the key > ").replace(" ", ""))



################ ENCRYPTION/DECRYPTION

result = bxor(text, validate_key(key, text))



################ FINAL

if not decryption: # encrypted result convert to hex format
    result = binOut(result)

out(result)