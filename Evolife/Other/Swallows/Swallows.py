##############################################################################
# Swallows     www.dessalles.fr/Evolife                 Jean-Louis Dessalles #
#              Telecom ParisTech  2013                   www.dessalles.fr    #
##############################################################################


""" Studying Collective Decision:
Though individual agents may have a tendency to
take a decision (e.g. to migrate away) that smoothly
increases with time, the collective takes a sharp decision.
"""

# In this story, swallows' tendency to perch (on a wire, say) increases
# smoothly with time. But swallows tend to imitate each other: their
# tendency to join a group of perched birds is proportional to its size
# The simulation shows that at some point, a collective decision to
# perch takes place. This offers an insight into the kind of collective
# processes involved when birds decide to migrate away.



##############################################################################
#  Launching a simulation													#
##############################################################################

""" Simulation Control
"""
import sys
import random
from time import sleep

from PyQt4 import QtGui

sys.path.append('../../..')

from Evolife.QtGraphics.Evolife_Window import Start
from Evolife.Ecology.Observer import Experiment_Observer
from Evolife.Tools.Tools import boost
from Evolife.Scenarii.Parameters import Parameters

print '\n\t[%s]\n\n' % boost() # a technical trick that may make Python faster (only with python 2.6 or below and on Windows)

WirePosition = 15	# position of the wire on display
Params = Parameters('_Params.evo')

def PerchingProb(Time, TimeSlope, MaxTime):
	" computes the rising probability for an individual swallow to perch down on the wire "
	TimeOffset = 0	# time before considering perching down
	return max(0, min(1.0, 0.002 + ((TimeSlope/1000.0 + 0.001) * (Time - TimeOffset))/MaxTime))

class Swallow_Observer(Experiment_Observer):
	" This class stores values about the simulation "

	def __init__(self):
		Experiment_Observer.__init__(self, Params) # stores global information

		#additional parameters	  
		self.Perched = 0		# number of agents perched
		self.Positions = []	 # agents' positions in the sky
		self.recordInfo('CurveNames', (('blue','Proportion of swallows perched'), ('yellow', 'Perching probability x 1000')))

	def get_data(self, Slot):
		if Slot == 'Positions':	
			Wire = [('Wire',(1, WirePosition-2, 'black', 1, len(self.Positions), WirePosition-2, 'grey', 1),)]
			return tuple(Wire + self.Positions)
		return Experiment_Observer.get_data(self, Slot)

	def get_info(self, Slot):
		if Slot == 'PlotOrders':
			return [('blue', (self.StepId, 100.0 * self.Perched/len(self.Positions))),	# number of individuals perched
					('yellow', (self.StepId,
						 1000 * PerchingProb(self.StepId, self.Parameter('TimeSlope'),
											 self.TimeLimit)))]		# perching probability
		return Experiment_Observer.get_info(self, Slot)

	def __repr__(self):
		return "%d agents\n%s" % (self.Parameter('NbAgents'), str(map(lambda x: x[1][1], self.Positions)))

class Swallow(object):
	""" Defines individual agents
	"""
	def __init__(self, IdNb):
		self.GroupOffset = Observer.Parameter('GroupOffset')	# minimum size of group worth joinning
		self.Inertia = Observer.Parameter('Inertia')	# minimum time spent on the wire
		self.IdNb = IdNb	# Identity number
		self.Name = 'S%d'   % self.IdNb
		self.TimeSlope = Observer.Parameter('TimeSlope') * random.random()	# time derivative of the probability of perching
		self.GroupSlope = Observer.Parameter('GroupSlope') * random.random() + 0.5  # derivative of the probability of joining a perched group
		self.perched = False
		self.PerchingTime = -1  # last time of perching (-1 if never perched)
		self.Position = random.randint(50,100) # vertical position

	def lands(self, TimeStep, MaxTime, GroupSize, NbAgents):
		" the agent decides to perch on the wire "
		if self.perched and TimeStep < self.PerchingTime + self.Inertia:
			# in this version, perched individuals do not fly up easily 
			return True
		Prob1 = PerchingProb(TimeStep, self.TimeSlope, MaxTime)
		Prob2 = max(0, min(1.0, (0.02 + self.GroupSlope * (GroupSize-self.GroupOffset))/NbAgents))
		if (random.random() < Prob1) or (random.random() < Prob2):
			self.perched = True
			self.Position = WirePosition  # on the wire
			self.PerchingTime = TimeStep
			return True
		else:
			self.perched = False
			self.Position = random.randint(50,100) # new vertical position
			self.PerchingTime = -1
			return False

class Population(object):
	" defines the population of agents "
	def __init__(self, NbAgents, Observer):
		" creates a population of swallow agents "
		self.Pop = [Swallow(IdNb) for IdNb in range(NbAgents)]
		self.PopSize = NbAgents
		self.Obs = Observer
		self.Perched = 0	# number of swallows on the wire
		self.Decisions = 0
		self.Obs.Positions = self.positions()
				 
	def positions(self):
		return [(A.Name,(A.IdNb,A.Position, 'black', 6)) for A in self.Pop]
	
	def One_Decision(self):
		" one swallow is randomly chosen and decides whether to perch or not "
		# This procedure is repeatedly called by the simulation thread
		agent = self.Pop[random.randint(0,self.PopSize-1)]
		OldPosition = agent.perched
		Landing = agent.lands(self.Obs.StepId, self.Obs.TimeLimit, self.Perched, self.PopSize)
		if OldPosition != Landing:
			if OldPosition:	self.Perched -= 1
			else:			self.Perched += 1
		self.Decisions += 1
		self.Obs.season(self.Decisions / self.PopSize)  # sets StepId
		self.Obs.Perched = self.Perched
		self.Obs.Positions[agent.IdNb] = (agent.Name,(agent.IdNb,agent.Position, 'black', 6))	# last coord = size
		return agent.IdNb	 

	def Many_decisions(self):
		" every swallow on average has been given a chance to perch down "
		for Sw in range(self.PopSize):
			self.One_Decision()
		return True
	
if __name__ == '__main__':

	print __doc__

	Observer = Swallow_Observer()   # Observer contains statistics
	#Observer.recordInfo('BackGround', 'blue11')	# windows will have this background by default
	Pop = Population(Observer.Parameter('NbAgents'), Observer)   # set of flying swallows

	Start(Pop.Many_decisions, Observer, Capabilities='FCP')

	

__author__ = 'Dessalles'
