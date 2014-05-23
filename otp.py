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
import shred
import gzip
import bz2

NOT_ENOUGH_KEYS = 5          # for warning (see KEY INPUT)


# FUNCTIONS

def bxor(b1, b2):            # use xor for bytes
    result = bytearray()
    for b1, b2 in zip(b1, b2):
        result.append(b1 ^ b2)
    return bytes(result)


def out(output):
    if output_file:          # output to a file
        with open(output_file, "bw") as ofile:
            ofile.write(output)
    else:
        print(output.decode())


# OPTIONS

parser = optparse.OptionParser()

parser.add_option("-o", "--output-file",
                  dest="output_file",
                  help="write output to FILE",
                  metavar="FILE")

parser.add_option("-i", "--input-file",
                  dest="input_file",
                  help="get data from FILE",
                  metavar="FILE")

parser.add_option("-k", "--keys-folder",
                  dest="key_source",
                  help="get a key from FOLDER",
                  metavar="FOLDER")

parser.add_option("-K", "--key-action",
                  dest="key_action",
                  choices=["leave", "delete", "rename", "shred"],
                  default="rename",
                  help=("action to do with used key, can be "
                        "`leave`, `rename`, `delete` or `shred`"),
                  metavar="ACTION")

parser.add_option("-I", "--input-mode",
                  dest="input_mode",
                  default="auto",
                  help="input mode, can be `bin`, `b64` or `auto`",
                  choices=["bin", "b64", "auto"],
                  metavar="MODE")

parser.add_option("-O", "--output-mode",
                  dest="output_mode",
                  default="auto",
                  choices=["bin", "b64", "auto"],
                  help="output mode, can be `bin`, `b64` or `auto`",
                  metavar="MODE")

parser.add_option("-g", "--gen-keys",
                  dest="key_generation",
                  default=False,
                  action="store_true",
                  help="generate keys")

parser.add_option("-c", "--hash",
                  dest="hash_action",
                  choices=["no", "auto", "add", "check"],
                  default="auto",
                  metavar="ACTION",
                  help="action to do with hash sum")

parser.add_option("-z", "--zip",
                  dest="compresser_action",
                  choices=["compress", "c", "decompress", "d", "no", "auto"],
                  # "auto" is like "no", but decompress gzip if found.
                  default="auto",
                  metavar="ACTION",
                  help="(de)compress data")

parser.add_option("-a", "--compress-algorithm",
                  dest="compress_algorithm",
                  choices=["gzip", "bzip2"],
                  default="gzip",
                  metavar="ALGORITHM",
                  help="compress algorithm")


(options, args) = parser.parse_args()

input_file = options.input_file
output_file = options.output_file
key_source = options.key_source
key_action = options.key_action
input_mode = options.input_mode
output_mode = options.output_mode
key_generation = options.key_generation
hash_action = options.hash_action
compresser_action = options.compresser_action
compress_algorithm = options.compress_algorithm

if hash_action in ["auto", "add"]:
    hash_length = 20
else:
    hash_length = 0

if compresser_action == "c":
    compresser_action = "compress"
elif compresser_action == "d":
    compresser_action = "decompress"

if compress_algorithm == "gzip":
    compresser = gzip
elif compress_algorithm == "bzip2":
    compresser = bz2

if compresser_action in ["compress", "decompress"] and hash_action == "auto":
    hash_action = "no"

# KEY GENERATION

if key_generation:
    number = int(input("number of keys > "))
    length = int(input("key length > "))

    if output_mode == "b64" or not output_file:
        # text with keys in base64
        result = b""
        for i in range(number):
            result += base64.b64encode(os.urandom(length)) + b"\n"
        out(result)

    else:                    # folder with binary key files
        os.makedirs(output_file, exist_ok=True)
        for i in range(number):
            with open(output_file + os.sep + str(i), "xb") as f:
                f.write(os.urandom(length))

    exit()


# TEXT INPUT

if input_file:               # from a file
    with open(input_file, "rb") as tfile:
        text = tfile.read()

    if input_mode == "auto":
        input_mode = "bin"

else:                        # direct input
    text = bytes(input("enter the text > "), "utf-8")


