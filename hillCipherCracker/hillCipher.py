#!/usr/bin/python
# Hill 2x2 Cipher

from sys import exit
import numpy
from collections import Counter
import itertools
import textwrap
import random


bigrams = []
alphabet = "abcdefghijklmnopqrstuvwxyz"
cipherText = ""

encText = "tquyantfqjqqcxjomovbsdvsoebmmollllwkxoawdshczluyrjmbsbgcmovbsdtquyantfqjiysiozjkqjpevvyodibwvsfbtydtzsvvwkigjrtuwsavanosvvwmuyjrfgkwvshcjokqoaridkiyvorzctvysbqugnfjyxosmlyoawggvsvoyxcxwkuunawsgnvtsovcujshqtzspeggvsllshefusgnuocajegtkaaeandtavshlaeesbfmjeichpinejgldvuzrmctvcshllwrzwdtvcqzqqdydqtydtzsqhqsylpudqdovshcxulppefgrxzsshgkbmqjcrwrcrqdykemxwshllilieputaizyzzsipqdykemxbintydhejgldvuzrmctvckkpellepsbnwxjsdllsomovstnaiitintydhyperwxuynaajcepullggbqmfmjllmuewoasduyvyvoanxbubklowbmbqfbilcrqzqqanyzfmjejcexshujifqstqphcpllosqsjxcrqyrxzssjmothiepcgtvoeqtjuodqzsjeevcrydrcloglcalp" # paste cipher text here
decodedText = ""

status_code = False

def encFunc(x, y):
	global cipherText
	#encrypt Vars?
	axby = (a * x) + (b * y)
	cxdy = (c * x) + (d * y)

	charcode1 = axby % 26
	charcode2 = cxdy % 26

	cipherText += alphabet[charcode1]
	cipherText += alphabet[charcode2]

def popGrams():
	ngrams = lambda a, n: zip(*[a[i:] for i in range(n)])
	bi = Counter(ngrams(encText, 2)).most_common(10)
	l = textwrap.wrap(encText, 2)
	for entry in bi:
	    print "".join(entry[0]), entry[1],
	    bigramEntry = ''.join(entry[0])
	    bigrams.append(bigramEntry)

	print("\n")
	print(bigrams)

	while status_code == False:
		xx = alphabet[random.randint(0,25)] + alphabet[random.randint(0,25)]
		yy = alphabet[random.randint(0,25)] + alphabet[random.randint(0,25)]
		keygen(xx, yy)

def keygen(bigram1, bigram2):
	print("Generating a key using :  " + bigram1 + " and " + bigram2)
	key = numpy.matrix('0 0; 0 0') # Initialize the key matrix
	key[0,0] = alphabet.find(bigram1[0])
	key[0,1] = alphabet.find(bigram1[1])
	key[1,0] = alphabet.find(bigram2[0])
	key[1,1] = alphabet.find(bigram2[1])

	geninversekey(key)

#key = numpy.matrix('7 8; 11 11') # HI LL


def geninversekey(key):
	a = key[0,0]
	b = key[0,1]
	c = key[1,0]
	d = key[1,1]

	determinant = ((a * d) - (b * c)) % 26
	determinentInverse = ''

	for i in range(26):
		xx = (i * determinant) % 26
		if xx == 1:
			determinantInverse = i
			

	#Create the adjugate matrix
	adjugateMatrix = numpy.matrix('0 0; 0 0') #initialize the matrix
	adjugateMatrix[0,0] = d
	adjugateMatrix[0,1] = -b + 26
	adjugateMatrix[1,0] = -c + 26
	adjugateMatrix[1,1] = a
	
	#set each matrix to a var for maths!
	a_aM = adjugateMatrix[0,0]
	b_aM = adjugateMatrix[0,1]
	c_aM = adjugateMatrix[1,0]
	d_aM = adjugateMatrix[1,1]

	inverseKey = numpy.matrix('0 0; 0 0') #initialize the matrix
	inverseKey[0,0] = (determinant * a_aM) % 26
	inverseKey[0,1] = (determinant * b_aM) % 26
	inverseKey[1,0] = (determinant * c_aM) % 26
	inverseKey[1,1] = (determinant * d_aM) % 26

	decoder(inverseKey, encText)


def decoder(inverseKey, cipha):
	global decodedText
	# this will generate decoded Text based on the cipha text digrams
	ciphaCounta = 0
	decodedText = ""
	for i in range(len(cipha) / 2):
		letter1 = cipha[ciphaCounta]
		letter2 = cipha[ciphaCounta + 1]
		x = alphabet.find(letter1)
		y = alphabet.find(letter2)

		letter1Code = ((inverseKey[0,0] * x) + (inverseKey[0,1] * y)) % 26
		letter2Code = ((inverseKey[1,0] * x) + (inverseKey[1,1] * y)) % 26

		decodedText += alphabet[letter1Code] + alphabet[letter2Code]
		ciphaCounta = ciphaCounta + 2

	substring = "ofthe"

	if decodedText.find(substring) is not -1:
		print(inverseKey)
		print(decodedText)
		answer = raw_input("\nIs the decoding correct? type yes to write to file, no to continue searching.  ")
		answer = answer.strip().lower()

		if answer[0] == 'y':
			with open('decoded.txt', 'a') as file_object:
				file_object.write(decodedText)
				file_object.write("\n")
				file_object.write("\n")
				exit()
		else:
			pass


#key = CHAZ which doesn't work... because the determinant is 50, which is not coprime to the modulus.
# try HILL
#Hard coded key values for encryption (HILL), which works with a decryption routine of inverse key of HILL
a = 7
b = 8
c = 11
d = 11

