otppy
=====

one-time pad, written with python  

##options

Options for otp.py:

`-o file`, `--output-file=file` - redirect output to the file  
`-i file`, `--input-file=file` - get data from the file  
`-k folder`, `--keys-folder=folder` - get a key from the folder  
`-I mode`, `--input-mode=mode` - input mode (can be `b64` - base64 data, `bin` or `auto`)  
`-O mode`, `--output-mode=mode` - output mode (can be `b64`, `bin` or `auto`)  
`-c action`, `--hash=action` - use hash sum (`check`- when you decrypt a message or `add` - when you encrypt a message, `no` - don't use (not recommended) or `auto` (by default))  
`-z action`, `--zip=action` - `compress`(`c`) or `decompress`(`d`) data, `no` - don't use or `auto` - don't compress data, but decompress if it looks compressed, by default.  
`-a algorithm`, `--compress-algorithm=algorithm` - algorithm for compressing data, `gzip` (by default) or `bzip2`.  
`-K`, `--key-action action` - action to do with used key (`leave`, `delete`, `shred` (secure delete), or `rename` to mark as used)  

##key generation

To generate keys, make a folder and put some files there. It's recommended to use your own files, that were not published. Total size of files should be in several times bigger than total keys size. Then use the `./keygen.py <folder> <keys_number> <key_length> [t]` command. After generation files, that were in the folder will be deleted.

##getting started

If you have already got key sets, skip steps 1 and 2.

1. Generate 2 folders with keys as described in previous paragraph. It's recommended to generate 100-10000 keys with a 100-10000 bytes size according to the situation. If you have a one-way communication, you can only generate one folder with keys or generate small 2 folder.
2. Send this folders to your recipient using a **secure** channel. You can zip the folder without compression.
3. To encrypt a message, use the `./otp.py -k you_to_interlocutor` command. Enter your message and press enter. Now the result is ready to be sent to the recipient.
4. To decrypt a message, use command `./otp.py -k interlocutor_to_you`, then enter the encrypted text.
5. Each key must be used only once. The number of keys is equal to the number of files in your keys folder, excluding files ending with "_used". When you run out of your keys set, you won't be able to encrypt anything until you repeat steps 1 and 2.

##examples

generation of a new folder with 10 keys 10 KB size:

    ./keygen.py keys 10000 10

encryption/decryption with manual text and key input:

    ./otp.py

encryption with bzip2 compression:

    ./otp.py -z c -a bzip2

encryption/decryption with manual text and adding a hashsum:

    ./otp.py -c add

encryption/decryption with manual text input and getting the key from the folder:

    ./otp.py -k keys

file decryption with getting the key from the folder:

    ./otp.py -k keys -i file.in -o file.out


##also

* It's highly recommended to generate 2 sets of keys: for outgoing messages and for incoming messages. Avoid simultaneous usage of the same key - it is insecure, however may happen if you and your interlocutor, both send messages at the same time.
* If a malefactor knows a part of a message or key, he can replace the part of message with any other text. Use hash sums to prevent it. Note, that using hash sums cannot protect you if the malefactor knows the full text or key.
* If you see message "The hash sum was added/wrong" when you encrypt you data, it means, thay the hash sum have been added, so everything is ok, but if you see this message when you decrypt data, it means, that the message have been modifyed.
* If you encrypt files, make sure, that file size, multiplied by 3 is less than free RAM. You can also save some time setting right hash action and/or compressing option.
* The program can be used if you have 2 channels, which both can be wiretapped. In this case you should send the keys set using one channel and messages using another one. To decrypt messages, both channels must be wiretapped.
* The security of the cipher depends on the way of keys transmission. It's recommended to transmit keys on a face-to-face, meeting using a flash storage or a CD. Also you can encrypt keys using truecrypt, encrypted zip, etc.
* Note, that some symbols, like Cyrillic letters, can use more than 1 byte for each symbol.
* Shredding a used key sometimes may not work correct. Read the manual for Gnu Shred.
* You can compress text data to minimize used storage.
* You can get more information about the one-time pad cipher [on wikipedia](http://en.wikipedia.org/wiki/One-time_pad)
* Should you detect a bug, have some questions or want to make a suggestion, feel free to contact me using [email](mailto:anton-tsyganenko@yandex.ru) or [jabber](xmpp:antontsyganenko@jabber.ru).
