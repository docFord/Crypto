#!/usr/bin/python

# xdg-open is designed to be used on Ubuntu based systems.
# Users on other systems may need to input the appropriate cli
# option to open files.

from Crypto.Cipher import AES
from Crypto import Random
import os, hashlib, binascii
from sys import exit
from PIL import Image


ciphertext = ""

def main():
	choice = raw_input(" Press 1 encrypt a message.\n Press 2 to decrypt a message.\n Press 3 to encrypt an image file.\n Press 4 to decrypt an image file.\n Press 5 to exit.\n If you would like to know how to use this program type help\n\nENTER SELECTION: ")
	choice = choice.strip()
	if choice == '1':
		key = keyType()
		encrypt(key)

	elif choice == '2':
		key = keyType()
		decrypt(key)

	elif choice == '3':
		key = keyType()
		encryptFile(key)

	elif choice == '4':
		key = keyType()
		decryptFile(key)

	elif choice == '5':
		exit()

	elif choice[0].lower() == 'h':
		print("\n*~*~*~*~*~*~~*~*~*~*~*~*~*~*~*~*~*~*\n| You selected the help option.    |\n| This will give a brief overview  |\n| of how the program works.        |\n*~*~*~*~*~*~~*~*~*~*~*~*~*~*~*~*~*~*\n\n[*] All options will first ask you if you are using a hashed password or a string, since both options\n    have been observed in use. It will then ask you for a password, in the case of encryption this\n    will be the key that is used to encrypt your data, whether it is an image or a message, or be\n    used to decrypt the message.\n\n[*] If you are encrypting a message, the program will ask you to type the message you wish to encrypt. \n    After entering your message, the program will display the file that this encrypted message is stored in. \n    The program will then ask you if you wish to return to the main menu or exit.\n\n[*] If you are decrypting a message, make sure that the ciphertext you want to decrypt is stored in \n    the local file encryptedFile.aes. This function will automatically attempt to decrypt the \n    ciphertext using the provided passphrase.\n\n[*] Encrypting an image file will ask you to enter the filename of the image you wish to encrypt. \n    It will then ask if you want to encrypt the image using ECB or CBC mode. Then it will have you\n    enter the output filename, without the file extension as the program will automatically store \n    the file as a png.\n\n[*] If you are decrypting an image, the program will ask you for the filename of the file you wish to \n    decrypt. It will then ask you which mode was used to encrypt the image. If CBC mode is selected,\n    the program will ask you if the IV is located at the beginning or the end of the byte array.\n    Then the program will store your decrypted file as [filename]-decrypted.png\n\n[!] Please note that if you do not enter the correct passphrase, the messages or images will not \n    decrypt to their plaintext. \n")

	else:
		print("\nInvalid Input. Returning to Main Menu.\n")
		main()

def keyType():
	choice = raw_input('Is the key a hash of a passphrase, or a string? Press 1 for Hash or 2 for string: ')
	choice = choice.strip()

	if choice == '1':
		pw = raw_input("Enter encryption password to be hashed: ")
		pw = pw.strip()
		key = hashlib.sha256(pw).digest() #32 bytes
		return key

	elif choice == '2':
		pw = raw_input("Enter encryption password, if must be 16 characters long!!: ")
		key = pw.strip()
		if len(key) != 16:
			print("Key Length not valid! Enter a 16 character passphrase!")
			pw = raw_input("Enter encryption password, if must be 16 characters long!!: ")
			key = pw.strip()

			if len(key) != 16:
				print("You can't follow instructions so program will not exit!")
				exit()
		return key

	else:
		print("Invalid Input. Returning you to the start of this function.")
		keyType()


def pad(s):
	return s + b"\0" * (AES.block_size - len(s) % AES.block_size)


def encrypt(key):
	global ciphertext
	message = raw_input("Enter message to encrypt: ")
	message = message.strip()
	message = pad(message)
	
	iv = os.urandom(AES.block_size)
	obj = AES.new(key, AES.MODE_CBC, iv)
	
	inp = iv + message

	ciphertext = obj.encrypt(message)
	ciphertext_hex = iv + binascii.hexlify(ciphertext)

	with open('encryptedFile.aes', 'wb') as f:
		f.write(ciphertext_hex)
		f.close()

	choice = raw_input("If you wish to return to the main menu press 1, otherwise program will exit: ")
	if choice[0] == '1':
		main()
	else:
		exit()


