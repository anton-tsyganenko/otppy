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
    if omode != "bin":
        return bytes(space.join('{:02x}'.format(x) for x in data), "utf-8")
    else:
        return data

def out(output):
    if fileout: # output to a file
        with open(nextarg("-o"), "bw") as outFile:
            outFile.write(output)
    else:
        print(bytesToString(output))




################ OPTIONS

fileout = False
filein = False
keyfromfile = False
imode = "auto"
omode = "hex"
genkey = False
deletekey = True

if "-o" in sys.argv:
    fileout = True

if "-i" in sys.argv:
    filein = True

if "-ki" in sys.argv:
    keyfromfile = True

if "--imode" in sys.argv:
    imode = nextarg("--imode")

if "--omode" in sys.argv:
    omode = nextarg("--omode")

if "--gen-key" in sys.argv:
    genkey = True

if "--do-not-delete-key" in sys.argv:
    deletekey = False

if "--no-spaces" in sys.argv:
    space = ""
else:
    space = " "

decryption = False



################ KEY GENERATION

if genkey:
    number = int(input("number of keys > "))
    length = int(input("key length > "))
    if omode != "bin": # text with keys in hex format
        result = b""
        for i in range(number):
            result += binOut(os.urandom(length)) + b"\n"
        out(result)
    else: # folder with binary key files
        keyfolder = nextarg("-o")
        try:
            os.mkdir(keyfolder)
        except:
            pass
        for i in range(number):
            with open(keyfolder + os.sep + str(i), 'xb') as f:
                f.write(os.urandom(length))

    exit()



################ TEXT INPUT

if filein: # from a file
    with open(nextarg("-i"), "rb") as file:
        text = file.read()
else: # direct input
    print("enter the text, then press ENTER; CTRL+D")
    text = sys.stdin.read()[:-1]
    text = bytes(text, "utf-8")

if imode in ["auto", "hex"]:
    try: # try to decode hex
        text = bytes.fromhex(text.replace(b" ", b"").decode("utf-8"))
    except:
        omode = "bin"



################ KEY INPUT

if keyfromfile: # use folder with keys
    keyfolder = nextarg("-ki")
    keyfile = keyfolder + os.sep + max(os.listdir(keyfolder))
    with open(keyfile, 'br') as f:
        key = f.read()
    if deletekey:
        os.remove(keyfile)

else: # manually input the key
    key = bytes.fromhex(input("enter the key > ").replace(" ", ""))



################ ENCRYPTION/DECRYPTION

result = bxor(text, validate_key(key, text))



################ FINAL

if omode == "hex": # encrypted result convert to hex format
    result = binOut(result)

if not fileout and not (filein and keyfromfile): # separator
    print("################\n")

out(result)
