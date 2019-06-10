#!/usr/bin/python
# Sha256 Bruter (CTF Challenge)

import hashlib
from sys import exit

file = open("findFlag.txt", "r")

flagHashes = []

alphabet = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.,!;:\"()\\{\\}-_+=*&^%$#@\'\\/?"
alphaHash = []

for letter in alphabet:
	letter = letter.strip('\n')
	alphaHash.append(letter)

for liner in file:
	liner = liner.strip()
	flagHashes.append(liner)
file.close()

phrase = ""

for item in flagHashes:
	item = item.strip()

	for letter in alphaHash:
		a = hashlib.sha256(letter).hexdigest()
		if a == item:
			phrase += letter
print(phrase + '\n')
exit()
