"""
This is a typical sized, 3x5, slot machine. The game evaluates wins as adjacent positions, rather than line wins. 
This script uses recursion to check adjacent positions and find all of the wins on the screen. 
The final rtp(return to player) is printed to the screen

"""

########### define variables here

iterations = 10000000
ReplacementSymbol = "R1"
NumBaseSchemeStates = 16
WildSymbol = "WW"
BonusSymbol = "B1"

SymbolList = ["M1","M2","M3","M4","F5","F6","F7","F8"]

BonusHitCount = 0 


#######

import pandas as pd
import random as rd

import os
cwd = os.getcwd()

adj_1 = [1,5]
adj_2 = [0,2,6]
adj_3 = [1,3,7]
adj_4 = [2,4,8]
adj_5 = [3,9]
adj_6 = [0,6,10]
adj_7 = [5,1,7,11]
adj_8 = [6,2,8,12]
adj_9 = [3,7,9,13]
adj_10 = [4,8,14]
adj_11 = [5,11]
adj_12 = [10,6,12]
adj_13 = [11,7,13]
adj_14 = [12,8,14]
adj_15 = [9,13]

Adjacents = [adj_1,adj_2,adj_3,adj_4,adj_5,adj_6,adj_7,adj_8,adj_9,adj_10,adj_11,adj_12,adj_13,adj_14,adj_15]

BaseReels = pd.read_csv(cwd + r'\BaseReels.csv',sep = ",")
PayTable = pd.read_csv(cwd + r'\Paytable.csv',sep = ",")

BaseSchemes = pd.read_csv(cwd + r'\BaseSchemes.csv',sep = ",")
BaseSchemeWeight = sum(BaseSchemes.ix[:,15])

def get_stop():

	
	return([rd.randint(0,BaseReels.iloc[:,0].count()-1),
		rd.randint(0,BaseReels.iloc[:,1].count()-1),
		rd.randint(0,BaseReels.iloc[:,2].count()-1),
		rd.randint(0,BaseReels.iloc[:,3].count()-1),
		rd.randint(0,BaseReels.iloc[:,4].count()-1),
		rd.randint(0,BaseReels.iloc[:,5].count()-1),
		rd.randint(0,BaseReels.iloc[:,6].count()-1),
		rd.randint(0,BaseReels.iloc[:,7].count()-1),
		rd.randint(0,BaseReels.iloc[:,8].count()-1),
		rd.randint(0,BaseReels.iloc[:,9].count()-1),
		rd.randint(0,BaseReels.iloc[:,10].count()-1),
		rd.randint(0,BaseReels.iloc[:,11].count()-1),
		rd.randint(0,BaseReels.iloc[:,12].count()-1),
		rd.randint(0,BaseReels.iloc[:,13].count()-1),
		rd.randint(0,BaseReels.iloc[:,14].count()-1)])

def get_symbols(Stop):	
	Window = (BaseReels.iloc[Stop[0],0],
		BaseReels.iloc[Stop[1],1],
		BaseReels.iloc[Stop[2],2],
		BaseReels.iloc[Stop[3],3],
		BaseReels.iloc[Stop[4],4],
		BaseReels.iloc[Stop[5],5],
		BaseReels.iloc[Stop[6],6],
		BaseReels.iloc[Stop[7],7],
		BaseReels.iloc[Stop[8],8],
		BaseReels.iloc[Stop[9],9],
		BaseReels.iloc[Stop[10],10],
		BaseReels.iloc[Stop[11],11],
		BaseReels.iloc[Stop[12],12],
		BaseReels.iloc[Stop[13],13],
		BaseReels.iloc[Stop[14],14])

	
	ReplacementState = rd.randint(0,BaseSchemeWeight-1)	
	for i in range(NumBaseSchemeStates):
		#chooses the 16th column which has the ranges in it		
		if ReplacementState <= BaseSchemes.iloc[i,16]:
			NewSymbolRow = BaseSchemes.ix[i,:]
			#print(i)
			break
			
	
	for i in range(15):
		
		if Window[i] == ReplacementSymbol:
			
			Window = list(Window)
			Window[i] = NewSymbolRow[i]
			
	global BonusHitCount
	if Window[6]== BonusSymbol and Window[7] == BonusSymbol and Window[8] == BonusSymbol:
		BonusHitCount = BonusHitCount + 1

	return[Window,NewSymbolRow[16]/BaseSchemeWeight]
	#return(Window.append(NewSymbolRow[16]))
'''
	for i in range(15):
		if Window[i] == ReplacementSymbol:
			Window[i] = NewSymbolRow[i] 
'''
	 

	

def check_adjacents(InitialPosition, Symbol):
	
	global  SpotsStillToCheck, Adjacent_Positions, Adjacent_Spots,Window
	#InitialPosition = InitialPosition - 1
	
	SpotsStillToCheck.remove(InitialPosition)
	for position in Adjacents[InitialPosition]:
		if position in SpotsStillToCheck:
			SpotsStillToCheck.remove(position)
			
			if Window[position] == Symbol or Window[position] == WildSymbol:
				#print("position" + str(position))
				Adjacent_Spots.append(position)
				
		else:
			next
	
	for adj in Adjacent_Spots:
		
		for pos in Adjacents[adj]:
			
			if pos in SpotsStillToCheck and (Window[pos] == Symbol or Window[pos] == WildSymbol):				
				Adjacent_Spots.append(pos)
				check_adjacents(pos,Symbol)		

			elif pos in SpotsStillToCheck:

				SpotsStillToCheck.remove(pos)		



def get_symbol_pay(Symbol):
	SpotsStillToCheck = list(range(15))
	Adjacent_Spots = []
	for i in range(15):
		check_adjacents(i,Symbol)
		#print(str(len(Adjacent_Spots)) + "length")

#Stop =  [1,5,6,1,1,1,1,2,2,1,2,1,1,2,2]


TotalPay = 0



for iter in range(iterations):
	if iter%100000 == 0:
		print(iter)
	WindowAndProb = get_symbols(get_stop())
	
	#WindowAndProb = get_symbols(Stop)
	Window = WindowAndProb[0]
	StateProb = WindowAndProb[1]

	SpotsStillToCheck = list(range(15))
	Adjacent_Spots = []
	
	SymbolRow = 0
	for Symbol in SymbolList:
		SymbolRow = SymbolRow + 1
		#print(Symbol)
		SpotsStillToCheck = list(range(15))
		Adjacent_Spots = []
		for i in range(15):
			#print(i)
			if i in SpotsStillToCheck:
				#print(str(i) + "i")
				if Window[i] == Symbol or Window[i] == WildSymbol:
					check_adjacents(i,Symbol)					
					if(len(Adjacent_Spots)+ 1) > 3:
						TotalPay = TotalPay + PayTable[str(len(Adjacent_Spots)+1)].iloc[SymbolRow]#*StateProb 

					Adjacent_Spots = []


rtp = float(TotalPay)/iterations/60
print("Totoal Pay = " + str(TotalPay))
print("RTP = %6f" %rtp)
print(str(BonusHitCount) + "bonus hit count")