if input_mode in ["auto", "b64"]:
    try:                     # try to decode base64
        text = base64.b64decode(text.decode(), validate=True)
    except base64.binascii.Error:
        if input_mode == "b64":
            print("Cannot decode base64!")
            exit()


if compresser_action == "compress":
    text = compresser.compress(text)


# KEY INPUT

if key_source:                    # use folder with keys or a key_file
    if os.path.isdir(key_source):           # folder with keys
        files_list = os.listdir(key_source)

        for i in files_list[:]:             # don't use used keys
            if i.endswith("_used"):
                files_list.remove(i)

        if len(files_list) == 0:
            print("================\n"
                  "NO KEYS IN {ks}!".format(ks=key_source))
            exit()

        if len(files_list) <= NOT_ENOUGH_KEYS:
            print("================\n"
                  "WARNING! only {k} keys left, and one of them "
                  "will be used now.".format(k=len(files_list)))

        key_file = key_source + os.sep + max(files_list, key=int)
        with open(key_file, "br") as f:
            key = f.read(len(text)+hash_length)

        key_from_folder = True         # see FINAL

        del files_list
    else:                     # a keyfile
        with open(key_source, "br") as f:
            key = f.read(len(text)+hash_length)
        key_from_folder = False

    del key_source, hash_length

else:                        # manually input the key
    key = base64.b64decode(input("enter the key > "))
    key_from_folder = False


# ADD A HASH SUM

if hash_action in ["add", "auto"]:
    text += hashlib.sha1(text).digest()


# DON'T LET USER TO USE TOO SHORT KEY

if len(key) < (len(text)):
    print("The key is too short.")
    if hash_action == "auto" and len(key) >= (len(text)-20):
        print("If you're decrypting data, try to use `-c check` option")
    exit()


# ENCRYPTION/DECRYPTION

result = bxor(text, key)
del text, key


# DETECT COMPRESSED DATA AND DECOMPRESS IT

if compresser_action in ["decompress", "auto"]:
    # gzip data starts with 1F 8B, bzip - 'BZh'
    compressed_detected = False

    if result[0:3] == b'BZh':
        compresser = bz2
        compressed_detected = True
    elif result[0:2] == b'\x1f\x8b':
        compresser = gzip
        compressed_detected = True

    hash_backup = result[-20:]

    if compressed_detected and hash_action == "auto":
        result = result[0:-20]
        hash_action = "no"

    try:
        result = compresser.decompress(result)
    except:
        if compresser_action == "decompress":
            print("Cannot decompress result!")
            exit()
        elif compressed_detected:
            result += hash_backup
            hash_action = "auto"
    else:
        print("Decompressed result")

    del compressed_detected, hash_backup


# CHECK A HASH SUM

if hash_action != "no":
    if hash_action == "check":
        hash_place = memoryview(result)[-20:]
        body = memoryview(result)[0:-20]
    elif hash_action == "auto":
        # in auto mode the program adds new hash sum(see ADD A HASH SUM)
        hash_place = memoryview(result)[-40:-20]
        body = memoryview(result)[0:-40]

    if hash_action != "add":
        result_hash = hashlib.sha1(body).digest()

    print("================")

    if hash_action != "add" and result_hash == hash_place:
        print("The hash sum is ok")
        result = bytes(body)

    elif hash_action == "check":
        print("The hash sum is wrong!")
        result = bytes(body)

    elif hash_action == "add":
        print("A hash sum has been added")
    else:
        print("A hash sum was added/wrong")

    if hash_action != "add":
        del body, hash_place


# FINAL

if output_mode == "auto":    # settings guessing
    if not output_file:
        try:
            result.decode()
        except UnicodeDecodeError:
            output_mode = "b64"
        else:
            output_mode = "bin"
    else:
        if output_mode == "auto":
            output_mode = "bin"


if output_mode == "b64":
    result = base64.b64encode(result)

if not (output_file or input_file and
        key_from_folder and hash_action == "no"):
    print("================\n")

out(result)

if key_from_folder:          # delete or rename used key
    if key_action == "rename":
        os.rename(key_file, key_file + "_used")
    elif key_action == "delete":
        os.remove(key_file)
    elif key_action == "shred":
        shred.shred(key_file)
