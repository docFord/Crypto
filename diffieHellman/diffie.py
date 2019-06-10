#!/usr/bin/python
from Crypto.Util.number import *

a = "" # alice's secret
b = "" # bob's secret

# ALICE
def createKey(): #used to gen the initial public secret (Alice)
	global a
	while True:
	    for i in range(100):
	        p = getStrongPrime(512)
	        a = getRandomRange(2, p-2) 
	        xxx = GCD(a, p-1)
	        #print xxx
        	if xxx == 1:
        	    base = 2
        	    A = pow(base, a, p)
        	    triplet = (p, base, A)
        	    return triplet

# BOB
def bob(triplet):
	global b
	while True:
		for i in range(100):
			p = triplet[0]
			b = getRandomRange(2, p-2)
			xxx = GCD(b, p-1)
			#print xxx
			if xxx == 1:
				base = triplet[1]
				A = triplet[2]
				B = pow(base, b, p) #base ^ b % p
				triple = (p, base, B)
				return triple


alice = createKey()
bob = bob(alice)

bobsK = pow(alice[2], b, alice[0])
alicesK = pow(bob[2], a, bob[0])

if alicesK == bobsK:
	print "woot!"
else:
	print "oh noes"
	print alicesK
print bobsK
