##############################################################################
# EVOLIFE  www.dessalles.fr/Evolife                    Jean-Louis Dessalles  #
#            Telecom ParisTech  2013                       www.dessalles.fr  #
##############################################################################



"""	 EVOLIFE: Favourable Scenario:
		A scenario to study the fate of favourable / unfavourable mutation
		(i.e. the most basic Darwinian case)
		Also: allows to define the benefit at the group level, what allows
		the study of the so-called 'group selection'
"""

	#=============================================================#
	#  HOW TO MODIFY A SCENARIO: read Default_Scenario.py		 #
	#=============================================================#


import sys
if __name__ == '__main__':  sys.path.append('../..')  # for tests


from Evolife.Scenarii.Default_Scenario import Default_Scenario
from Evolife.Tools.Tools import percent


######################################
# specific variables and functions   #
######################################

class Scenario(Default_Scenario):

	######################################
	# Most functions below overload some #
	# functions of Default_Scenario	  #
	######################################

	def genemap(self):
		""" Defines the name of genes and their position on the DNA.
			(see Genetic_map.py)"""
		return [('favourable',8),('neutral',8)]  

	def initialization(self):
		self.CollectiveAsset = 0 # collective wealth due to group members
		self.Cumulative = bool(self.Parameter('Cumulative'))	# indicates whether scores are accumulated or are reset each year

	def start_game(self,members):
		""" defines what to be done at the group level each year
			before interactions occur - Used in 'life_game'
		"""

		if len(members) == 0:   return
		InitialBonus = 0
		
		# special case of negative benefits: Individuals are given an initial bonus to keep scores positive
		if self.Parameter('CollectiveBenefit') < 0:
			InitialBonus = -self.Parameter('CollectiveBenefit')		# just to keep scores positive
		if self.Parameter('IndividualBenefit') < 0:
			InitialBonus -= self.Parameter('IndividualBenefit')	# just to keep scores positive

		self.CollectiveAsset = 0	# reset each year

		for indiv in members:
			indiv.score(InitialBonus, FlagSet=not self.Cumulative)	# Initial bonus is added or assigned to Score 
			
			################################
			# computing collective benefit #
			################################
			# each agent contributes to collective benefit in proportion of its 'favourable' gene value
			self.CollectiveAsset += indiv.gene_relative_intensity('favourable')
		self.CollectiveAsset = float(self.CollectiveAsset) / len(members)

	def evaluation(self,indiv):
		""" Implements the computation of individuals' scores -  - Used in 'life_game'
		"""
		################################
		# computing individual benefit #
		################################
		Bonus = percent(indiv.gene_relative_intensity('favourable') * self.Parameter('IndividualBenefit'))
		Bonus += percent(self.CollectiveAsset * self.Parameter('CollectiveBenefit'))
		indiv.score(Bonus, FlagSet=False)  # Bonus is added to Score 

	def default_view(self):	return ['Genomes']		

	def update_positions(self, members, groupLocation):
		""" Allows to define spatial coordinates for individuals.
			These positions are displayed in the Field window.
		"""
		for indiv in enumerate(members):
			indiv[1].location = (groupLocation + indiv[0], indiv[1].score())

	def display_(self):
		" Defines what is to be displayed. "
		return [('red','favourable'),('yellow','neutral')]


		
###############################
# Local Test                  #
###############################

if __name__ == "__main__":
	print __doc__ + '\n'
	raw_input('[Return]')
	
