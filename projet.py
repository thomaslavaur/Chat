#!/usr/bin/python3
import sys
import random
import subprocess
import re
import socket
import os
import math



							### test_primalite renvoie True si un nombre est premier, False sinon.
							### entree : un nombre entier en base 10
							### sortie : un booleen
def test_primalite(nombre):		
	commande = "openssl prime"
	r = subprocess.run(commande+" "+str(nombre),shell=True,stdout=subprocess.PIPE)		#renvoie le résultat de la commande SHELL openssl prime nombre
	resultat_openssl = r.stdout															#si la chaine contient not alors le résultat n'est pas premier sinon, il l'est
	test= re.compile(r'not')
	if(test.search(str(resultat_openssl))):
		return False
	else:
		return True




							### premiere_generation_nombre (utilisée seulement pour la première génération)
							### entree : un entier en base 10 qui représente le nombre de décimales attendues
							### sortie : un entier en base 10 avec le nombre de décimale attendu
def premiere_generation_nombre(nombre_de_decimale):
	random.seed()
	nombre_premier = int(random.choice('123456789'))*(10**(nombre_de_decimale-1))		#tire au sort le n_max
	for i in range (1,nombre_de_decimale-1):
		nombre_premier = nombre_premier + int(random.choice('0123456789'))*(10**i) 		#tire au sort les n_i pour i dans 1 à n_max - 1
	nombre_premier = nombre_premier + int(random.choice('1379'))						#tire au sort n_0
	return nombre_premier





							### generation_nombre prend un nombre entier non premier et un nombre de décimale et effectue une modification sur celui-ci suivant la méthode du projet
							### entree : deux entiers en base 10
							### sortie : un entier en base 10
def generation_nombre(nombre_pas_premier,nombre_de_decimale):
	random.seed()
	nombre_pas_premier = (nombre_pas_premier*10) % (10**nombre_de_decimale) 										# Shift tout les chiffres 1 fois à gauche et oublie n_max
	if(len(str(nombre_pas_premier))==nombre_de_decimale):															# Vérifie si après un décalage on a bien le nombre de décimale attendu.
		nombre_pas_premier = nombre_pas_premier - (nombre_pas_premier%100)											# Oublie les deux dernières décimales de notre nombre
		nombre_pas_premier = nombre_pas_premier + int(random.choice('0123456789'))*10 + int(random.choice('1379'))	#tire aléatoirement les deux dernières décimales parmies la liste fournie
	else:																											# Si on a pas le bon nombre de décimale on utilise un mélange des deux méthodes pour économiser la fonction rand
		if (nombre_pas_premier < 10**(nombre_de_decimale-1)):
			decimale_manquantes = nombre_de_decimale-len(str(nombre_pas_premier))
			for i in range(0,decimale_manquantes):
				if(i==decimale_manquantes-1):
					nombre_pas_premier = int(str(nombre_pas_premier)+random.choice('1379'))
				else:
					nombre_pas_premier = int(str(nombre_pas_premier)+random.choice('0123456789'))
	return nombre_pas_premier																						#génère un autre nombre candidat à partir de l'ancient




							### nombre_premier prend en entrée un entier et retourne un nombre premier
							### entree : un entier en base 10
							### sortie : un entier premier en base 10 avec le nombre de décimale de l'entree
def nombre_premier(nombre_de_decimale):
	nombre = premiere_generation_nombre(nombre_de_decimale)
	while(not(test_primalite(nombre))):
		nombre = generation_nombre(nombre,nombre_de_decimale)
	return nombre





							#### Renvoie le pgcd de a et b et les coéficients de Bézout x et y tels que ax+by = pgcd(a,b) (cette fonction nous est donnée)
def pgcd(a, b):
	x,y,u,v = 0,1,1,0
	while a != 0:
		q,r = b//a,b%a
		m,n = x-u*q, y-v*q
		b,a,x,y,u,v = a,r,u,v,m,n
	gcd = b
	return gcd,x,y






							#### renvoie l'inverse de a modulo m (cette fonction nous est donnée)
def modinv(a, m):
	gcd,x,y = pgcd(a, m)
	if gcd != 1:
		return None
	return x % m




							#### puissance modulaire: (x**y)%n avec x, y et n entiers (cette fonction nous est donnée)
def lpowmod(x, y, n):
	result = 1
	while y>0:
		if y&1>0:
			result = (result*x)%n
		y >>= 1
		x = (x*x)%n
	return result






							###	Cette fonction prend en entrée un message et une clé et renvoie un tableau d'entier correspondant aux valeurs de chaque sous-message
							### entree : une chaine de caractère et un entier en base 10
							### sortie : un tableau d'entier en base 10
