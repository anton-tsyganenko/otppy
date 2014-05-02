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
import hashlib
import base64

notenoughkeys = 5 # for warning (see KEY INPUT)



################ FUNCTIONS

def bxor(b1, b2): # use xor for bytes
    result = bytearray()
    for b1, b2 in zip(b1, b2):
        result.append(b1 ^ b2)
    return bytes(result)

def out(output):
    if outfile: # output to a file
        with open(outfile, "bw") as file:
            file.write(output)
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
                  dest = "keysource",
                  help = "get a key from FOLDER",
                  metavar = "FOLDER")

parser.add_option("-K", "--key-action",
                  dest = "keyaction",
                  choices = ["leave", "delete", "rename"],
                  default = "rename",
                  help = "action to do with used key, can be " +
                       "`leave`, `delete` or `rename`",
                  metavar = "ACTION")

parser.add_option("-I", "--input-mode",
                  dest = "imode",
                  default = "auto",
                  help = "input mode, can be `bin` or `b64`",
                  choices = ["bin", "b64", "auto"],
                  metavar = "MODE")

parser.add_option("-O", "--output-mode",
                  dest = "omode",
                  default = "auto",
                  choices = ["bin", "b64", "auto"],
                  help = "output mode, can be `bin` or `b64`",
                  metavar = "MODE")

parser.add_option("-g", "--gen-keys",
                  dest = "genkey",
                  default = False,
                  action = "store_true",
                  help = "generate keys")

parser.add_option("-c", "--hash",
                  dest = "hashaction",
                  choices = ["check", "add", "no", "auto"],
                  default = "auto",
                  action = "store",
                  metavar = "ACTION",
                  help = "`check` or `add` a hash sum")


(options, args) = parser.parse_args()

infile = options.infile
outfile = options.outfile
keysource = options.keysource
keyaction = options.keyaction
imode = options.imode
omode = options.omode
genkey = options.genkey
hashaction = options.hashaction

if hashaction != "no":
    hashlen = 20
else:
    hashlen = 0



################ KEY GENERATION

if genkey:
    number = int(input("number of keys > "))
    length = int(input("key length > "))

    if omode == "b64" or not outfile: # text with keys in base64
        result = b""
        for i in range(number):
            result += base64.b64encode(os.urandom(length)) + b"\n"
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

else: # direct input
    text = bytes(input("enter the text > "), "utf-8")



################ SETTINGS GUESSING

if infile:
    if imode == "auto":
        imode = "bin"


if imode in ["auto", "b64"]:
    try: # try to decode base64
        text = base64.b64decode(text.decode("utf-8"))
        if omode == "auto": # if user inputs base64 data,
            omode = "bin"   # probably he wants to get a text
    except:           # if user inputs not base64 data,
        if not outfile:
            omode = "b64" # probably he wants to get base64 code


if hashaction == "auto":
    if omode == "b64" or (outfile and not infile):
        hashaction = "add"
    else:
        hashaction = "check"

# there are some other settings guessing code in FINAL.


################ KEY INPUT

if keysource: # use folder with keys
    if os.path.isdir(keysource):
        fileslist = os.listdir(keysource)

        newfl = fileslist.copy() # newlf is just for not modifying list,
                                 # using in a loop
        for i in fileslist: # don't use used keys
            if "_used" in i:
                newfl.remove(i)

        fileslist = newfl
        del newfl

        if len(fileslist) == 0:
            print("================\n" +
                  "NO KEYS IN {kf}!".format(kf=keysource))
            exit()

        if len(fileslist) <= notenoughkeys:
            print("================")
            print(("WARNING! only {k} keys left, and one of them " +
                  "will be used now.").format(k=len(fileslist)))

        keyfile = keysource + os.sep + max(fileslist, key=int)
        with open(keyfile, "br") as f:
            key = f.read(len(text)+hashlen)
    else:
        with open(keysource, "br") as f:
            key = f.read(len(text)+hashlen)

else: # manually input the key
    key = base64.b64decode(input("enter the key > "))



################ ADD A HASH SUM

if hashaction != "no":
    texthash = hashlib.sha1(text).digest()
    text += texthash



################ DON'T LET USER TO USE TOO SHORT KEY

if len(key) < (len(text)):
    print("the key must have the text's length or be longer")
    exit()



################ ENCRYPTION/DECRYPTION

result = bxor(text, key)



################ CHECK A HASH SUM

# the hash sum of the text, excluding the last 20 bytes
# takes last 20 bytes of text.

if hashaction != "no":
    resulthash = hashlib.sha1(result[0:-40]).digest()

    if resulthash == result[-40:-20]:
        print("================\nThe hash sum is ok")
        result = result[0:-40]
    else:
        print("================")
        print("The hash sum was added/wrong")



################ FINAL

if omode == "auto": # settings guessing
    try:
        result.decode("utf-8")
        omode = "bin"
    except:
        if not outfile:
            omode = "b64"
        else:
            omode = "bin"


if omode == "b64": # convert encrypted result to base64
    result = base64.b64encode(result)

if not outfile and not (infile and keysource and hashaction == "no"):
    print("================\n") # separator

out(result)

if keysource: # delete or rename used key
    if keyaction == "rename":
        os.rename(keyfile, keyfile + "_used")
    elif keyaction == "delete":
        os.remove(keyfile)
