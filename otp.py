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
        with open(outfile, "bw") as ofile:
            ofile.write(output)
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
                  help = "get data from FILE",
                  metavar = "FILE")

parser.add_option("-k", "--keys-folder",
                  dest = "keysource",
                  help = "get a key from FOLDER",
                  metavar = "FOLDER")

parser.add_option("-K", "--key-action",
                  dest = "keyaction",
                  choices = ["leave", "delete", "rename"],
                  default = "rename",
                  help = ("action to do with used key, can be "
                          "`leave`, `delete` or `rename`"),
                  metavar = "ACTION")

parser.add_option("-I", "--input-mode",
                  dest = "imode",
                  default = "auto",
                  help = "input mode, can be `bin`, `b64` or `auto`",
                  choices = ["bin", "b64", "auto"],
                  metavar = "MODE")

parser.add_option("-O", "--output-mode",
                  dest = "omode",
                  default = "auto",
                  choices = ["bin", "b64", "auto"],
                  help = "output mode, can be `bin`, `b64` or `auto`",
                  metavar = "MODE")

parser.add_option("-g", "--gen-keys",
                  dest = "genkey",
                  default = False,
                  action = "store_true",
                  help = "generate keys")

parser.add_option("-c", "--hash-action",
                  dest = "hashaction",
                  choices = ["no", "auto", "add", "check"],
                  default = "auto",
                  metavar = "ACTION",
                  help = "action to do with hash sum")


(options, args) = parser.parse_args()

infile = options.infile
outfile = options.outfile
keysource = options.keysource
keyaction = options.keyaction
imode = options.imode
omode = options.omode
genkey = options.genkey
hashaction = options.hashaction

if hashaction in ["auto", "add"]:
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
        os.makedirs(outfile, exist_ok=True)
        for i in range(number):
            with open(outfile + os.sep + str(i), "xb") as f:
                f.write(os.urandom(length))

    exit()



################ TEXT INPUT

if infile: # from a file
    with open(infile, "rb") as tfile:
        text = tfile.read()

else: # direct input
    text = bytes(input("enter the text > "), "utf-8")



################ SETTINGS GUESSING

if infile:
    if imode == "auto":
        imode = "bin"


if imode in ["auto", "b64"]:
    try: # try to decode base64
        text = base64.b64decode(text.decode("utf-8"), validate=True)
    except:
        if imode == "b64":
            print("Cannot decode base64!")
            exit()


# there are some other settings guessing code in FINAL.



################ KEY INPUT

if keysource: # use folder with keys or a keyfile
    if os.path.isdir(keysource): # folder with keys
        fileslist = os.listdir(keysource)

        for i in fileslist[:]: # don't use used keys
            if i.endswith("_used"):
                fileslist.remove(i)

        if len(fileslist) == 0:
            print("================\n"
                  "NO KEYS IN {ks}!".format(ks=keysource))
            exit()

        if len(fileslist) <= notenoughkeys:
            print("================\n"
                  "WARNING! only {k} keys left, and one of them "
                  "will be used now.".format(k=len(fileslist)))

        keyfile = keysource + os.sep + max(fileslist, key=int)
        with open(keyfile, "br") as f:
            key = f.read(len(text)+hashlen)

        keyfromfolder = True # see FINAL

        del fileslist
    else: # a keyfile
        with open(keysource, "br") as f:
            key = f.read(len(text)+hashlen)
        keyfromfolder = False

    del keysource, hashlen

else: # manually input the key
    key = base64.b64decode(input("enter the key > "))
    keyfromfolder = False



################ ADD A HASH SUM

if hashaction in ["add", "auto"]:
    text += hashlib.sha1(text).digest()



################ DON'T LET USER TO USE TOO SHORT KEY

if len(key) < (len(text)):
    print("The key must have the text's length or be longer")
    if hashaction == "auto" and len(key) >= (len(text)-20):
        print("If you're decrypting data, try to use `-c check` option")
    exit()



################ ENCRYPTION/DECRYPTION

result = bxor(text, key)
del text, key



################ CHECK A HASH SUM

if hashaction != "no":
    if hashaction == "check":
        hashplace = memoryview(result)[-20:]
        resultbody = memoryview(result)[0:-20]
    elif hashaction == "auto":
        # in auto mode the program adds new hash sum(see ADD A HASH SUM)
        hashplace = memoryview(result)[-40:-20]
        resultbody = memoryview(result)[0:-40]

    if hashaction != "add":
        resulthash = hashlib.sha1(resultbody).digest()

    print("================")

    if hashaction != "add" and resulthash == hashplace:
        print("The hash sum is ok")
        result = bytes(resultbody)

    elif hashaction == "check":
        print("The hash sum is wrong!")
        result = bytes(resultbody)

    elif hashaction == "add":
        print("A hash sum has been added")
    else:
        print("A hash sum was added/wrong")

    if hashaction != "add":
        del resultbody, hashplace



################ FINAL

if omode == "auto": # settings guessing
    if not outfile:
        try:
            result.decode("utf-8")
            omode = "bin"
        except:
            omode = "b64"
    else:
        omode = "bin"


if omode == "b64": # convert encrypted result to base64
    result = base64.b64encode(result)

if not (outfile or infile and keyfromfolder and hashaction == "no"):
    print("================\n") # separator

out(result)

if keyfromfolder: # delete or rename used key
    if keyaction == "rename":
        os.rename(keyfile, keyfile + "_used")
    elif keyaction == "delete":
        os.remove(keyfile)
