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


################ FUNCTIONS

def nextarg(arg): # just for better readability
    return sys.argv[sys.argv.index(arg) + 1]

def bxor(b1, b2): # use xor for bytes
    result = b""
    for b1, b2 in zip(b1, b2):
        result += bytes([b1 ^ b2])
    return result

def validate_key(key, text): # check, if the key is too short
    return len(key) >= len(text)

def toHex(data): # convert binary data to hex code
    return bytes(space.join('{:02x}'.format(x) for x in data), "utf-8")

def out(output):
    if fileout: # output to a file
        with open(nextarg("-o"), "bw") as outFile:
            outFile.write(output)
    else:
        print(output.decode("utf-8"))




################ OPTIONS

fileout = False         # output to a file
filein = False          # get data from a file
keyfromfile = False     # use key from a folder
imode = "auto"          # input mode
omode = "auto"          # output mode
genkey = False          # generate keys
deletekey = True        # detele used key
notenoughkeys = 5       # for warning (see line 156)

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

    if omode == "hex" or not fileout: # text with keys in hex format
        result = b""
        for i in range(number):
            result += toHex(os.urandom(length)) + b"\n"
        out(result)

    else: # folder with binary key files
        keyfolder = nextarg("-o")
        try:
            os.mkdir(keyfolder)
        except:
            pass
        for i in range(number):
            with open(keyfolder + os.sep + str(i), "xb") as f:
                f.write(os.urandom(length))

    exit()



################ TEXT INPUT

if filein: # from a file
    with open(nextarg("-i"), "rb") as file:
        text = file.read()
    if omode == "auto":
        omode = "bin"
    if imode == "auto": # not a mistake, look at first letters
        imode = "bin"

else: # direct input
    text = input("enter the text > ")
    text = bytes(text, "utf-8")

if imode in ["auto", "hex"]:
    try: # try to decode hex
        text = bytes.fromhex(text.replace(b" ", b"").decode("utf-8"))
        if omode == "auto": # if user inputs hex code,
            omode = "bin"   # probably he wants to get a text
    except:           # if user inputs not hex code,
        omode = "hex" # probably he wants to get a hex code



################ KEY INPUT

if keyfromfile: # use folder with keys
    keyfolder = nextarg("-ki")
    fileslist = os.listdir(keyfolder)

    if len(fileslist) == 0:
        print("================\n" +
              "NO KEYS IN {kf}!".format(kf=keyfolder))
        exit()

    if len(fileslist) <= notenoughkeys:
        print("================\n" +
            "WARNING! only {k} keys left, ".format(k=len(fileslist)) +
            "and one of them will be used now.")

    keyfile = keyfolder + os.sep + max(fileslist)
    with open(keyfile, 'br') as f:
        key = f.read()

else: # manually input the key
    key = bytes.fromhex(input("enter the key > ").replace(" ", ""))


################ DON'T LET USER TO USE TOO SHORT KEY

if not validate_key(key, text):
    print("the key must have the text length or be longer")
    exit()

################ ENCRYPTION/DECRYPTION

result = bxor(text, key)



################ FINAL

if omode in ["hex", "auto"]: # encrypted result convert to hex format
    result = toHex(result)

if not fileout and not (filein and keyfromfile): # separator
    print("================\n")

out(result)

if deletekey and keyfromfile: # delete the key if evrything is ok
    os.remove(keyfile)
