##############################################################################
# EVOLIFE  www.dessalles.fr/Evolife                    Jean-Louis Dessalles  #
#            Telecom ParisTech  2013                       www.dessalles.fr  #
##############################################################################

##############################################################################
# Walker                                                                     #
##############################################################################

""" Path finding:
Individuals walk, and paths emerge
"""


import sys
from time import sleep
import random
import cmath
		
sys.path.append('..')
sys.path.append('../../..')
import Evolife.Scenarii.Parameters			as EPar
import Evolife.Ecology.Observer				as EO
import Evolife.Ecology.Individual			as EI
import Evolife.Ecology.Group				as EG
import Evolife.Ecology.Population			as EP
import Evolife.QtGraphics.Evolife_Window	as EW
import Evolife.Tools.Tools					as ET
import Landscapes

print ET.boost()	# significWalkerly accelerates python on some platforms


# two functions to convert from complex numbers into (x,y) coordinates
c2t = lambda c: (int(round(c.real)),int(round(c.imag))) # converts a complex into a couple
t2c = lambda (x,y): complex(x,y) # converts a couple into a complex

#################################################
# Aspect of Walkers and pheromone on display
#################################################
# WalkerAspect = ('black', 6)	
# PheromonAspect = (17, 2)
WalkerAspect = ('white', 1)	
PheromonAspect = ('white', 4)

	
class Walker_Observer(EO.Observer):
	""" Stores global variables for observation
	"""
	def __init__(self, Scenario):
		EO.Observer.__init__(self, Scenario)
		self.CurrentChanges = []	# stores temporary changes
		self.StepId = 0
		self.recordInfo('CurveNames', [(3, 'Year (each Walker moves once a year on average)')])

	def record(self, Info):
		# stores current changes
		# Info is a couple (InfoName, Position) and Position == (x,y)
		self.CurrentChanges.append(Info)

	def get_info(self, Slot):
		" this is called when display is required "
		if Slot == 'PlotOrders':	return [(3, (self.StepId, self.StepId))]	# curve
		#elif Slot == 'PlotOrders':	return [(3, (self.StepId, int(self.Statistics['Food']['average'][0])))]	
		# curve
		else:	return EO.Observer.get_info(self, Slot)
		
	def get_data(self, Slot):
		if Slot == 'Positions':
			CC = self.CurrentChanges
			# print CC
			self.CurrentChanges = []
			return tuple(CC)
		else:	return EO.Observer.get_data(self, Slot)
		
class LandCell(Landscapes.LandCell_3D):
	""" Defines what's in one location on the ground
	"""

	# Cell content is defined as Pheromone
	def __init__(self, InitContent=0):
		self.VoidCell = 0
		self.setContent(InitContent, Record=False)

	def p(self, addendum=0):	
		if addendum:	self.setContent(min(self.Content() + addendum, Gbl.Parameter('Saturation')))
		return self.Content()

	def evaporate(self):
		# Pheromone evaporation should be programmed about here
		Pher = self.p()
		if Pher > 0:
			self.p(-Pher * Gbl.Parameter('Evaporation')/1000.0) # Attractive Pheromone
			if self.p() <= 1:
				self.clean()
				return True
		return False

class Landscape(Landscapes.Landscape_3D):
	""" A 2-D grid with cells that contains food or pheromone
	"""

	def Modify(self, (x,y), Modification):
		self.Ground[x][y] += Modification   # uses addition as redefined in LandCell
		return self.Ground[x][y]

	def pheromone(self, Pos, delta=0):	
		if delta:	self.ActiveCells.append(Pos)
		return self.Cell(Pos).p(delta)	# adds attractive pheromone

	def Altitude(self, Pos):
		return self.Cell(Pos).Altitude
		
	def evaporation(self):
		for Pos in self.ActiveCells.list():
			if self.Cell(Pos).evaporate(): # no pheromone left
				# call 'erase' for updating display when there is no pheromone left
				self.erase(Pos) # for ongoing display
				self.ActiveCells.remove(Pos)

	def erase(self, Pos):
		" says to Observer that there is no pheromone left at that location "
		Observer.record(('P%d_%d' % Pos, Pos + (-3,))) # negative colour means erase from display
		
	def update_(self):
		# scans ground for food and pheromone - May be used for statistics
		Food = []
		Pher = []
		for (Position, Cell) in self.travel():
			if Cell.Pheromone:	Pher.append((Pos, Cell.p()))
		return Pher
	   
	   
