##############################################################################
# EVOLIFE  www.dessalles.fr/Evolife                    Jean-Louis Dessalles  #
#            Telecom ParisTech  2013                       www.dessalles.fr  #
##############################################################################


##############################################################################
#  Tools                                                                     #
##############################################################################

""" EVOLIFE: Module Tools: various functions """

import re
import random
import time
from math import floor, modf, log

try:
	import EvolifeGray # gray code
	GrayTable = EvolifeGray.GrayCode() # pre-computes a Gray code into a table for rapid acess
except ImportError:
	pass



def decrease(x,M,Selection):
	""" Computes a decreasing function of x in [0,M] which sums to 1 
		1/(x+a) normalized for x in [0,1] """
	def one_value(x):
		if x >= 0:
			return 1.0/(x+(1.0*M)/Selection) / log(1+Selection)
		else:
			error('Tools: decrease called with negative value')
	if M:
		if Selection:
			return (one_value(x) + one_value(x+1))/2
		else:
			return 1.0/M
	else:
		return 0

def chances(proba, N):
	" computes what one gets from a maximum of N with probability proba "
	C = N * proba
	if random.random() < modf(C)[0]:	# modf(3.14) == (0.14, 3.0) ;  modf(3.14)[0] ==  0.14
		return int(C) + 1
	return int(C)

def percent(x):
	return float(x) / 100

def noise_mult(x, range_):
	""" returns x affected by a multiplicative uniform noise
		between 1-range_/100 and 1+range_/100
	"""
	if (range_ > 100):
			error("Tools: noise amplitude",str(range_))
	return x * (1.0 + percent((2 * random.random() - 1) * range_))

def noise_add(x, range_):
	""" returns x affected by an additive uniform noise
		between -range_ and range_
	"""
	return x + ((2 * random.random() - 1) * range_)

def transpose(Matrix):
	' groups ith items in each list of Matrix '
	#This genial version is much too slow
	#return reduce(lambda x, y: map(lambda u,v: u+v,x,y),
	#	   [map(lambda x: [x],L) for L in Matrix])
	if Matrix == []:
		return []
	Result = [[0] * len(Matrix) for x in range(len(Matrix[0]))]			 
	for ii in range(len(Matrix)):
		for jj in range(len(Matrix[ii])):
			Result[jj][ii] = Matrix[ii][jj]
	return Result

def Nb2A(Nb):
	" converts a number into letters - Useful to list files in correct order "
	A = chr(ord('a') + Nb // 676)
	A += chr(ord('a')+ (Nb % 676) // 26)
	A += chr(ord('a')+ Nb % 26)
	return A

def Nb2A0(Nb):
	" converts a number into a padded string "
	return ("000000" + str(Nb))[-6:]

def ChildrenSlide(x, Start, Low, High, Slope):
	" computes a two-slope function between 0 and 1 "
	#		H----
	#	   /
	#	  /
	#  ---L
	def middle(x):
		return Slope*x+0.5*(1-Slope) # line passing through (0.5,0.5)

	if x < Low:
		return ((x-Start) * middle(Start)) / (Low - Start)
	if x > High:
		return middle(High) + ((x-High) * (1-middle(High))) / (1-High)
	return middle(x)
		
def FileAnalysis(FileName, Pattern, Flag=re.M):
	""" Analyses the content of a file and returns all matching occurrences of Pattern
	"""
	Filin = open(FileName,"r")
	FContent = Filin.read() + '\n'
	Filin.close()
	R = re.findall(Pattern,FContent,flags=Flag) # default: Multiline analysis
	return R

def List2File(L, FileName):
	""" Saves a list of strings into a file
	"""
	Filout = open(FileName, "w")
	Filout.write('\n'.join(L))
	Filout.close()

class EvolifeError(Exception):
	def __init__(self, Origine, Msg):
		self.Origine = Origine
		self.Message = Msg
	def __repr__(self):
		return('%s: %s' % (self.Origine, Explanation))
		
def error(ErrMsg, Explanation=''):
	print "\n\n******** ERROR ************"
	print ErrMsg
	if Explanation:
		print Explanation
	print "************ ERROR ********\n"
	#raw_input('Press [Return] to exit')
	time.sleep(5)
	raise EvolifeError(ErrMsg, Explanation)

class LimitedMemory(object):
	"   memory buffer with limited length  "

	def __init__(self, MaxLength):
		self.past = []
		self.MaxLength = MaxLength

	def Length(self): return len(self.past)
	
	def push(self, Item):
		self.past = self.past[-self.MaxLength+1:]
		self.past.append(Item)

	def retrieve(self): return self.past

	def last(self):
		if self.past != []: return self.past[-1]
		return None

	def pull(self):
		if self.past != []: return self.past.pop()
		return None
		
	def __repr__(self):
		return ' '.join(["(%0.1f, %0.1f)" % It for It in self.past])

#########
# Boost #
#########

def boost():
	# A technical trick - look at http://psyco.sourceforge.net/
	#(somewhat magical, but sometimes provides impressive speeding up)
	try:
	##	psyco.profile()
		import os.path
		if os.path.exists('/usr/local/lib/python/site-packages'):
			import sys
			sys.path.append('/usr/local/lib/python/site-packages/')
		#from psyco.classes import *
		import psyco
		UsePsyco = True
		psyco.full()
	except ImportError:
		UsePsyco = False

	return "Boosting with Psyco : %s" % UsePsyco




if __name__ == "__main__":
	# putting Evolife into the path (supposing we are in the same directory tree)
	import sys
	import os 
	import os.path

	for R in os.walk(os.path.abspath('.')[0:os.path.abspath('.').find('Evo')]):
		if os.path.exists(os.path.join(R[0],'Evolife','__init__.py')):
			sys.path.append(R[0])
			break
	
##    EvolifePath = os.path.abspath('.')[0:os.path.abspath('.').find('Evolife')+7]
##    sys.path += [D[0] for D in os.walk(EvolifePath) if 'Evolife' in D[1] ]

	from Evolife.Scenarii.Parameters import Parameters
	P = Parameters('../Evolife.evo')
	print __doc__
	M= 20
	S = P.Parameter('Selectivity')
	print "selectivity = ", int(S)
	print [ (x,decrease(x,M,S)) for x in range(M)]
	print sum([decrease(x,M,S) for x in range(M)])
	print [ int(chances(decrease(x,M,S),24)) for x in range(M)]
	raw_input('[Return]')
	





__author__ = 'Dessalles'
