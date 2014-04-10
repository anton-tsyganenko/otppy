#!/usr/bin/python3

decryption = False

def sxor(str1, str2): # use xor for bytes
    return ''.join(chr(str1 ^ str2) for str1, str2 in zip(str1, str2))

def validate_key(key, text):
    if len(key) < len(text):
        print("the key must have the text length or be longer")
        exit()
    return key

text = input("enter the text > ")
try:
    text = bytes.fromhex(text.replace(" ", ""))
    decryption = True
except:
    text = bytes(text, "utf-8")

key = input("enter the key > ")
try:
    key = bytes.fromhex(key.replace(" ", ""))
except:
    print ("the key must be in HEX format")
    exit()

result = str(sxor(text, validate_key(key, text)))

if not decryption:
    result = " ".join("{:02x}".format(ord(c)) for c in result)

print (result)