class Walker(EI.Individual):
	""" Defines individual agents
	"""
	def __init__(self, Scenario, IdNb, Start=(0,0), Target=(100,100)):
		EI.Individual.__init__(self, Scenario, ID=IdNb)
		self.Start = Start # Starting position
		self.Target = Target
		NoPoints = Gbl.Parameter('NoStartpoints')
		if NoPoints > 1:
			Y = int(IdNb[1:]) % NoPoints
			self.Start = (Start[0], 5 + int(Y * float(Land.Height - 10)/(NoPoints-1)))
			self.Target = (Target[0], Land.Height -5 - int(Y * float(Land.Height - 10)/(NoPoints-1)))
		# print self.Start, self.Target
		self.location = self.Start
		self.Path = []
		self.PreviousPathLength = 0
		self.Deposit = Gbl.Parameter('Deposit')	# quantity of pheromone laid down by the agent
		self.Action = 'Move'	# agents moves toward target, or back home when value is 'BackHome'
		self.moves()

	def Sniff(self):
		" Looks for the next place to go "
		DirectionToTarget = cmath.phase(t2c(self.Target) - t2c(self.location))   # argument 
		DirectionToTarget = ET.noise_add(DirectionToTarget, 0.02*cmath.pi * Gbl.Parameter('Noise'))
		# Distance0 = abs(DirectionToTarget)
		Neighbourhood = Land.neighbours(self.location, Gbl.Parameter('SniffingDistance'))
		random.shuffle(Neighbourhood) # to avoid anisotropy
		acceptable = None
		best = -Gbl.Parameter('Saturation')	# best == pheromone balance found so far
		for NewPos in Neighbourhood:
			if NewPos == self.location: continue
			# Target attractiveness
			Direction = cmath.phase(t2c(NewPos) - t2c(self.location))
			Value = Gbl.Parameter('TargetAttractiveness') * abs(cmath.pi - abs(DirectionToTarget - Direction))
			# looking for position with pheromone
			# attractiveness of pheromone
			Value += Gbl.Parameter('PheromoneAttractiveness') * float(Land.pheromone(NewPos)) / Gbl.Parameter('Saturation')
			# Value += Gbl.Parameter('PheromoneAttractiveness') * (Land.pheromone(NewPos))
			# aversion to climbing
			Value -= Gbl.Parameter('SlopeAversion') * abs(Land.Altitude(NewPos) - Land.Altitude(self.location))
			if Value > best:			  
				acceptable = NewPos
				best = Value
		return acceptable
		
	def pathPurge(self):
		" Eliminates loops from Path "
		NewPath = []
		Positions = []
		for step in self.Path:
			if step[0] in Positions:
				del NewPath[Positions.index(step[0]):]
				del Positions[Positions.index(step[0]):]
			NewPath.append(step)
			Positions.append(step[0])
		self.Path = NewPath
				
	def checkTarget(self):
		" Path are reinforced when target reached "
		if abs(t2c(self.Target) - t2c(self.location)) <= Gbl.Parameter('SniffingDistance'):
			# Target has been reached
			# Computing the quantity of pheromone that will be laid down on the way back home
			self.pathPurge()
			ApparentLength =  len(self.Path)
			ApparentLength +=  Gbl.Parameter('SlopeAversion') * (sum(map(lambda x: x[1], self.Path)))
			ApparentLength +=  Gbl.Parameter('PheromoneAttractiveness') * (sum(map(lambda x: x[2], self.Path)))
			if self.PreviousPathLength == 0:	self.PreviousPathLength = ApparentLength
			if ApparentLength > self.PreviousPathLength:
				self.Deposit = Gbl.Parameter('Deposit')	* (1 - Gbl.Parameter('DepositVariation')/100.0)
			elif ApparentLength < self.PreviousPathLength:
				self.Deposit = Gbl.Parameter('Deposit') * (1 + Gbl.Parameter('DepositVariation')/100.0)
			return True
		return False
			
				
	def moves(self):
		""" Basic behavior: move by looking for neighbouring unvisited cells.
			If food is in sight, return straight back home.
			Lay down negative pheromone on visited cells.
			Lay down positive pheromone on returning home.
		"""
		if self.Path:
			if  self.Action == 'Move' and self.checkTarget():	
				self.Action = 'BackHome'	# agent will move back home
		else:
			self.location = self.Start
			self.Action = 'Move'	# agents moves toward target
		if self.Action == 'BackHome':
			self.location = self.Path.pop()[0]
			Observer.record((self.ID, self.location + WalkerAspect)) # for ongoing display of Walkers
			# marking current positon as interesting with pheromone
			Land.pheromone(self.location, self.Deposit) 
			# ongoing display of positive pheromone
			Observer.record(('P%d_%d' % self.location, self.location + PheromonAspect)) 
		else:
			NextPos = self.Sniff()
			if NextPos is None or random.randint(0,100) < Gbl.Parameter('Exploration'): 
				# either all neighbouring cells have been visited or in the mood for exploration
				E = Gbl.Parameter('SniffingDistance')
				NextPos = c2t(t2c(self.location) + complex(random.randint(-E,E),random.randint(-E,E)))
				NextPos = Land.ToricConversion(NextPos)
			self.Path.append((NextPos, max(0, Land.Altitude(NextPos) - Land.Altitude(self.location)), 
								1*(Land.pheromone(NextPos) < Gbl.Parameter('ForwardThreshold'))))
			self.location = NextPos
			Observer.record((self.ID, self.location + WalkerAspect)) # for ongoing display of Walkers
			# marking current positon as visited with pheromone
			Land.pheromone(self.location, Gbl.Parameter('ForwardDeposit')) 
			Observer.record(('P%d_%d' % self.location, self.location + PheromonAspect)) 


		
