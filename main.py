###Documentatia se gaseste la: 
#https://docs.google.com/document/d/1Kii9Zuhu-xd-3et3R0miekLWLHa3NZK-5XqFBupKSCw/edit?usp=sharing

import math
import copy
import sys
import time


#informatii despre un nod din arborele de parcurgere (nu din graful initial)
class NodParcurgere:
	gr=None #trebuie setat sa contina instanta problemei
	def __init__(self, info, parinte, cost=0, h=0):
		self.info=info
		self.parinte=parinte #parintele din arborele de parcurgere
		self.g=cost #consider cost=1 pentru o mutare
		self.h=h
		self.f=self.g+self.h


	def obtineDrum(self):
		l=[self];
		nod=self
		while nod.parinte is not None:
			l.insert(0, nod.parinte)
			nod=nod.parinte
		return l
		
	def afisDrum(self,f,afisCost=False, afisLung=False): #returneaza si lungimea drumului
		l=self.obtineDrum()
		for nod in l:
			if nod.parinte is not None:
				if nod.parinte.info[2]==1:
					mbarca1=self.__class__.gr.malInitial
					mbarca2=self.__class__.gr.malFinal
				else:
					mbarca1=self.__class__.gr.malFinal
					mbarca2=self.__class__.gr.malInitial
				f.write(">>> Barca s-a deplasat de la malul {} la malul {} cu {} canibali si {} misionari cantarind {} kg.\n".format(mbarca1,mbarca2, abs(len(nod.info[0])-len(nod.parinte.info[0])), abs(len(nod.info[1])-len(nod.parinte.info[1])),nod.g-nod.parinte.g))
			f.write(str(nod))
		if afisCost:
			f.write(f"\nCost: {self.g}")
		if afisCost:
			f.write(f"\nNr noduri: {len(l)}")
		return len(l)


	def contineInDrum(self, infoNodNou):
		nodDrum=self
		while nodDrum is not None:
			if(infoNodNou==nodDrum.info):
				return True
			nodDrum=nodDrum.parinte
		
		return False
		
	def __repr__(self):
		sir=""		
		sir+=str(self.info)
		return(sir)


	#euristica banală: daca nu e stare scop, returnez 1, altfel 0

	
	def __str__(self):
		if self.info[2]==1:
			barcaMalInitial="<barca>"
			barcaMalFinal="       "
		else:
			barcaMalInitial="       "
			barcaMalFinal="<barca>"
		return ("Mal: "+ self.gr.malInitial +" Canibali: {} Misionari: {} {}  |||  Mal:"+self.gr.malFinal+" Canibali: {} Misionari: {} {}\n").format(self.info[0], self.info[1],barcaMalInitial, [int(s) for s in self.__class__.gr.greutateCanibali if s not in self.info[0]], [int(s) for s in self.__class__.gr.greutateMisionari if s not in self.info[1]],  barcaMalFinal)
	"""
	def __str__(self):
		return str(self.info)+"\n"

	"""

