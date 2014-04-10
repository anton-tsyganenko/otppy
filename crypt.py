#!/usr/bin/python3

try:
  def encrypt(text, key):
    i = 0
    encrypted = ""
    for t in text:
      p = key[i]
      i += 1
      encrypted += str(ord(t)+ord(p)) + " "
    return encrypted[:-1]

  def decrypt(text, key):
    try:
      i = 0
      decrypted = ""
      text = text.split(" ")
      for t in text:
        p = key[i]
        i += 1
        decrypted += chr(int(t)-ord(p))
      return decrypted
    except ValueError:
        return "Ошибка! скорее всего вы ввели не последовательность чисел, разделенных пробелом."

  def resize_key(key, text):
    while True:
      if len(text) > len(key):
        key += key
      else:
        break
    return key

  while True:
    print ('наберите "з" или "e" чтобы зашифровать сообщение или "р" или "d" чтобы расшифровать сообщение, или "в" или "ex" для выхода')
    cmd = input("> ")

    if cmd in ["e", "з", "е"]:
      text = input("введите сообщение > ")
      key = input("введите ключ > ")
      encrypted = encrypt(text, resize_key(key, text))
      print (encrypted)
    elif cmd in ["d", "р", "p"]:
      text = input("введите шифротекст > ")
      key = input("введите ключ > ")
      decrypted = decrypt(text, resize_key(key, text))
      print (decrypted)
    elif cmd in ["ex", "в", "ех"]:
      break
    else:
      print("Ошибка!")
except Exception as err:
  print('Произошла ошибка! отправьте на адрес "anton-tsyganenko@yandex.ru" это:')
  print(err)