def decrypt(key):
	with open('encryptedFile.aes', 'rb') as f:
		ct = f.read()
		iv = ct[0:AES.block_size] #value should be 16
		ct = binascii.unhexlify(ct[16:])
	obj = AES.new(key, AES.MODE_CBC, iv)
	plaintext = obj.decrypt(ct)
	print("Decrypted Text:\n" + plaintext)

	choice = raw_input("If you wish to return to the main menu press 1, otherwise program will exit: ")
	choice = choice.strip()
	if choice == '1':
		main()
	else:
		print("Exiting Program.")
		exit()


def encryptFile(key):
	filename = raw_input("Enter filename to encrypt: ")
	filename = filename.strip()

	choicer = raw_input("Which AES mode do you want to use, ECB or CBC? Press 1 for ECB, or 2 for CBC: ")
	choicer = choicer.strip()

	if choicer == '1':
		obj = AES.new(key, AES.MODE_ECB)

		im = Image.open(filename)
		x = width, height = im.size #create a tuple of the image size
		imBytes = im.convert('RGB').tobytes()
		imBytes = pad(imBytes)
		#print(x) #verify the image size

		ct = obj.encrypt(imBytes)

	elif choicer == '2':
		iv = os.urandom(AES.block_size)
		obj = AES.new(key, AES.MODE_CBC, iv)

		im = Image.open(filename)
		x = width, height = im.size #create a tuple of the image size
		imBytes = im.convert('RGB').tobytes()
		imBytes = pad(imBytes)
		#print(x) #verify the image size

		imBytes = im.convert('RGB').tobytes()
		imBytes = pad(imBytes)

		ct = obj.encrypt(imBytes)
		ct = ct + iv

	else:
		print("Invalid Input. Returning you to the start of the function.")
		encryptFile(key)


	j = Image.frombytes('RGB', x, ct)

	fileN = raw_input('Enter the output filename, (the program will autosave as .png): ')
	fileN = fileN.strip()
	fileN = fileN + ".png"
	j.save(fileN)
	print("File saved as " + fileN)

	#j.save('dog.png')

	choice = raw_input("If you wish to return to the main menu press 1, otherwise program will exit: ")
	choice = choice.strip()
	if choice == '1':
		main()
	else:
		print("Exiting Program.")
		exit()


def decryptFile(key):
	filename = raw_input("Enter filename to decrypt: ")
	filename = filename.strip()

	im = Image.open(filename)
	x = width, height = im.size

	imBytes = im.convert('RGB').tobytes()

	aesMode = raw_input('What mode of encryption was used? Press 1 for ECB mode, or 2 for CBC mode: ')
	aesMode = aesMode.strip()

	if aesMode == '1':
		obj = AES.new(key, AES.MODE_ECB)

	elif aesMode == '2':
		ivChoice = raw_input('Is the IV located at the [beginning] or the [end] of the byte array? Press 1 for beginning, and 2 for end.\nChoice: ')
		ivChoice = ivChoice.strip()

		if ivChoice == '1':
			iv = imBytes[:AES.block_size]

		elif ivChoice == '2':
			iv = imBytes[-AES.block_size:]

		else:
			print("Invalid Input. Returning you to start of function.")
			decryptfile(key)

		obj = AES.new(key, AES.MODE_CBC, iv)

	else:
		print('Invalid Input. Returning you to the start of this function.')
		decryptFile(key)
	
	imBytes = pad(imBytes)
	pt = obj.decrypt(imBytes)

	j = Image.frombytes('RGB', x, pt)

	print("Output file is " + filename[:-4] + "-decrypted.png")
	outputFile = filename[:-4] + "-decrypted.png"

	j.save(outputFile)

	#j.save('cbc.png')

	choice = raw_input("If you would like to view the decrypted image and then exit, press 0\nIf you wish to return to the main menu press 1\n Otherwise program will exit: ")
	choice = choice.strip()
	if choice == '1':
		main()
	elif choice == '0':
		dirPath = os.getcwd() + '/'
		os.system('xdg-open ' + dirPath + outputFile)
		exit()
	else:
		print("Exiting Program.")
		exit()
	

if __name__ == '__main__':
	main()