class Group(EG.Group):
	# The group is a container for individuals.
	# Individuals are stored in self.members

	def __init__(self, Scenario, Start=(0,0), Target=(100,100), ID=1, Size=100):
		self.Start = Start
		self.Target = Target
		EP.Group.__init__(self, Scenario, ID=ID, Size=Size)
		
	def createIndividual(self, ID=None, Newborn=True):
		# calling local class 'Individual'
		return Walker(self.Scenario, self.free_ID(Prefix='A'), Start=self.Start, Target=self.Target)	# call to local class 'Walker'
					
					
class Population(EP.Population):
	" defines the population of agents "
	
	def __init__(self, Scenario, Observer, Start=(0,0), Target=(100,100)):
		self.Start = Start
		self.Target = Target
		EP.Population.__init__(self, Scenario, Observer)
		" creates a population of Walker agents "
		self.Moves = 0  # counts the number of times agents have moved

	def createGroup(self, ID=0, Size=0):
		return Group(self.Scenario, Start=self.Start, Target=self.Target, ID=ID, Size=Size)	# Call to local class 'Group'
		
	def One_Decision(self):
		""" This function is repeatedly called by the simulation thread.
			One Walker is randomly chosen and decides what it does
		"""
		Walker = self.selectIndividual()
		Walker.moves()
		self.Moves += 1
		Newyear = self.Moves // self.popSize	# One step = all Walkers have moved once on average
		if Newyear > self.year:
			EP.Population.one_year(self)	# performs statistics
			Land.evaporation()
			self.year = Newyear
		return True	 # This value is forwared to "ReturnFromThread"

		
if __name__ == "__main__":
	print __doc__

	#############################
	# Global objects			#
	#############################
	Gbl = EPar.Parameters('_Params.evo')	# Loading global parameter values
	Observer = Walker_Observer(Gbl)   # Observer contains statistics
	Observer.recordInfo('FieldWallpaper', Gbl.Parameter('Ground'))
	# Observer.recordInfo('FieldWallpaper', 'white')
	Observer.recordInfo('DefaultViews', ['Field'])

	Land = Landscape(AltitudeFile=Gbl.Parameter('Altitudes'), CellType=LandCell)
	Startpoint = Gbl.Parameter('Startpoint').split('x')
	Startpoint = ((int(Startpoint[0]) * Land.Width) // 100, (int(Startpoint[1]) * Land.Height) // 100)
	Endpoint = Gbl.Parameter('Endpoint').split('x')
	Endpoint =   ((int(Endpoint[0]) * Land.Width) // 100, (int(Endpoint[1]) * Land.Height) // 100)
	
	Pop = Population(Gbl, Observer, Start=Startpoint, Target=Endpoint)   # Walker colony
	print Land.Width, Land.Height
	Observer.record(('Dummy',(Land.Width, Land.Height, 0, 1)))	# to resize the field
	# Observer.record(('Dummy',(Gbl.Parameter('LandSize'), Gbl.Parameter('LandSize'), 0, 1)))	# to resize the field

	EW.Start(Pop.One_Decision, Observer, Capabilities='RPC')

	print "Bye......."
	sleep(1.0)
##	raw_input("\n[Return]")

__author__ = 'Dessalles'
