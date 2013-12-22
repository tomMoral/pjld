##############################################################################
# EVOLIFE  www.dessalles.fr/Evolife                    Jean-Louis Dessalles  #
#            Telecom ParisTech  2013                       www.dessalles.fr  #
##############################################################################



##############################################################################
#  S_SexRatio                                                                #
##############################################################################


""" EVOLIFE: SexRatio Scenario:
	If the sex ratio in the progeny is genetically controlled, a 50-50 ratio 
	emerges, despite the fact that males consume resources without investing
	in offspring. 
	However, in hymenoptera (wasps, bees, ants), in which males are haploid 
	(one exemplar for each chomosome) whereas females are diploid (two exemplars
	of each chromosome), sex ratio is expected to converge toward 25-75 whenever 
	it is controlled by genes expressed in sisters (workers).
"""
	#=============================================================#
	#  HOW TO MODIFY A SCENARIO: read Default_Scenario.py		 #
	#=============================================================#

import sys
if __name__ == '__main__':  sys.path.append('../..')  # for tests



import random

from Evolife.Scenarii.Default_Scenario import Default_Scenario


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
		return [('sexControl',0)]	# size 0 means that the gene's length is given in the configuration

	def phenemap(self):
		""" Defines the set of non inheritable characteristics
		"""
		return ['Sex']  # Sex is considered a phenotypic characteristic !
						# This is convenient because sex is determined at birth
						# and is not inheritable

	def female(self, Indiv):
		if Indiv.Phene_value('Sex') > 50:	return True
		return False
		
	def parents(self, candidates):
		""" selects a female and a male for procreation
		"""
		mothers = [m for m in candidates if self.female(m[0])]
		fathers = [f for f in candidates if not self.female(f[0])]
		try:	return (random.choice(mothers), random.choice(fathers))
		except	IndexError:	return None
		
	def new_agent(self, child, parents):
		""" makes a child from a couple 
		"""
		if parents:		# parents is None when the population is initialized
			# deciding the child's sex
			# Suppose that mother's genes decide
			mother = parents[0]
			if random.randint(0,100) >= mother.gene_relative_intensity('sexControl'):
				child.Phene_value('Sex',100)
			else:
				child.Phene_value('Sex',0)

			# testing selective death
			if not self.female(child) and random.randint(0,100) < self.Parameter('SelectiveDeath'):
				return False
		
			if self.Parameter('Hymenoptera') and not self.female(child):
				# The haplo-diploidy of hymenoptera is simulated by
				# increasing the contribution of mother to the child's genome
				child.hybrid(child, mother) # the child is more related to its mother
		return True

		
	def display_(self):
		" Defines what is to be displayed. "
		return [('white','sexControl'), ('red','Sex')]

			


###############################
# Local Test				  #
###############################

if __name__ == "__main__":
	print __doc__ + '\n'
	raw_input('[Return]')
	
