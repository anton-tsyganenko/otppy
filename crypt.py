#!/usr/bin/python3

decryption = False

def sxor(str1, str2):
    return ''.join(chr(ord(str1) ^ ord(str2)) for str1, str2 in zip(str1, str2))

def resize_key(key, text):
    while True:
      if len(text) > len(key):
        key += key
      else:
        break
    return key

text = input("введите текст > ")
try:
    text = bytes.fromhex(text).decode('utf-8')
    decryption = True
except:
    pass

key = input("введите ключ > ")
result = sxor(text, resize_key(key, text))

if not decryption:
    result = "".join("{:02x}".format(ord(c)) for c in result)

print (result)