def split_message(message,clé):
	nombre_de_bit_max = int(math.log2(clé))
	nombre_d_octets_max = int(nombre_de_bit_max/8)
	message = bytes(message,"utf8")
	if(verbose):
		print("On transforme notre message en bytes : ",end='')
		print(message)
	m = ["" for i in range(0,len(message),nombre_d_octets_max)]
	if(verbose):
		print("On découpe en sous-messages : ",end='')
	for i in range(0,len(message),nombre_d_octets_max):
		if(verbose):
			print(message[i:i+nombre_d_octets_max],end='')
			print(" , ",end='')
		m[int(i/nombre_d_octets_max)]= to_int(message[i:i+nombre_d_octets_max])
	if(verbose):
		print("\nOn transforme chaque bytes en entier pour trouver le tableau suivant :",end='')
	return(m)





							### Cette fonction prend un entier et le renvoie en bytes
							### entree : un entier en base 10
							### sortie : des bytes 
def to_bytes(entier):
	return(entier.to_bytes((entier.bit_length() + 7) // 8, byteorder='big'))




							### Cette fonction prend des bytes et renvoie l'entier correspondant
							### entree : des bytes
							### sortie : un entier en base 10
def to_int(byte):
	return(int.from_bytes(byte, byteorder='big'))




#Couleurs :
blanc = '\033[0m'
bleu = '\033[96m'
rouge = '\033[91m'
jaune = '\033[93m'
vert = '\033[92m'




							#### choix des fonctionnalités et initialisation des variables
print("\n")
print("Voulez-vous acitver le mode verbose ?[Y/N]".center(os.get_terminal_size().columns))
verbose = input(">")
while((verbose != "Y")&(verbose != "N")):
	print("\nCommande invalide, commande attendue : Y ou N ")
	print("Voulez-vous acitver le mode verbose ?[Y/N]".center(os.get_terminal_size().columns))
	verbose = input(">")
if verbose == 'Y':
	verbose = True
if verbose == 'N':
	verbose = False
print("\n")
print("Combien voulez-vous de décimales pour votre taille de clé ? (>4)".center(os.get_terminal_size().columns))
nombre_de_decimale_de_n = int(input('>'))
while(nombre_de_decimale_de_n < 4):
	print("\n")
	print("nombre incorrect : attendue entier suppérieur ou égal à 4")
	print("Combien voulez-vous de décimales pour votre taille de clé ? (>4)".center(os.get_terminal_size().columns))
	nombre_de_decimale_de_n = int(input('>'))
print("\nGénération des clés. . .\n")
p = nombre_premier(int(((nombre_de_decimale_de_n)/2)-2))
n = p
test = False
while(len(str(n))!= nombre_de_decimale_de_n):
	if test:
		q = nombre_premier(int((nombre_de_decimale_de_n/2)+3))
		test = False
	else:
		q = nombre_premier(int((nombre_de_decimale_de_n/2)+2))
		test = True
	n = p*q
phi = (p-1)*(q-1)
e = 65537
d = modinv(e,phi)
print("Votre clé privée est : ".center(os.get_terminal_size().columns))
print(d,"\n")
print("Votre clé publique est : ".center(os.get_terminal_size().columns))
print(n,"\n")

print("Voulez-vous lancez la version serveur ou client? [serveur/client]".center(os.get_terminal_size().columns))
commande = input(">")
while((commande != "serveur")&(commande != "client")):
	print("\nCommande invalide, commande attendue : client ou serveur ")
	print("Voulez-vous lancez la version serveur ou client? [serveur/client]".center(os.get_terminal_size().columns))
	commande = input(">")
port_serveur = 8790




																		#### Partie SERVEUR (BOB) ####

if(commande == "serveur"):

								# Initialisation du serveur
	print("\nMise en route du serveur. . .")
	ma_chaussette = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	ma_chaussette.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	ma_chaussette.bind(('',port_serveur))
	print("\nEn attente d'une connexion. . .")
	ma_chaussette.listen(socket.SOMAXCONN)
	(nouvelle_connexion,tsap_client) = ma_chaussette.accept()
	print("\nConnexion établie!")


								# Echange des clés
	cle_de_alice = to_int(nouvelle_connexion.recv(2048))
	print("\nClé publique de "+vert+"Alice"+blanc+" reçue!")
	print("\n")
	print(("La clé publique de "+vert+"Alice"+blanc+" est :").center(os.get_terminal_size().columns))
	print(cle_de_alice)
	print("\nEnvoie de votre clé pubique à "+vert+"Alice"+blanc+"\n\n\n\n")
	nouvelle_connexion.sendall(to_bytes(n))
	print(("Début du chat avec "+vert+"Alice"+blanc+", tapez "+rouge+"EXIT "+blanc+"pour un arrêt de la conversation.").center(os.get_terminal_size().columns))
	print("\n")
	message =""
	pid = os.fork()



	if not pid:
							#ceci est le processus fils qui envoie les messages
		while 1:
			print('>',end='')
			message = input()
			if message == "EXIT":
				print(rouge+"Fin du chat"+blanc)								# arret du chat
			if message == "(EXIT)":
				print(rouge+"mot interdit"+blanc)
			else:
				if(verbose):
					print("message à envoyer : "+message)
				m = split_message(message,cle_de_alice)
				if(verbose):
					print(m)
				nouvelle_connexion.sendall(len(m).to_bytes(4, byteorder='big'))	# envoie le nombre de sous-message
				if(verbose):
					print("On envoie le nombre de sous-message : ",len(m))
					print("Qui vaut : ",end='')
					print(len(m).to_bytes(4, byteorder='big'),end='')
					print(" en bytes")
					print("On envoie chaque sous-message après chiffrement")
				for i in m:														# chiffrement et envoie de chaque sous-message
					chiffre = lpowmod(i,e,cle_de_alice)
					nouvelle_connexion.sendall(chiffre.to_bytes(int(int(math.log2(cle_de_alice)/8))+1, byteorder='big'))
					if(verbose):
						print("On envoie alors dans le réseau ce sous-message : ",end='')
						print(chiffre.to_bytes(int(int(math.log2(cle_de_alice))/8)+1, byteorder='big'))




	else:
							#ceci est le processus parent qui recoit les messages
			while (message != "EXIT"):
				nombre_de_sous_message = nouvelle_connexion.recv(4)			# reception du nombre de sous-messages
				if(verbose):
					print("On sait que l'on doit recevoir : ",end='')
					print(nombre_de_sous_message,end='')
					print(" sous-messages")
				nombre_de_sous_message = to_int(nombre_de_sous_message)
				if(verbose):
					print("C'est-à-dire : ",nombre_de_sous_message)
				r = ["" for i in range (0,nombre_de_sous_message)]
				recu = bytes()
				for i in range (0,nombre_de_sous_message):
					r[i] = to_int(nouvelle_connexion.recv(int(int(math.log2(n))/8)+1))
					if(verbose):
						print("On recoit un sous-message chiffré : ",r[i],end="")
					r[i] = to_bytes(lpowmod(r[i],d,n))						# déchiffrement
					if(verbose):
						print(",",end='')
						print(" qui une fois décodé et remis en bytes vaut : ",end='')
						print(r[i])
					recu += r[i]
				if(verbose):
					print("Finalement le message complet encore encodé est : ",end='')
					print(recu)
					print("On décode pour enfin avoir :")
				message = recu.decode()										# conversion utf-8	
				if (message == "(EXIT)"):
					os.kill(pid,9)											# arret du chat
					break
				if (message == "EXIT"):										# arret du chat
					print(bleu+"Alice"+rouge+" a mis fin au chat"+blanc)
					os.kill(pid,9)											# tue le processus fils
					nouvelle_connexion.sendall(len("(EXIT)").to_bytes(4, byteorder='big'))
					chiffre = lpowmod(to_int(bytes("(EXIT)","utf8")),e,cle_de_alice)
					nouvelle_connexion.sendall(chiffre.to_bytes(int(int(math.log2(cle_de_alice))/8)+1, byteorder='big'))
					break
				print(vert,end='')
				print(message,end='')
				print(blanc,end='')
				if ((message != "EXIT")):
					print('\n>',end='')
					nombre_de_sous_message = 0
	ma_chaussette.close()




																		#### Partie CLIENT (ALICE) ####

if(commande == "client"):

					# Initialisation de la connexion au serveur
	print("\nVoulez-vous vous connecter en local ou par ip ? [local/ip]".center(os.get_terminal_size().columns))
	methode = input('>')
	while (( methode != 'ip') & (methode != 'local')):
		print("\nCommande invalide, attendue : ip ou local")
		print("Voulez-vous vous connecter en local ou par ip ? [local/ip]".center(os.get_terminal_size().columns))
		methode = input('>')
	if methode == 'local':
		adresse_serveur = socket.gethostbyname('localhost')
	else:
		print("\nVeuillez saisir l'adresse ip du serveur".center(os.get_terminal_size().columns))
		adresse_serveur = input('>')
	print("\nConnexion au serveur . . .")
	ma_chaussette = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	ma_chaussette.settimeout(10)																							 
	try:																												# tentative de connexion
		ma_chaussette.connect((adresse_serveur,port_serveur))
		erreur = 'no'
	except socket.timeout as e:																							# erreur si la tentative dépasse un certain délai sans réponse
		print((rouge+"Connexion impossible, le serveur ne répond pas (connexion timed out)"+blanc).center(os.get_terminal_size().columns))
		erreur = 'yes'
	if erreur == 'no':
		ma_chaussette.settimeout(None)																					# réglage de la socket en mode bloquer si la connexion a réussie
		print("\nConnexion réussie !")



					# Echange des clés
		print("\nEnvoie de votre clé pubique à "+bleu+"Bob"+blanc+". . .")
		ma_chaussette.sendall(to_bytes(n))
		print("\nEn attente de la clé de "+bleu+"Bob"+blanc+". . .")
		cle_de_bob = to_int(ma_chaussette.recv(1024))
		print("\n")
		print(("Clé publique de "+bleu+"Bob"+blanc+" reçue :").center(os.get_terminal_size().columns))
		print(cle_de_bob,"\n\n\n\n")
		print(("Début du chat avec "+bleu+"Bob"+blanc+", tapez "+rouge+"EXIT"+blanc+" pour un arrêt de la conversation.").center(os.get_terminal_size().columns))
		print("\n")
		message = ""
		pid = os.fork()




		if not pid:
						# ceci est le processus fils qui envoie les messages
			while 1:
				print('>',end='')
				message = input()
				if message == "EXIT":
					print(rouge+"Fin du chat"+blanc)								# arret du chat
				if message == "(EXIT)":
					print(rouge+"mot interdit"+blanc)
				else:
					if(verbose):
						print("message à envoyer : "+message)
					m = split_message(message,cle_de_bob)
					if(verbose):
						print(m)
					ma_chaussette.sendall(len(m).to_bytes(4, byteorder='big'))		# envoie du nombre de sous-messages
					if(verbose):
						print("On envoie le nombre de sous-message : ",len(m))
						print("Qui vaut : ",end='')
						print(len(m).to_bytes(4, byteorder='big'),end='')
						print(" en bytes")
						print("On envoie chaque sous-message après chiffrement")
					for i in m:														# chiffrement et envoie de chaque sous-message
						chiffre = lpowmod(i,e,cle_de_bob)
						ma_chaussette.sendall(chiffre.to_bytes(int(int(math.log2(cle_de_bob))/8)+1, byteorder='big'))
						if(verbose):
							print("On envoie alors dans le réseau ce sous-message : ",end='')
							print(chiffre.to_bytes(int(int(math.log2(cle_de_bob))/8)+1, byteorder='big'))





		else:
						# ceci est le processus parent qui recoit les messages
			while (message != "EXIT"):
				nombre_de_sous_message = ma_chaussette.recv(4)				# reception du nombre de sous-messages
				if(verbose):
					print("On sait que l'on doit recevoir : ",end='')
					print(nombre_de_sous_message,end='')
					print(" sous-messages")
				nombre_de_sous_message = to_int(nombre_de_sous_message)
				if(verbose):
					print("C'est-à-dire : ",nombre_de_sous_message)
				r = ["" for i in range (0,nombre_de_sous_message)]
				recu = bytes()
				for i in range (0,nombre_de_sous_message):
					r[i] = to_int(ma_chaussette.recv(int(int(math.log2(n))/8)+1))
					if(verbose):
						print("On recoit un sous-message chiffré : ",r[i],end="")
					r[i] = to_bytes(lpowmod(r[i],d,n))						# déchiffrement
					if(verbose):
						print(",",end='')
						print(" qui une fois décodé et remis en bytes vaut : ",end='')
						print(r[i])
					recu += r[i]
				if(verbose):
					print("Finalement le message complet encore encodé est : ",end='')
					print(recu)
					print("On décode pour enfin avoir :")
				message = recu.decode()										# conversion utf-8
				if (message == "(EXIT)"):
					os.kill(pid,9)											# arret du chat
					break
				if (message == "EXIT"):										# arret du chat
					print(bleu+"Bob"+rouge+" a mis fin au chat"+blanc)
					os.kill(pid,9)											# tue le processus fils
					ma_chaussette.sendall(len("(EXIT)").to_bytes(4, byteorder='big'))
					chiffre = lpowmod(to_int(bytes("(EXIT)","utf8")),e,cle_de_bob)
					ma_chaussette.sendall(chiffre.to_bytes(int(int(math.log2(cle_de_bob))/8)+1, byteorder='big'))
					break
				print(bleu,end='')
				print(message,end='')
				print(blanc,end='')
				if ((message != "EXIT")):
					nombre_de_sous_message = 0
					print('\n>',end='')
	ma_chaussette.close()
