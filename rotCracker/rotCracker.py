#!/usr/bin/python
#ROT-x Cracker

cipherText = raw_input("Enter the Cipher Text you want to bruteforce: ")
cipherText = cipherText.strip()

letters = 'abcdefghijklmnopqrstuvwxyz'

for key in range(len(letters)):
	translated = ''

	for symbol in cipherText:
		if symbol.lower() in letters:
			num = letters.find(symbol.lower())
			num = num - key

			if num < 0:
				num = num + len(letters)

			translated = translated + letters[num]

		else:
			translated = translated + symbol

print("Key #{key}: {translated}").format(key=key, translated=translated)
