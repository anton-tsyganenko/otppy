otppy
=====

one-time pad, written with python

##options

`-o file` - redirect output to a file  
`-i flie` - get a data from a file  
`-ki folder` - get a key from a folder  
`--imode mode` - input mode (can be hex or bin)  
`--omode mode` - output mode (can be hex or bin)  
`--gen-key` - generate keys  
`--no-spaces` - do not insert spaces in hex code  
`--do-not-delete-key` - do not delete the key after usage  

##getting started

1. Generate a folder with keys using the `./otp.py --gen-key -o keys_folder --omode bin` command. The program will ask you the number of keys, that is equal to the number of messages and keys length, that is equal to the maximum length of each message. Do not make them too small or too big. It's recommended to generate 100-10000 keys with a 100-10000 bytes size according to the situation.
2. Send the folder to your recipient using a **secure** channel. You can zip the folder without a compression.
3. To encrypt a message use the `./otp.py -ki keys_folder` command. Enter your message, then press enter and then ctrl+d. Send the result to your recipient.
4. To decrypt the message, use the same command (`./otp.py -ki keys_folder`). Enter the encrypted text, press enter and ctrl+d.
5. Be careful to not over keys. The number of keys is equal to the number of files in your keys folder. When your keys are over, repeat 1 and 2 steps.

##examples

generation of a folder with keys:

    ./otp.py --gen-key --omode bin -o keys

encryption/decryption with manual text and key input:

    ./otp.py

encryption/decryption with manual text input and getting a key from a folder:

    ./otp.py -ki keys

file encryption with getting a key from a folder:

    ./otp.py -ki keys -i file.in -o file.out

if you need to get a text from a hex code, use the `./otp.py --imode hex --omode bin` command. Use zeros as a key:

    enter the text, then press ENTER; CTRL+D
    68 65 6c 6c 6f 2c 20 70 79 74 68 6f 6e
    enter the key > 00 00 00 00 00 00 00 00 00 00 00 00 00
    ================

    hello, python

##also

* Used keys are being deleted. Use the `--do-not-delete-key` option to prevent it.
* Do not encrypt large files. Feel free to encrypt small files (about a few KB), encryption of bigger files (a few MB) will take longer, encryption of big files (more than 100 MB) will be **very** long. **Make sure that the total size of the file and the key is lesser than free RAM**
* The program can be used if you have 2 channels, each of those can be wiretapped. In this case you should send keys using one channel and messages using another one. To decrypt messages both channels must be wiretapped by the same person.
* The secure of the crypt depends on the way of keys transmission. It's recommended to transmit keys on a face-to-face meeting using a flash storage or a CD. Also you can encrypt keys using truecrypt, encrypted zip, etc.
* Note, that some symbols, like cyrillic letters, can use more than 1 byte for each symbol.
* You can get more information about the one-time notepad crypt [on wikipedia](http://en.wikipedia.org/wiki/One-time_pad)
* If you find a bug, have some questions or want to make a suggestion, feel free to contact me using [email](mailto:anton-tsyganenko@yandex.ru) or [jabber](xmpp:antontsyganenko@jabber.ru).
