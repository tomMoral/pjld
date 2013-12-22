##############################################################################
# EVOLIFE  www.dessalles.fr/Evolife                    Jean-Louis Dessalles  #
#            Telecom ParisTech  2013                       www.dessalles.fr  #
##############################################################################



##############################################################################
#  S_SumBits                                                                 #
##############################################################################


"""	 EVOLIFE: SumBits Scenario:
		A scenario to study how fast all bits in the DNA evolve to 1
		A useful scenario for didactic purposes
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
	# Most functions below overload some #
	# functions of Default_Scenario	  #
	######################################


	def genemap(self):
		""" Defines the name of genes and their position on the DNA.
			(see Genetic_map.py)"""
		return [('sumbit',100)]  # Add new elements to the list to insert new genes

	def evaluation(self,indiv):
		""" Implements the computation of individuals' scores
		"""
		if indiv.score() == 0:  # just check whether it's a newborn, to avoid computing score n times
			# score() without input value returns the current value of the score 
			# gene_intensity('sumbit') returns the number of bits set to 1 (if UNWEIGHTED is chosen in the configuration file)
			# gene_relative_intensity('sumbit') returns that value brought back between 0 and 100
			# The value is merely copied into the score
			# (Flagset=True means that thre previous value of the score is deleted)
			indiv.score(indiv.gene_relative_intensity('sumbit'), FlagSet=True)
				

	def update_positions(self, members, start_location):
		""" locates individuals on a 2-D space
		"""
		# sorting individuals by gene value (provisory)
		duplicate = members[:]
		duplicate.sort(key=lambda x: x.gene_intensity('sumbit'))
		for m in enumerate(duplicate):
			m[1].location = (start_location+m[0], m[1].score())

	def default_view(self):	return ['Genomes']
	
	def display_(self):
		""" Defines what is to be displayed. It offers the possibility
			of plotting the evolution through time of the best score,
			the average score, and the average value of the
			various genes defined on the DNA.
			It should return a list of pairs (C,X)
			where C is the curve colour and X can be
			'best', 'average', or any gene name as defined by genemap
		"""
		return [('white','best'),('blue','average')]
		


###############################
# Local Test                  #
###############################

if __name__ == "__main__":
	print __doc__ + '\n'
	SB = Scenario()
	raw_input('[Return]')
	
