##############################################################################
# EVOLIFE  www.dessalles.fr/Evolife                    Jean-Louis Dessalles  #
#            Telecom ParisTech  2013                       www.dessalles.fr  #
##############################################################################


##############################################################################
#  Genetic Map                                                                     #
##############################################################################


""" EVOLIFE: Module Genetic_map:
		Definition of genes as DNA segment having semantics """

import sys
if __name__ == '__main__':  sys.path.append('../..')  # for tests


from Evolife.Tools.Tools import error

class Gene_def(object):
	"   class Gene_def: definition of semantic segments on DNA "

	def __init__(self, gene_name, gene_length, locus, position, length_def):
		""" A gene knows its name, its length,
			its locus (order in the list of genes) and its start and end position
			on the DNA
		"""
		self.name = gene_name
		if gene_length:
			self.length = gene_length
		elif length_def:
			self.length = length_def
		else:
			error('Gene definition','Zero length with zero Default length')
		self.locus = locus
		self.start = position
		self.end = position + self.length

	def __repr__(self):
		return 'L' + str(self.locus) + ': ' + self.name + ' ' + str(self.start) + '->' + str(self.end) + ' '

class Genetic_map(object):
	"   a Genetic_map is a series of genes, located one after the other "

	def __init__(self, GeneMap):
		self.init_genes(GeneMap)

	def init_genes(self,gene_list):
		" creates genes and puts them in a list "
		self.GeneMap = []
		locus = 0
		current_pos = 0
		for (g_name,g_length) in gene_list:
			# genes are assigned locus and future position on DNA
			NewGene = Gene_def(g_name, g_length, locus, current_pos, self.Parameter('GeneLength'))
			self.GeneMap.append(NewGene)
			locus += 1
			current_pos = NewGene.end

	def get_gene(self,locus):
		try:
			return self.GeneMap[locus]
		except IndexError:
			error("Gene_def: incorrect locus")

	def get_locus(self, gene_name):
		for g in self.GeneMap:
			if g.name == gene_name:
				return g.locus
		error("Genetic_map: unknown gene name: " + str(gene_name))
		return None

	def get_gene_name(self, locus):
		return self.get_gene(locus).name

	def get_gene_names(self):
		return [g.name for g in self.GeneMap]
	
	def get_gene_boundaries(self,locus):
		return (self.get_gene(locus).start, self.get_gene(locus).end)

	def gene_boundaries(self, gene_name):
		return get_boundaries(self, get_locus(self, gene_name))

	def geneMap_length(self):
		return self.get_gene(len(self.GeneMap)-1).end

	def locus_range(self, Locus):
		" returns the maximal amplitude of the gene at Locus "
		coding = self.Parameter('GeneCoding')
		if coding in range(-1,3):
			# old numeric designation of coding
			coding = ['NoCoding', 'Weighted', 'Unweighted', 'Gray'][coding+1]		
		if coding in ['Weighted', 'Gray']:
			# Usual integer coding
			return (1 << self.get_gene(Locus).length ) - 1
		elif coding == 'Unweighted':
			# Genes are coded as the number of 1s on the DNA section
			return self.get_gene(Locus).length
		elif coding == 'NoCoding':
			return 1
		else:
			error("Genetic Map", 'unknown binary coding mode: %d' % self.Parameter('GeneCoding'))

	def gene_range(self, gene_name):
		return self.locus_range(self.get_locus(gene_name))

	def gene_pattern(self):
		" generates a tuple giving a binary mask showing gene alternation on DNA "
		G = 0
		pattern = []
		for g in self.GeneMap:
			pattern += [G] * g.length
			G = 1 - G
		return tuple(pattern)
		
	def __repr__(self):
		return "Genetic map:\n\t" + '\n\t'.join([g.__repr__() for g in self.GeneMap])
	 


if __name__ == "__main__":
	print __doc__
	print Gene_def.__doc__
	print Genetic_map.__doc__ + '\n'




###################################
# Test                            #
###################################

if __name__ == "__main__":
	from Evolife.Scenarii.Parameters import Parameters
	class GMTest(Genetic_map, Parameters):
		def __init__(self):
			Parameters.__init__(self,'../Evolife.evo')
			Genetic_map.__init__(self,[('sex',1), ('prems',4),('deuze',7),('terce',2)])
	GeneMap = GMTest()
	print GeneMap
	print 'pattern: ',
	print GeneMap.gene_pattern()
	raw_input('[Return]')


__author__ = 'Dessalles'
