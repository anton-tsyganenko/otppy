otppy
=====

one-time pad, written with python

##options

`-o file` - redirect output to the file  
`-i file` - get data from the file  
`-ki folder` - get a key from the folder  
`--imode mode` - input mode (can be hex or bin)  
`--omode mode` - output mode (can be hex or bin)  
`--gen-key` - generate keys  
`--no-spaces` - do not insert spaces into hex code  
`--do-not-delete-key` - do not delete the key after usage  

##getting started

1. Generate a folder with keys using the `./otp.py --gen-key -o keys_folder` command. The program will ask you the number of keys, that is equal to the number of messages and keys length, that is equal to the maximum length of each message. Do not make them too short or too long. It's recommended to generate 100-10000 keys with a 100-10000 bytes size according to the situation.
2. Send the folder to your recipient using a **secure** channel. You can zip the folder without compression.
3. To encrypt a message, use the `./otp.py -ki keys_folder` command. Enter your message, then press enter and then ctrl+d. Now the result is ready to be sent to the recipient.
4. To decrypt a message, use the same command (`./otp.py -ki keys_folder`). Enter the encrypted text, press enter and ctrl+d.
5. Each key must be used only once. The number of keys is equal to the number of files in your keys folder. When you run out of your keys set, you won't be able to encrypt anything until you repeat steps 1 and 2.

##examples

generation of a new folder with keys:

    ./otp.py --gen-key -o keys

encryption/decryption with manual text and key input:

    ./otp.py

encryption/decryption with manual text input and getting the key from the folder:

    ./otp.py -ki keys

file encryption with getting the key from the folder:

    ./otp.py -ki keys -i file.in -o file.out

if you need to decode hex code into text, use the `./otp.py --imode hex --omode bin` command. Use zeros as a key:

    enter the text, then press ENTER; CTRL+D
    68 65 6c 6c 6f 2c 20 70 79 74 68 6f 6e
    enter the key > 00 00 00 00 00 00 00 00 00 00 00 00 00
    ================

    hello, python

##also

* Used keys are being deleted. Use the `--do-not-delete-key` option to prevent key deletion.
* Do not encrypt large files. Feel free to encrypt small files (about a few KB), encryption of bigger files (a few MB) will take longer, encryption of big files (more than 100 MB) will be **very** long. **Make sure that the total size of the file and the key is less than free RAM**
* The program can be used if you have 2 channels, whick both can be wiretapped. In this case you should send the keys set using one channel and messages using another one. To decrypt messages, both channels must be wiretapped.
* The security of the cipher depends on the way of keys transmission. It's recommended to transmit keys on a face-to-face, meeting using a flash storage or a CD. Also you can encrypt keys using truecrypt, encrypted zip, etc.
* Note, that some symbols, like cyrillic letters, can use more than 1 byte for each symbol.
* You can get more information about the one-time notepad cipher [on wikipedia](http://en.wikipedia.org/wiki/One-time_pad)
* Should you detect a bug, have some questions or want to make a suggestion, feel free to contact me using [email](mailto:anton-tsyganenko@yandex.ru) or [jabber](xmpp:antontsyganenko@jabber.ru).