class Graph: #graful problemei
	def __init__(self, nume_fisier):
		f=open(nume_fisier,"r")
		#citim din fisierul de input si puntem datele intr o lista, fiecare linie va deveni un element
		textFisier=f.read()
		listaInfoFisier=textFisier.splitlines()
		
		self.__class__.N=int(listaInfoFisier[0][2:])
		self.__class__.greutateMisionari=[int(s) for s in listaInfoFisier[1].split(' ')]
		self.__class__.greutateCanibali=[int(s) for s in listaInfoFisier[2].split(' ')]
		self.__class__.M=int(listaInfoFisier[3][2:])
		self.__class__.GMAX=int(listaInfoFisier[4][5:])
		self.__class__.malInitial=listaInfoFisier[5][11:]
		self.__class__.malFinal=listaInfoFisier[6][9:]

		#se fac cateva verificari a datelor de intrare
		if self.__class__.M == 0 or self.__class__.M == 1:
			print("Nu se vor gerera solutii pentru aceste date")
			sys.exit()
		if len(self.__class__.greutateMisionari)!=len(self.__class__.greutateCanibali):
			print("Numarul mis si al can trbuie sa fie la fel")
			sys.exit()

		#a=mini(self.__class__.greutateMisionari)
		#b=mini(self.__class__.greutateCanibali)

		#if self.__class__.GMAX < sum([a[i] for i in range(self.__class__.M)]) or  #self.__class__.GMAX< sum([b[i] for i in range(self.__class__.M)]):
		#	print("Nu se vor gerera solutii pentru aceste date")
		#	sys.exit()
		

		self.start=(self.__class__.greutateCanibali,self.__class__.greutateMisionari,1) #informatia nodului de start
		self.scopuri=[([],[],0)]
		#info despre starea finala

	#functia care testeaza daca s-a ajuns in starea finala
	def testeaza_scop(self, nodCurent):
			return nodCurent.info in self.scopuri;


  #"""Orodneaza o lista "vector" de nr_elemente crescator si returneaza noua lista ca rez
	#arg: vector (list of int), nr_elemente (int)
	#returns: rez(list of int)
	#atrib:min (int)- min in array, nr_elemente(int)"""

	def mini(vector,nr_elemente):
			vector_copy = copy.deepcopy(vector)
			rez=[]
			while nr_elemente>0:
				mim=min(vector_copy)
				rez.append(mim)
				nr_elemente-=1
			return rez



	#functia de generare a succesorilor
	def genereazaSuccesori(self, nodCurent,tip_euristica="euristica banala"):

		def test_conditie(mis, can):
			return mis==0 or mis>=can
		
		

		listaSuccesori=[]
		#nodCurent.info va contine un triplet (greutati_C, greutati_M,barca)
		barca=nodCurent.info[2]

		if barca==1:
			canMalCurent=nodCurent.info[0]
			misMalCurent=nodCurent.info[1]
			#presupannad ca toti cantaresc diferit 
			canMalOpus=[int(s) for s in Graph.greutateCanibali if s not in canMalCurent]
			misMalOpus=[int(s) for s in Graph.greutateMisionari if s not in misMalCurent]
		else:
			canMalOpus=nodCurent.info[0]
			misMalOpus=nodCurent.info[1]
			canMalCurent=[int(s) for s in Graph.greutateCanibali if s not in canMalOpus]
			misMalCurent=[int(s) for s in Graph.greutateMisionari if s not in misMalOpus]

		maxMisionariBarca=min(Graph.M, len(misMalCurent))
		#nr de misionari maxim de misionari care pot pleca cu parca

		for misBarca in range(maxMisionariBarca+1):
			if misBarca==0: #daca nu se afla niciun misionar in barca
				maxCanibaliBarca=min(Graph.M, len(canMalCurent))#nr max de canibali care pot pleca este acesta
				minCanibaliBarca=1#cum barca nu poate pleca goala (aici se poate chiar 2 fiindca este inutil sa plece barca cu o singura persoana)
			else:
				maxCanibaliBarca=min(Graph.M-misBarca, len(canMalCurent), misBarca)# daca se afla misionari in barca atunci nr maxim de canibali care pot exista in barca va fi ales astfel incat pe mal sa nu ramana mai multi decat mis, in barca la fel si nici sa depasim nr de locuri din barca
				minCanibaliBarca=0
		
			for canBarca in range(minCanibaliBarca, maxCanibaliBarca+1):
				#consideram mal curent nou ca fiind acelasi mal de pe care a plecat barca
				#Pentru fiecare nr de misionar care pot pleca luam fiecare canibal care poate pleca (respecta reguluile impuse mai sus) si vom crea vectori noi pt can, mis de pe malul nou, cat si pt cei care au ramas pe malul vechi 
				#canMalCurentNou=canMalCurent-canBarca
				canMalCurentNou=[int(s) for i,s in enumerate(canMalCurent) if i+1<=(len(canMalCurent)-canBarca)]
				#misMalCurentNou=misMalCurent-misBarca
				misMalCurentNou=[int(s) for i,s in enumerate(misMalCurent) if i+1<=(len(misMalCurent)-misBarca)]
				#canMalOpusNou=canMalOpus+canBarca
				canMalOpusNou=copy.deepcopy(canMalOpus)
				canInBarca=[int(s) for i,s in enumerate(canMalCurent) if i+1>len(canMalCurent)-canBarca]
				canMalOpusNou+=canInBarca
				#misMalOpusNou=misMalOpus+misBarca
				misMalOpusNou=copy.deepcopy(misMalOpus)
				misInBarca=[int(s) for i,s in enumerate(misMalCurent) if i+1>(len(misMalCurent)-misBarca)]
				misMalOpusNou+=misInBarca
					
				#greutatea celor din barca
				greutateBarca=sum(canInBarca)+sum(misInBarca)
				#daca aceasta depaseste GMAX dat se trece la urmatoarea iteratie
				if greutateBarca>Graph.GMAX:
					continue
				#daca nu sunt respectate conditiile privind nr_mis>=can la orice moment se trece la urmatoarea iteratie
				if not test_conditie(len(misMalCurentNou),len(canMalCurentNou)):
					continue
				if not test_conditie(len(misMalOpusNou),len(canMalOpusNou)):
					continue	
				if barca==1: #testul este pentru barca nodului curent (parinte) deci inainte de mutare
					infoNodNou= (canMalCurentNou,misMalCurentNou, 0)	
				else:				
					infoNodNou= (canMalOpusNou,misMalOpusNou, 1)

				#se verifica daca nodul curent este deja continut, daca nu este se adauga la lista de succesori
				if not nodCurent.contineInDrum(infoNodNou):
					costSuccesor=greutateBarca
					listaSuccesori.append(NodParcurgere(infoNodNou,nodCurent,cost=nodCurent.g+costSuccesor, h=NodParcurgere.gr.calculeaza_h(infoNodNou, tip_euristica)))

		return listaSuccesori

		"""for misBarca in range(maxMisionariBarca+1):
			if misBarca==0:
				maxCanibaliBarca=min(Graph.M, len(canMalCurent))
				minCanibaliBarca=1
			else:
				maxCanibaliBarca=min(Graph.M-misBarca, len(canMalCurent), misBarca)
				minCanibaliBarca=0

			misInBarca = mini(misMalCurent,misBarca)
			misMalCurentNou = [int(s) for s in misMalCurent if s not in misInBarca]
			misMalOpusNou=copy.deepcopy(misMalOpus)
			misMalOpusNou+=misInBarca

			for canBarca in range(minCanibaliBarca, maxCanibaliBarca+1):
				#consideram mal curent nou ca fiind acelasi mal de pe care a plecat barca
				#canMalCurentNou=canMalCurent-canBarca
				canInBarca = mini(canMalCurent,canBarca)
				#canMalCurentNou=[int(s) for i,s in enumerate(canMalCurent) if i+1<=(len(canMalCurent)-canBarca)]
				canMalCurentNou = [int(s) for s in canMalCurent if s not in canInBarca ]
				#misMalCurentNou=misMalCurent-misBarca
				#misMalCurentNou=[int(s) for i,s in enumerate(misMalCurent) if i+1<=(len(misMalCurent)-misBarca)]
				#canMalOpusNou=canMalOpus+canBarca
				canMalOpusNou=copy.deepcopy(canMalOpus)
				canMalOpusNou+=canInBarca
				#misMalOpusNou=misMalOpus+misBarca
				#misMalOpusNou=copy.deepcopy(misMalOpus)
				#misInBarca=[int(s) for i,s in enumerate(misMalCurent) if i+1>(len(misMalCurent)-misBarca)]
				#misMalOpusNou+=misInBarca
					
				greutateBarca=sum(canInBarca)+sum(misInBarca)

				if greutateBarca>Graph.GMAX:
					continue
				if not test_conditie(len(misMalCurentNou),len(canMalCurentNou)):
					continue
				if not test_conditie(len(misMalOpusNou),len(canMalOpusNou)):
					continue	
				if barca==1: #testul este pentru barca nodului curent (parinte) deci inainte de mutare
					infoNodNou= (canMalCurentNou,misMalCurentNou, 0)	
				else:				
					infoNodNou= (canMalOpusNou,misMalOpusNou, 1)

				if not nodCurent.contineInDrum(infoNodNou):
					costSuccesor=greutateBarca
					listaSuccesori.append(NodParcurgere(infoNodNou,nodCurent,cost=nodCurent.g+costSuccesor, h=NodParcurgere.gr.calculeaza_h(infoNodNou, tip_euristica)))
					 
		return listaSuccesori"""

	""""
	for misBarca in range(maxMisionariBarca+1):
			if misBarca==0:
				maxCanibaliBarca=min(Graph.M, len(canMalCurent))
				minCanibaliBarca=2
			else:
				maxCanibaliBarca=min(Graph.M-misBarca, len(canMalCurent), misBarca)
				minCanibaliBarca=0
			
			M=list(combinations(misMalCurent,misBarca))

			for canBarca in range(minCanibaliBarca, maxCanibaliBarca+1):
				#consideram mal curent nou ca fiind acelasi mal de pe care a plecat barca
				C=list(combinations(canMalCurent,canBarca))
				#print(f"M: {M} C: {C}")
				for j in range(len(M)):
					if sum(M[j])>Graph.GMAX:
						continue
					for k in range(len(C)):
						greutateBarca=sum(C[k])+sum(M[j])
						if greutateBarca>Graph.GMAX:
							continue
						canMalCurentNou=[int(s) for s in canMalCurent if s not in C[k]]
						misMalCurentNou=[int(s) for s in misMalCurent if s not in M[j]]
						if not test_conditie(len(misMalCurentNou),len(canMalCurentNou)):
							continue
						canMalOpusNou=copy.deepcopy(canMalOpus)
						canMalOpusNou+=C[k]
						misMalOpusNou=copy.deepcopy(misMalOpus)
						misMalOpusNou+=M[j]
						if not test_conditie(len(misMalOpusNou),len(canMalOpusNou)):
								continue
						#print(f"can {canMalCurentNou} mis {misMalCurentNou} v si can{canMalOpusNou} mis{misMalOpusNou} e")
						if barca==1: #testul este pentru barca nodului curent (parinte) deci inainte de mutare
							infoNodNou= (canMalCurentNou,misMalCurentNou, 0)	
						else:				
							infoNodNou= (canMalOpusNou,misMalOpusNou, 1)

						if not nodCurent.contineInDrum(infoNodNou):
							#print(listaSuccesori)
							costSuccesor=greutateBarca
							listaSuccesori.append(NodParcurgere(infoNodNou,nodCurent,cost=nodCurent.g+costSuccesor, h=NodParcurgere.gr.calculeaza_h(infoNodNou, tip_euristica))) 
"""


	#va genera succesorii sub forma de noduri in arborele de parcurgere	
	#aceasta este o functie mai eficienta de generare a succesorilor, care genereaza direct perechiile valide de numere de canibali si misionari care trec raul (respectand conditia problemei atat pe maluri cat si in barca; deci nu se mai genereaza acele perechi pe care le eliminam apoi pentru ca nu indeplineau conditia)


	# euristica banala
	def calculeaza_h(self, infoNod, tip_euristica="euristica banala"):
		if tip_euristica=="euristica banala":
			if infoNod not in self.scopuri:
				return 1
			return 0			
		if tip_euristica=="euristica admisibila 1":
			#calculez cati oameni mai am de mutat si impart la nr de locuri in barca
			#totalOameniDeMutat=infoNod[0]+infoNod[1]
			return 2*math.ceil((len(infoNod[0])+len(infoNod[1]))/self.M)+(1-infoNod[2])-1 #(1-infoNod[2]) vine de la faptul ca daca barca e pe malul final trebuie sa mai faca o trecere spre malul initial ca sa ii ia pe oameni, pe cand daca e deja pe malul initial, nu se mai aduna acel 1
		if tip_euristica=="euristica admisibila 2":
			return math.ceil((sum(infoNod[0])+sum(infoNod[1]))/self.GMAX)

		if tip_euristica=="euristica neadmisibila":
			cat=infoNod[0]+infoNod[1]
			cat+=[0,1]
			return math.ceil(max(cat)*len(cat)/self.GMAX) 

		"""if tip_euristica=="euristica neadmisibila":
			if infoNod[0] is None and infoNod[1] is not None:
				return 2*math.ceil((len(infoNod[1])*max(infoNod[1]))/self.GMAX)
			if  infoNod [1] is None and infoNod[0] is not None:
				return 2*math.ceil((len(infoNod[1])*max(infoNod[1]))/self.GMAX)
			if infoNod [1] is None and infoNod[0] is None:
				return 0
			return 2*math.ceil((len(infoNod[0])*max(infoNod[0])+len(infoNod[1])*max(infoNod[1]))/self.GMAX)"""

			


	def __repr__(self):
		sir=""
		for (k,v) in self.__dict__.items() :
			sir+="{} = {}\n".format(k,v)
		return(sir)
		
