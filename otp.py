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
    result = bytearray()
    for b1, b2 in zip(b1, b2):
        result.append(b1 ^ b2)
    return bytes(result)

def toHex(data): # convert binary data to hex code
    return bytes(space.join("{:02x}".format(x) for x in data), "utf-8")

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
keyaction = "rename"    # action for used key (rename, delete, leave)
notenoughkeys = 5       # for warning (see KEY INPUT)

if "-o" in sys.argv:
    fileout = True

if "-i" in sys.argv:
    filein = True

if "-ki" in sys.argv:
    keyfromfile = True

if "--key-action" in sys.argv:
    keyaction = nextarg("--key-action")

if "--imode" in sys.argv:
    imode = nextarg("--imode")

if "--omode" in sys.argv:
    omode = nextarg("--omode")

if "--gen-key" in sys.argv:
    genkey = True

if "--no-spaces" in sys.argv:
    space = ""
else:
    space = " "



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
    if imode == "auto":
        imode = "bin"
    if omode == "auto" and fileout:
        omode = "bin"

else: # direct input
    text = bytes(input("enter the text > "), "utf-8")

if imode in ["auto", "hex"]:
    try: # try to decode hex
        text = bytes.fromhex(text.decode("utf-8"))
        if omode == "auto": # if user inputs hex code,
            omode = "bin"   # probably he wants to get a text
    except:           # if user inputs not hex code,
        omode = "hex" # probably he wants to get a hex code



################ KEY INPUT

if keyfromfile: # use folder with keys
    keyfolder = nextarg("-ki")
    fileslist = os.listdir(keyfolder)

    newfl = fileslist.copy() # newlf is just for not modifying list,
                             # using in a loop
    for i in fileslist: # don't use used keys
        if "_used" in i:
            newfl.remove(i)

    fileslist = newfl
    del newfl

    if len(fileslist) == 0:
        print("================\n" +
              "NO KEYS IN {kf}!".format(kf=keyfolder))
        exit()

    if len(fileslist) <= notenoughkeys:
        print("================\n" +
            "WARNING! only {k} keys left, ".format(k=len(fileslist)) +
            "and one of them will be used now.")

    keyfile = keyfolder + os.sep + max(fileslist)
    with open(keyfile, "br") as f:
        key = f.read()

else: # manually input the key
    key = bytes.fromhex(input("enter the key > "))



################ DON'T LET USER TO USE TOO SHORT KEY

if len(key) < len(text):
    print("the key must have the text's length or be longer")
    exit()



################ ENCRYPTION/DECRYPTION

result = bxor(text, key)



################ FINAL

if omode == "hex": # encrypted result convert to hex format
    result = toHex(result)

if not fileout and not (filein and keyfromfile): # separator
    print("================\n")

out(result)

if keyfromfile: # delete or rename used key
    if keyaction == "rename":
        os.rename(keyfile, keyfile + "_used")
    elif keyaction == "delete":
        os.remove(keyfile)