# Main Routine
choice = raw_input("Which function would you like to run?\n\t1.Encrypt\n\t2.Decrypt\n\tChoose your option (number): ")
#choice = '2' # hardcoding value for multiple automated runs with BASH
if int(choice.strip()) == 1:
	ptMessage = raw_input("Enter Plaintext: ")
	ptMessage = ptMessage.strip().lower().replace(" ", "")

	#This will verify that the length of the message is an even number, if not it will pad with an x
	if (len(ptMessage) % 2) == 1:
		print("Message is one character short. Padding message.")
		ptMessage += "x"

	print('Length of message: ' + str(len(ptMessage)))

	i = 0 	#this will be used to grab the 1st char of the bigram 
	j = 1 	#this will be used to grab the 2nd char of the bigram 

	for step in range(len(ptMessage) / 2):
		char1 = ptMessage[i]
		char2 = ptMessage[j]

		# **Do stuff like mathz**
		if char1 in alphabet:
			num1 = alphabet.find(char1)

		if char2 in alphabet:
			num2 = alphabet.find(char2)

		i = i + 2
		j = j + 2

		encFunc(num1, num2)
	print(cipherText)

elif int(choice.strip()) == 2:
	popGrams()


else:
	choicez = False

	while choicez == False:
		choice = raw_input("Please enter 1 for encryption or 2 for decryption.\n\tEnter your choice: ")

		if int(choice.strip()) == 1:
			choicez = True
			ptMessage = raw_input("Enter Plaintext: ")
			ptMessage = ptMessage.strip().lower().replace(" ", "")

			#This will verify that the length of the message is an even number, if not it will pad with an x
			if (len(ptMessage) % 2) == 1:
				print("Message is one character short. Padding message.")
				ptMessage += "x"

			print('Length of message: ' + str(len(ptMessage)))

			for step in range(len(ptMessage) / 2):
				char1 = ptMessage[i]
				char2 = ptMessage[j]

				# **Do stuff like mathz**
				if char1 in alphabet:
					num1 = alphabet.find(char1)

				if char2 in alphabet:
					num2 = alphabet.find(char2)

				i = i + 2
				j = j + 2
				encFunc(num1, num2)
			print(cipherText)

		elif int(choice.strip()) == 2:
			choicez = True
			popGrams()


'''
Maths:
-----------+
The Below Math will generate the ciphertext

Key(M) (A 2x2 matrix)
positions: a = 25, b = 3, c = 9, d = 20

-------     -----      -------------     ---------
|25  3|     | x |      | (ax + by) |     | axby  |    axby % 26 [Remaining value is the position of the letter]
|     |  X  |   |  =   | --------- |  =  | ----- |  = 
|9  20|     | y |      | (cx + dy) |     | cxdy  |    cxdy % 26 [Remaining value is the position of the letter]
-------     -----      -------------     ---------

The Below Math will decrypt the ciphertext using the inverse

Finding the Inverse is 1st then we use the same math as above, 
except instead of the key, we use the inverse matrix as the key
and use the cipher text as x & y. The result is the plaintext.

General Method to calculate the inverse Key matrix:

	K ^ -1 = d ^ -1 x adj(K)

	-> K is the key matrix, 
	-> d is the determinant of the key matrix 
	-> and adj(K) is the adjugate matrix of K


Finding the determinant in 2x2 matrix:
	[[25,3], [9,20]]
	determinant = (ad - bc) % 26
		-> ex. ( (25 * 20) - (3 * 9) )% 26
			-> (500 - 27) % 26 
			-> 473 % 26 == 5  --> which means our determinant is 5

We now need to find the multiplicative inverse of the determinant working modulo 26.
	In laymans terms, we need to find the number between 1 and 25, which gives an answer of 1
	when we multiply it by the determinant.

	-> ex. dd ^ -1 = 1 % 26 (any number 1-25 % 26 is it's own value...)
		-> 5 * 21 = 105
		-> 105 % 26 = 1
		so our multiplicative inverse of the determinant is 21. 


Now that we have dd ^ -1, we need to find the adjugate matrix:

	The adjugate matrix is a matrix of the same size as the original. 
	For a 2 x 2 matrix, this is fairly straightforward as it is just 
	moving the elements to different positions and changing a couple 
	of signs. That is, we swap the top left and bottom right numbers 
	in the key matrix, 	and change the sign of the the top right and 
	bottom left numbers.

adj ([[a,b]], [c,d]]) = [[d, -b], [-c, a]]

	-> ex.  [[25,3], [9,20]]
		-> 1st, swap places and change signs
			-> [[20, -3], [-9, 25]]
		-> 2nd we need to add 26 to the negative values to get a # between 0 and 25
			-> adjugateMatrix = [[20, 23], [17, 25]]

Now to get the Inverse Key, we will multiply each value in the adjugate matrix by the determinant value and % 26 them

 	-> ex. 5 * [[20, 23], [17, 25]] 
 		-> [[100, 115], [85, 125]] % 26
 		-> inverseKey = [[22, 11], [7, 21]]

Now we have the inverse key matrix, we have to convert the ciphertext into column vectors and 
multiply the inverse matrix by each column vector in turn, take the results modulo 26 
and convert these back into letters to get the plaintext.


ciphertext = "AP"

	plaintext = inverseKey * ciphertext
	PT = ([[20,23], [27,25]]* [0, 15]) % 26
	PT = [abxy, cxdy] % 26

plaintext = "AL"


reference: https://crypto.interactive-maths.com/hill-cipher.html
'''
