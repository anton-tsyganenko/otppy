#!/usr/bin/python3

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

if not decryption: encrypted result convert to hex format
    result = " ".join("{:02x}".format(ord(c)) for c in result)

print (result)