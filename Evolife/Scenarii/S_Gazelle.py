##############################################################################
# EVOLIFE  www.dessalles.fr/Evolife                    Jean-Louis Dessalles  #
#            Telecom ParisTech  2013                       www.dessalles.fr  #
##############################################################################



""" EVOLIFE: Gazelle Scenario

Imagine two species, call them gazelles and lions. Gazelles have the genetically choice to invest energy in jumping vertically when lions approach. Of course, this somewhat reduces their ability to run away in case of pursuit. If lions prefer to chase non jumping gazelles, and poorly jumping ones among those who are jumping, show that investment in jumping evolves, at least for healthy individuals.	

	http://icc.enst.fr/IC/Intranet/projects/P08111502.html 

"""

	#=============================================================#
	#  HOW TO MODIFY A SCENARIO: read Default_Scenario.py		 #
	#=============================================================#

import random

import sys
if __name__ == '__main__':  sys.path.append('../..')  # for tests

from Evolife.Scenarii.Default_Scenario import Default_Scenario
from Evolife.Tools.Tools import error, noise_add, percent


######################################
# specific variables and functions   #
######################################


class Scenario(Default_Scenario):

	######################################
	# All functions in Default_Scenario  #
	# can be overloaded				  #
	######################################


	
	def genemap(self):
		""" Defines the name of genes and their position on the DNA.
			(see Genetic_map.py)
		"""
		return [('GazelleSignal', 8), ('LionSensitivityToSignal', 8)] 	

	def phenemap(self):
		""" Defines the set of non inheritable characteristics
		"""
		# Elements in phenemap are integers between 0 and 100 and are initialized randomly
		# Lions and gazelles belong to the same species (!)
		# Their nature is decided at birth by the Phene 'Lion'
		return ['Lion', 'GazelleStrength']

	def gazelle(self, indiv):
		if indiv:
			return indiv.Phene_value('Lion') < self.Parameter('GazelleToLionRatio')	# typically more gazelles than lions 
		return False
	
	def strongGazelle(self, gazelle):
		if not self.gazelle(gazelle):	error("Gazelle scenario:", "Jumping lion")
		return gazelle.Phene_value('GazelleStrength') > self.Parameter('SignallingThreshold')
	
	def jump(self, gazelle):
		" Strong gazelles perform a jump proportional to their signalling gene "
		if not self.gazelle(gazelle):	error("Gazelle scenario:", "Signalling lion")
		if self.strongGazelle(gazelle):
			#return noise_add(gazelle.gene_relative_intensity('GazelleSignal'), self.Parameter('Noise'))
			return gazelle.gene_relative_intensity('GazelleSignal')
		return 0
	
	def initialization(self):
		self.Jumps = 0 

	def prepare(self, indiv):
		""" defines what is to be done at the individual level before interactions
			occur - Used in 'life_game'
		"""
		indiv.score(self.Parameter('PreyCost')*self.Parameter('GroupMaxSize')*self.Parameter('Rounds'), FlagSet=True)

	def partner(self, indiv, members):
		""" a gazelle's partner must be a lion
		"""
		if not self.gazelle(indiv):	return None
		lions = [L for L in members if not self.gazelle(L)]
		if lions != []:	return random.choice(lions)
		else:			return None
		
		
	def interaction(self, gazelle, lion):
		if self.gazelle(gazelle) and lion:	# a partner has been found - Hunt may begin
			if self.gazelle(lion):	error("Gazelle scenario:", "Hunting gazelle")
			# the lion decides whether the gazelle is worth chasing
			chase = True
			if random.randint(1,100) < lion.gene_relative_intensity('LionSensitivityToSignal'):
				# this lion pays attention to jumps
				jump = self.jump(gazelle)
				# the gazelle pays the price
				gazelle.score(-percent(self.Parameter('JumpCost')*jump))
				if jump > self.Parameter('Noise'):
					chase = False	# This wise lion will consider another prey
			# Now the lion gets the benefit or cost of the chase
			if chase:
				if self.strongGazelle(gazelle):		# SOMETHING'S MISSING HERE . . .
					lion.score(-self.Parameter('LostPreyCost'))
				else:
					lion.score(self.Parameter('HunterReward'))
					gazelle.score(-self.Parameter('PreyCost'))					


	def couples(self, members):						
		"""	Lions and gazelles should not attempt to make babies together
			(because the selection of both subspecies operates on different scales)
		"""
		gazelles = [G for G in members if self.gazelle(G)]
		lions = [L for L in members if not self.gazelle(L)]
		Couples = Default_Scenario.couples(self, gazelles) + Default_Scenario.couples(self, lions)
		#print sorted(["%d%d" % (1*self.gazelle(C[0]),1*self.gazelle(C[1])) for C in Couples])
		return Couples
					
	def lives(self, members):
		""" Lions and gazelles should be evaluated separately
		"""
		gazelles = [G for G in members if self.gazelle(G)]
		lions = [L for L in members if not self.gazelle(L)]
		Default_Scenario.lives(self, gazelles)
		Default_Scenario.lives(self, lions)

	# def end_game(self, members):
		# jumpinggazelles = [G for G in members if self.gazelle(G) and self.jump(G)]
		# if jumpinggazelles:
			# self.Jumps = sum([self.jump(G) for G in jumpinggazelles]) / len(jumpinggazelles)
	
	def update_positions(self, members, groupLocation):
		" Allows to define spatial coordinates for individuals. "
		for m in enumerate(members):
			if self.gazelle(m[1]):
				m[1].location = (groupLocation + m[0], 4 + self.jump(m[1]), 'blue')
			else:
				m[1].location = (groupLocation + m[0], 1 , 'red')

	def local_display(self,DummyVariable):
		" allows to diplay locally defined values "
		return self.Jumps
					
	def default_view(self):	return ['Field']
	
	def display_(self):
		""" Defines what is to be displayed. 
			It should return a list of pairs (C,X)
			where C is the curve colour and X can be
			'best', 'average', 'n' (where n is any string processed by local_display),
			any gene name defined in genemap or any phene defined in phenemap
		"""
		disp = [('blue', 'GazelleSignal'), ('red', 'LionSensitivityToSignal')] 	
		# disp += [('yellow','')]
		return disp
		

		
###############################
# Local Test                  #
###############################

if __name__ == "__main__":
	print __doc__ + '\n'
	SB = Scenario()
	raw_input('[Return]')
	
