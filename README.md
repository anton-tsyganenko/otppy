otppy
=====

one-time pad, written with python

##options

`-o file`, `--output-file=file` - redirect output to the file  
`-i file`, `--input-file=file` - get data from the file  
`-k folder`, `--keys-folder=folder` - get a key from the folder  
`-I mode`, `--input-mode=mode` - input mode (can be `hex`, `bin` or `auto`)  
`-O mode`, `--output-mode=mode` - output mode (can be `hex`, `bin` or `auto`)  
`-c action`, `--hash=action` - use hash sum (`check`- when you decrypt a message or `add` - when you encrypt a message, `no` - don't use (not recommended) or `auto` (by default))
`--gen-keys` - generate keys  
`--no-spaces` - do not insert spaces into hex code  
`--key-action action` - action to do with used key (`leave`, `delete` or `rename` to mark as used)  

##getting started

If you have already got key sets, skip steps 1 and 2.

1. Generate 2 folders with keys using commands `./otp.py --gen-keys -o you_to_interlocutor` and `./otp.py --gen-keys -o interlocutor_to_you`. The program will ask you the number of keys, that is equal to the number of messages and keys length, that is equal to the maximum length of each message. Do not make them too short or too long. It's recommended to generate 100-10000 keys with a 100-10000 bytes size according to the situation. If you have a one-way communication, you can only generate one folder with keys or generate small 2 folder.
2. Send this folders to your recipient using a **secure** channel. You can zip the folder without compression.
3. To encrypt a message, use the `./otp.py -k you_to_interlocutor` command. Enter your message and press enter. Now the result is ready to be sent to the recipient.
4. To decrypt a message, use command `./otp.py -k interlocutor_to_you`, then enter the encrypted text.
5. Each key must be used only once. The number of keys is equal to the number of files in your keys folder, excluding files ending with "_used". When you run out of your keys set, you won't be able to encrypt anything until you repeat steps 1 and 2.

##examples

generation of a new folder with keys:

    ./otp.py --gen-keys -o keys

encryption/decryption with manual text and key input:

    ./otp.py

encryption/decryption with manual text input and getting the key from the folder:

    ./otp.py -k keys

encryption/decryption with manual text input, getting the key from the folder and adding a hash sum:

    ./otp.py -k keys -c add

file decryption with getting the key from the folder and checking the hash sum:

    ./otp.py -k keys -i file.in -o file.out -c check

if you need to decode hex code into text, use the `./otp.py -I hex -O bin` command. Use zeros as a key:

    enter the text > 68 65 6c 6c 6f 2c 20 70 79 74 68 6f 6e
    enter the key > 00 00 00 00 00 00 00 00 00 00 00 00 00
    ================

    hello, python

##also

* It's highly recommended to generate 2 sets of keys: for outgoing messages and for incoming messages. Avoid simultaneous usage of the same key - it is insecure, however may happen if you and your interlocutor, both send messages at the same time.
* If a malefactor knows a part of a message or key, he can replace the part of message with any other text. Use hash sums to prevent it. Note, that using hash sums cannot protect you if the malefactor knows the full text or key.
* If you encrypt files, make sure, that file size, multiplied by 3 is less than free RAM
* The program can be used if you have 2 channels, which both can be wiretapped. In this case you should send the keys set using one channel and messages using another one. To decrypt messages, both channels must be wiretapped.
* The security of the cipher depends on the way of keys transmission. It's recommended to transmit keys on a face-to-face, meeting using a flash storage or a CD. Also you can encrypt keys using truecrypt, encrypted zip, etc.
* Note, that some symbols, like Cyrillic letters, can use more than 1 byte for each symbol.
* You can get more information about the one-time notepad cipher [on wikipedia](http://en.wikipedia.org/wiki/One-time_pad)
* Should you detect a bug, have some questions or want to make a suggestion, feel free to contact me using [email](mailto:anton-tsyganenko@yandex.ru) or [jabber](xmpp:antontsyganenko@jabber.ru).
