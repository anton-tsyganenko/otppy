#!/usr/bin/python3

decryption = False

def sxor(str1, str2): # use xor for strings
    return ''.join(chr(ord(str1) ^ ord(str2)) for str1, str2 in zip(str1, str2))

def resize_key(key, text):
    if len(key) < len(text):
        print("the key must have the text length or be longer")
        exit()
    return key

text = input("enter the text > ")
try:
    text = bytes.fromhex(text).decode('utf-8').replace(" ", "")
    decryption = True
except:
    pass

key = input("enter the key > ")
try:
    key = bytes.fromhex(key).decode('utf-8').replace(" ", "")
except:
    print ("the key must be in HEX format")
    exit()

result = sxor(text, resize_key(key, text))

if not decryption:
    result = " ".join("{:02x}".format(ord(c)) for c in result)

print (result)