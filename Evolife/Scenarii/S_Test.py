##############################################################################
# EVOLIFE  www.dessalles.fr/Evolife                    Jean-Louis Dessalles  #
#            Telecom ParisTech  2013                       www.dessalles.fr  #
##############################################################################



##############################################################################
#  S_Test : a scenario that does nothing ! (and to be customized)            #
##############################################################################

	#   If your scenario is 'XXX', copy this file to S_XXX.py.
	#   Indicate your name, date, context and abstract.
	#   Change the scenario name in the Evolife Configuration Editor
	#   for the [Run] button to execute S_XXX.py.
	#   You may have to edit the Evolife Configuration File (EvolifeConfigTree.xml)
	#   (exit from the Configuration Editor first!)
	#   to add new parameters. You may use you favorite editor (e.g. Emacs or Notepad++)
	#   or a specialized xml editor such as "Serna XML Editor" (available for free).
	#   Insert a section for your scenario by copy and modifying an existing scenario section.
	#   Then run the Evolife Configuration Editor again
		

""" EVOLIFE: Test Scenario: This scenario does nothing ! It has to be copied and customized.

	Evolife scenarii may rewrite several functions listed here :
	(those marked with '+' are called from 'Group.py')
	(those marked with 'o' are called from 'Observer.py')
	
	COPY-PASTE the required functions from Default_Scenario.py

	- initialization(self): allows to define local variables
	- genemap(self):	initialises the genes on the gene map (see 'Genetic_map.py')
	- phenemap(self):   defines a list of phenotypic character names (see 'Phenotype.py')
	+ season(self, year):   makes periodic actions like resetting parameters
	+ behaviour(self, BestIndiv, AvgIndiv):   defines a behaviour to be displayed
	+ life_game(self, members): defines a round of interactions - calls the five following functions
		- start_game(self, indiv):	individual initialization before starting interactions
		- start_game(self, members):	group-level initialization before starting interactions
		- evaluation(self, Indiv):  defines how the score of an individual is computed
		- partner(self, Indiv, members):	select a partner among 'members' that will interact with 'Indiv'
		- interaction(self, Indiv, Partner):	defines a single interaction 
		- end_game(self, members):  an occasion for a closing round after all interactions
		- lives(self, members): converts scores into life points
	+ couples(self, members): returns a list of couples for procreation (individuals may appear in several couples!)
	+ new_agent(self, child, parents): initializes newborns
	+ kill_agent(self, agent): action to be performed when an agent dies
	+ update_positions(self, members, groupID):	assigns a position to agents
	o display_(self):   says which statistics are displayed each year
	o local_display_(self):   allows to diplay locally defined values

						************

	You may pick those function from actual scenarios as well.

"""

	#=============================================================#
	#  HOW TO MODIFY A SCENARIO: read Default_Scenario.py		 #
	#=============================================================#

import sys
if __name__ == '__main__':  sys.path.append('../..')  # for tests


from Evolife.Scenarii.Default_Scenario import Default_Scenario

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
		return [('Neutral1',8), ('Neutral2',8)] 

	def phenemap(self):
		""" Defines the set of non inheritable characteristics
		"""
		return ['Character']	# Elements in phenemap are integers between 0 and 100 and are initialized randomly

	def evaluation(self, Indiv):
		# some stupid behaviour, to be replaced
		if self.Parameter('Parameter1') == self.Parameter('Parameter2'):
			Indiv.score(10)

			
###############################
# Local Test                  #
###############################

if __name__ == "__main__":
	print __doc__ + '\n'
	SB = Scenario()
	raw_input('[Return]')
	
