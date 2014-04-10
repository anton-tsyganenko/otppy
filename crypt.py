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

if "--no-spaces" in sys.argv:
    space = ""
else:
    space = " "

if "--gen-key" in sys.argv:
    number = int(input("number of keys > "))
    len = int(input("key len > "))
    for i in range(number):
        print (space.join('{:02x}'.format(x) for x in os.urandom(len)))
    exit()

decryption = False

def sxor(str1, str2): # use xor for bytes
    return ''.join(chr(str1 ^ str2) for str1, str2 in zip(str1, str2))

def validate_key(key, text): # don't let user to use small key
    if len(key) < len(text):
        print("the key must have the text length or be longer")
        exit()
    return key

text = input("enter the text > ") # input text, decide, if it's a encrypted text and convert to bytes
try:
    text = bytes.fromhex(text.replace(" ", ""))
    decryption = True
except:
    text = bytes(text, "utf-8")

key = input("enter the key > ") # input key, check, if it's hex
try:
    key = bytes.fromhex(key.replace(" ", ""))
except:
    print ("the key must be in HEX format")
    exit()

result = str(sxor(text, validate_key(key, text))) # encrypt/decrypt the text

if not decryption: # encrypted result convert to hex format
    result = space.join("{:02x}".format(ord(c)) for c in result)

print (result)