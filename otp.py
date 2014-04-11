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

def bytesToString(bytes):
    return "".join(chr(x) for x in bytes)

def binOut(value):
    result = ''
    if "--bin" not in sys.argv:
        if type(value) == bytes:
            result += space.join('{:02x}'.format(x) for x in value)
        if type(value) == str:
            result += space.join('{:02x}'.format(ord(x)) for x in value)
        return result
    else:
        return value

def nextarg(arg): # just for better readability
    return sys.argv[sys.argv.index(arg) + 1]

if "-o" in sys.argv: # output to a file
    def out(output):
        outFile = open(nextarg("-o"), "w")
        print ("output redirected to " + nextarg("-o"))
        outFile.write(output)
        outFile.close()
else:
    def out(output): print(output)

if "--no-spaces" in sys.argv: # remove spaces from encrypted data and generated keys if user doesn't need them.
    space = ""
else:
    space = " "

if "--gen-key" in sys.argv: # function for keys generation
    number = int(input("number of keys > "))
    len = int(input("key len > "))
    result = ""
    for i in range(number):
        result += binOut(bytesToString(os.urandom(len)))
        result += "\n"
    out(result)
    exit()

decryption = False

def sxor(str1, str2): # use xor for bytes
    return ''.join(chr(str1 ^ str2) for str1, str2 in zip(str1, str2))

def validate_key(key, text): # don't let user to use small key
    if len(key) < len(text):
        print("the key must have the text length or be longer")
        print(type(key), len(key), type(text), len(text))
        exit()
    return key

if "-i" not in sys.argv:
    text = input("enter the text > ") # input text, decide, if it's a encrypted text and convert to bytes
else:
    text = open(nextarg("-i"), "rb").read()

if "-i" in sys.argv:
    try:
        text = bytes.fromhex(text.replace(" ", ""))
    except:
        text = bytes.fromhex(bytesToString(text))
    decryption = True
elif "--force-encrypt" not in sys.argv:
    try:
        text = bytes.fromhex(text.replace(" ", ""))
        decryption = True
    except:
        if "-i" not in sys.argv: text = bytes(text, "utf-8")
else:
    text = bytes(text, "utf-8")

key = input("enter the key > ") # input key, check, if it's hex
try:
    key = bytes.fromhex(key.replace(" ", ""))
except:
    print ("the key must be in HEX format")
    exit()

result = str(sxor(text, validate_key(key, text))) # encrypt/decrypt the text

if not decryption: # encrypted result convert to hex format
    result = binOut(result)

out(result)