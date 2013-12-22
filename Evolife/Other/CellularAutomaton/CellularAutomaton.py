##############################################################################
# EVOLIFE  www.dessalles.fr/Evolife                    Jean-Louis Dessalles  #
#            Telecom ParisTech  2013                       www.dessalles.fr  #
##############################################################################


""" Cellular Automaton:


"""

import sys
sys.path.append('../../..')

import Evolife.Ecology.Observer as EO
import Evolife.QtGraphics.Evolife_Window as EW
import Evolife.Tools.Tools as ET
import Evolife.Scenarii.Parameters as EPar

print ET.boost()   # A technical trick that sometimes provides impressive speeding up

	
import random

class Rule:
	" defines all possible automaton rules "
	def __init__(self, RuleNumber):
		" convert the rule number into a list of bits "
		# For each configuration number (3-bit for three-cell neighbourhood --> 8 configurations), 
		# the rule gives the new binary state of the cell.
		# Attention: the following line is only valid for 8 configurations
		self.Rule = [int(b) for b in list(bin(RuleNumber)[2:].rjust(8,'0'))]
		# example: rule 32 --> 00100000
		self.Rule.reverse()
		# example: rule 32 --> 00000100
		# only the 5th configuration: '101', allows the next state to be 1.
		# if this configuation is absent at the beginning, an all-0 state emerges.
		print 'Rule {0}: {1}'.format(RuleNumber, self.Rule)
	
	def Next(self, Left, Middle, Right):
		try:
			return self.Rule[(Left << 2) + (Middle << 1) + Right]
		except IndexError:
			print 'Rule Error: unknown environment {0}{0}{0}'.format(Left,Middle,Right)
			return None
		

class CA_Scenario(EPar.Parameters):

	def __init__(self, ConfigFile):
		# Parameter values
		EPar.Parameters.__init__(self, ConfigFile)
		#############################
		# Global variables			#
		#############################
		self.Colours = ['red', 'yellow']	# corresponds to Evolife colours
		self.Rule = Rule(self.Parameter('Rule'))



# en envoyant des coordonnees (sans noms d'agents) en Layout, 
# on obtient un simple dessin des points en tant que courbe

	
class CA_Observer(EO.Experiment_Observer):
	""" Stores parameters and observation data
	"""
	def __init__(self, Scenario):
		EO.Experiment_Observer.__init__(self, Scenario) # stores global information
		Dim = Scenario.Parameter('CASize')	# Logical size of the grid
		Depth= Scenario.Parameter('TimeLimit')
		self.CurrentChanges = [(0,0,0),(0,Depth,0),(Dim,0,0),(Dim,Depth,0)]	# stores temporary changes
		self.recordInfo('DefaultViews', ['Field'])

	def record(self, Info):
		# stores current changes
		# Info is a couple (InfoName, Position) and Position == (x,y)
		self.CurrentChanges.append(Info)

	def get_data(self, Slot):
		if Slot == 'Positions':
			CC = self.CurrentChanges
			self.CurrentChanges = []
			return tuple(CC)
		return None

class Cell:
	""" Defines what's in one location on the ground
	"""
	def __init__(self, Position, State=None):
		self.Position = Position
		self.CurrentState = State	
		self.NextState = State	# Avoids mixing time steps during computation

	def content(self):
		return self.CurrentState

	def setContent(self, State):
		self.NextState = State
		return State
	
	def update(self):
		self.CurrentState = self.NextState

class Automaton:
	"""	A 1-D grid that represents the current state of the automaton
	"""
	def __init__(self, Scenario):
		self.Size = Scenario.Parameter('CASize')
		self.Ground = [Cell(x,0) for x in range(self.Size)]
		self.Ground[self.Size//2].setContent(1)	# The middle cell is set to 1
		self.VPosition = 1	# Vertical position in display
		self.display()
		

	def ToricConversion(self, x):
		# circular row
		return x % self.Size

	def Content(self, x):
		" binary state inferred from colour "
		return self.Ground[x].content()

	def display(self):
		for C in self.Ground:
			C.update()
			Depth= Scenario.Parameter('TimeLimit')
			# Cells are displayed as blobs: (x, y, colour, blobsize)
			Observer.record((C.Position, (-self.VPosition) % Depth, Scenario.Colours[C.content()], 2))

	def EvolveCell(self, Cell):
		x= Cell.Position
		Area = map(self.ToricConversion, [x-1, x, x+1])
		# print Area,
		Neighbourhood = map(self.Content, Area)
		# print Neighbourhood,
		NewState = Scenario.Rule.Next(*Neighbourhood)
		return Cell.setContent(NewState)
	
	def OneStep(self):
		Observer.season()	# One step = one agent has moved
		self.display()
		if self.VPosition < Scenario.Parameter('TimeLimit'):
			for C in self.Ground:
				NewState = self.EvolveCell(C)
			self.VPosition += 1
			return True
		return False
		
	
if __name__ == "__main__":
	print __doc__

	
	#############################
	# Global objects			#
	#############################
	Scenario = CA_Scenario('_Params.evo')
	Observer = CA_Observer(Scenario)	  # Observer contains statistics
	CAutomaton = Automaton(Scenario)	  # logical settlement grid
	
	
	EW.Start(CAutomaton.OneStep, Observer, Capabilities='FP')


	print "Bye......."
	


__author__ = 'Dessalles'