################################################
#                    A*                        #
################################################

def a_star(gr, nrSolutiiCautate, tip_euristica, nume_f):
	#in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
	c=[NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
	f=open(nume_f,'w')
	f.write("\n\n##################\nSolutii obtinute cu A*:\n\n")
	t_inainte=int(round(time.time()*1000))
	#time.sleep(1)
	t_dupa=int(round(time.time()*1000))
	while len(c)>0:
		nodCurent=c.pop(0)
		if(t_dupa-t_inainte>timeout):
			print("S-a depasit timpul de executie de "+str(timeout)+"milisecunte")
			sys.exit()

		if gr.testeaza_scop(nodCurent):
			
			f.write("Solutie: \n")
			nodCurent.afisDrum(f,afisCost=True, afisLung=True)
			t_dupa=int(round(time.time() * 1000))
			f.write('\nTimpul: '+str(t_dupa-t_inainte)+' milisecunde')
			f.write("\n----------------\n")
			#input()
			nrSolutiiCautate-=1
			if nrSolutiiCautate==0:
				return
		lSuccesori=gr.genereazaSuccesori(nodCurent,tip_euristica=tip_euristica)	
		for s in lSuccesori:
			i=0
			gasit_loc=False
			for i in range(len(c)):
				#diferenta fata de UCS e ca ordonez dupa f
				if c[i].f>=s.f :
					gasit_loc=True
					break;
			if gasit_loc:
				c.insert(i,s)
			else:
				c.append(s)

	#f.write("heeeeeeeeeeeeei")  
	#t_dupa=int(round(time.time() * 1000))
	#f.write(str(t_dupa-t_inainte))
	f.close()



################################################
#                   UCS                        #
################################################

def uniform_cost(gr, nrSolutiiCautate, tip_euristica, nume_f):
	#in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
	c=[NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
	f=open(nume_f,'w')
	f.write("\n\n##################\nSolutii obtinute cu UCS:\n\n")
	
	while len(c)>0:
		#print("Coada actuala: " + str(c))
		#input()
		nodCurent=c.pop(0)
		
		if gr.testeaza_scop(nodCurent):
			f.write("Solutie: \n")
			nodCurent.afisDrum(f,afisCost=True, afisLung=True)
			f.write("\n----------------\n")
			nrSolutiiCautate-=1
			if nrSolutiiCautate==0:
				return
		lSuccesori=gr.genereazaSuccesori(nodCurent,tip_euristica=tip_euristica)	
		for s in lSuccesori:
			i=0
			gasit_loc=False
			for i in range(len(c)):
				#ordonez dupa cost(notat cu g aici și în desenele de pe site)
				if c[i].g>s.g :
					gasit_loc=True
					break
			if gasit_loc:
				c.insert(i,s)
			else:
				c.append(s)
	f.close()		

################################################
#             A* optimizat                    #
################################################

def a_star_optimizat(gr,tip_euristica,nume_f):
	#in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
	l_open=[NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
	f=open(nume_f,'w')
	f.write("\n\n##################\nSolutii obtinute cu A* optimizat:\n\n")
	#l_open contine nodurile candidate pentru expandare

	#l_closed contine nodurile expandate
	l_closed=[]
	while len(l_open)>0:
		#print("Coada actuala: " + str(l_open))
		#input()
		nodCurent=l_open.pop(0)
		l_closed.append(nodCurent)
		if gr.testeaza_scop(nodCurent):
			f.write("Solutie: \n")
			nodCurent.afisDrum(f,afisCost=True, afisLung=True)
			f.write("\n----------------\n")
			return
		lSuccesori=gr.genereazaSuccesori(nodCurent)	
		for s in lSuccesori:
			gasitC=False
			for nodC in l_open:
				if s.info==nodC.info:
					gasitC=True
					if s.f>=nodC.f:
						lSuccesori.remove(s)
					else:#s.f<nodC.f
						l_open.remove(nodC)
					break
			if not gasitC:
				for nodC in l_closed:
					if s.info==nodC.info:
						if s.f>=nodC.f:
							lSuccesori.remove(s)
						else:#s.f<nodC.f
							l_closed.remove(nodC)
						break
		for s in lSuccesori:
			i=0
			gasit_loc=False
			for i in range(len(l_open)):
				#diferenta fata de UCS e ca ordonez crescator dupa f
				#daca f-urile sunt egale ordonez descrescator dupa g
				if l_open[i].f>s.f or (l_open[i].f==s.f and l_open[i].g<=s.g) :
					gasit_loc=True
					break
			if gasit_loc:
				l_open.insert(i,s)
			else:
				l_open.append(s)
	f.close()
					

################################################
#             IDA*                             #
################################################

def ida_star(gr, nrSolutiiCautate,tip_euristica,nume_f):
	
	nodStart=NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))
	limita=nodStart.f
	f=open(nume_f,'w')
	f.write("\n\n##################\nSolutii obtinute cu IDA*:\n\n")
	while True:

		f.write(f"Limita de pornire: {limita}")
		nrSolutiiCautate, rez= construieste_drum(gr, nodStart,limita,nrSolutiiCautate,tip_euristica,f)
		if rez=="gata":
			break
		if rez==float('inf'):
			f.wrtie("Nu exista solutii!")
			break
		limita=rez
		f.write(f"\n>>> Limita noua: {limita}")
	f.close()
def construieste_drum(gr, nodCurent, limita, nrSolutiiCautate,tip_euristica,f):
	f.write(f"A ajuns la: {nodCurent}")
	if nodCurent.f>limita:
		return nrSolutiiCautate, nodCurent.f
	if gr.testeaza_scop(nodCurent) and nodCurent.f==limita :
		f.write("Solutie: ")
		nodCurent.afisDrum(f)
		f.write(limita)
		f.write("\n----------------\n")
		#input()
		f.write()
		nrSolutiiCautate-=1
		if nrSolutiiCautate==0:
			return 0,"gata"
	lSuccesori=gr.genereazaSuccesori(nodCurent,tip_euristica)	
	minim=float('inf')
	for s in lSuccesori:
		nrSolutiiCautate, rez=construieste_drum(gr, s, limita, nrSolutiiCautate,tip_euristica,f)
		if rez=="gata":
			return 0,"gata"
		f.write(f"\nCompara {rez} cu {minim}")
		if rez<minim:
			minim=rez
			f.write(f"\nNoul minim: {minim}")
	return nrSolutiiCautate, minim


		
									
				


print("Introduceti calea catre folder input: ")
stringInput = str(input())
print("Introduceti calea catre folder output: ")
stringOutput=str(input())

print("Introduceti nr de solitii cautate: ")
nrSolutiiCautate=int(input())
print("Introduceti in secunde timpul de timeout")
timeout=int(input())

"""stringInput="inputs/date1.txt"
stringOutput="output"
nrSolutiiCautate=2"""
gr=Graph(stringInput)				
NodParcurgere.gr=gr
i=1



a_star(gr, nrSolutiiCautate,tip_euristica="euristica banala", nume_f=stringOutput+str(i)+".txt")
i+=1
a_star(gr, nrSolutiiCautate,tip_euristica="euristica admisibila 1", nume_f=stringOutput+str(i)+".txt")
i+=1
a_star(gr, nrSolutiiCautate,tip_euristica="euristica admisibila 2", nume_f=stringOutput+str(i)+".txt")
i+=1
a_star(gr, nrSolutiiCautate,tip_euristica="euristica neadmisibila", nume_f=stringOutput+str(i)+".txt")
i+=1

uniform_cost(gr,nrSolutiiCautate,tip_euristica="euristica admisibila 1",nume_f=stringOutput+str(i)+".txt")
i+=1

a_star_optimizat(gr,tip_euristica="euristica banala",nume_f=stringOutput+str(i)+".txt")
i+=1
a_star_optimizat(gr,tip_euristica="euristica admisibila 1",nume_f=stringOutput+str(i)+".txt")
i+=1
a_star_optimizat(gr,tip_euristica="euristica admisibila 2",nume_f=stringOutput+str(i)+".txt")
i+=1
a_star_optimizat(gr,tip_euristica="euristica neadmisibila",nume_f=stringOutput+str(i)+".txt")
#i+=1

#ida_star(gr,nrSolutiiCautate,tip_euristica="euristica banala",nume_f=stringOutput+str(i)+".txt")
#i+=1
#ida_star(gr,nrSolutiiCautate,tip_euristica="euristica admisibila 1",nume_f=stringOutput+str(i)+".txt")
#i+=1
#ida_star(gr,nrSolutiiCautate,tip_euristica="euristica admisibila 2",nume_f=stringOutput+str(i)+".txt")
#i+=1
#ida_star(gr,nrSolutiiCautate,tip_euristica="euristica neadmisibila",nume_f=stringOutput+str(i)+".txt")