#!/usr/bin/python
# Sha512 Bruter for Unsalted Dictionary words (English) v1.1

import requests, hashlib
from sys import exit

file = open("dictionary.txt", "r")

r = requests.get('https://vip.udel.edu/crypto/sha512.php')
crack_me_hash = r.text

print("Hash Value to crack: " + crack_me_hash)

for line in file:
    line = line.strip()
    a = hashlib.sha512(line)
    testHash = a.hexdigest()
    
    if testHash == crack_me_hash:
        print("Hash Cracked! Word is: " + line)
        file.close()
        exit()

    else:
pass
