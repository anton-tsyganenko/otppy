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
import optparse

notenoughkeys = 5 # for warning (see KEY INPUT)



################ FUNCTIONS

def bxor(b1, b2): # use xor for bytes
    result = bytearray()
    for b1, b2 in zip(b1, b2):
        result.append(b1 ^ b2)
    return bytes(result)

def toHex(data): # convert binary data to hex code
    return bytes(space.join("{:02x}".format(x) for x in data), "utf-8")

def out(output):
    if outfile: # output to a file
        with open(nextarg("-o"), "bw") as outFile:
            outFile.write(output)
    else:
        print(output.decode("utf-8"))



################ OPTIONS

parser = optparse.OptionParser()

parser.add_option("-o", "--output-file",
                  dest = "outfile",
                  help = "write output to FILE",
                  metavar = "FILE")

parser.add_option("-i", "--input-file",
                  dest = "infile",
                  help = "write output to FILE",
                  metavar = "FILE")

parser.add_option("-k", "--keys-folder",
                  dest = "keyfolder",
                  help = "get a key from FOLDER",
                  metavar = "FOLDER")

parser.add_option("--key-action",
                  dest = "keyaction",
                  choices = ["leave", "delete", "rename"],
                  help = "action to do with used key, can be " +
                       "`leave`, `delete` or `rename`",
                  metavar = "ACTION")

parser.add_option("-I", "--input-mode",
                  dest = "imode",
                  default = "auto",
                  help = "input mode, can be `bin` or `hex`",
                  metavar = "MODE")

parser.add_option("-O", "--output-mode",
                  dest = "omode",
                  default = "auto",
                  help = "output mode, can be `bin` or `hex`",
                  metavar = "MODE")

parser.add_option("--gen-keys",
                  dest = "genkey",
                  default = False,
                  action = "store_true",
                  help = "generate keys")

parser.add_option("--no-spaces",
                  dest = "nospaces",
                  default = False,
                  action = "store_true",
                  help = "do not use spaces in hex code")

(options, args) = parser.parse_args()

infile = options.infile
outfile = options.outfile
keyfolder = options.keyfolder
keyaction = options.keyaction
imode = options.imode
omode = options.omode
genkey = options.genkey
if options.nospaces:
    space = ""
else:
    space = " "



################ KEY GENERATION

if genkey:
    number = int(input("number of keys > "))
    length = int(input("key length > "))

    if omode == "hex" or not outfile: # text with keys in hex format
        result = b""
        for i in range(number):
            result += toHex(os.urandom(length)) + b"\n"
        out(result)

    else: # folder with binary key files
        try:
            os.makedirs(outfile)
        except:
            pass
        for i in range(number):
            with open(outfile + os.sep + str(i), "xb") as f:
                f.write(os.urandom(length))

    exit()



################ TEXT INPUT

if infile: # from a file
    with open(infile, "rb") as file:
        text = file.read()
    if imode == "auto":
        imode = "bin"
    if omode == "auto":
        if outfile:
            omode = "bin"
        else:
            omode = "hex"

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

if keyfolder: # use folder with keys
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
        key = f.read(len(text))

else: # manually input the key
    key = bytes.fromhex(input("enter the key > "))



################ DON'T LET USER TO USE TOO SHORT KEY

if len(key) < len(text):
    print("the key must have the text's length or be longer")
    exit()



################ ENCRYPTION/DECRYPTION

result = bxor(text, key)



################ FINAL

if omode == "hex": # convert encrypted result to hex format
    result = toHex(result)

if not outfile and not (infile and keyfolder): # separator
    print("================\n")

out(result)

if keyfolder: # delete or rename used key
    if keyaction == "rename":
        os.rename(keyfile, keyfile + "_used")
    elif keyaction == "delete":
        os.remove(keyfile)
