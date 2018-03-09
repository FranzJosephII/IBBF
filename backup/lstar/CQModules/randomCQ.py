import random
import time
from IBBFPrintModules import lstar_printer
try:
	from IBBFPrintModules import lstar_drawer
	drawer = 1
except:
	print "Unable to import drawer."
	drawer = 0

class CQModule:

	"""
	Init lstar instance
	"""
	def __init__(self, ObjectClass, MQModule, parser, debugFlag, params, testFlag, DFSM_output):

		self._DEBUG_ = debugFlag
		self._TIME_ = 0
		self._TEST_ = testFlag
		self.drawer_para = DFSM_output

		self.MQModule = MQModule
		self.Parser = parser
		self.ObjectClass = ObjectClass

		parameter = params.split(",")

		self.tries = int(parameter[0])
		self.length = int(parameter[1])

	def getTime(self):
		return self._TIME_

	@staticmethod
	def getTestParameter():
		return "1000000,50"

	"""
	Makes a membership query to a teacher and returns 1 if string was a member and 0 if not
	"""
	def membershipQuery(self, teststring):

		return self.MQModule.isMember(teststring)


	"""
	Generates x examples, if no counterexample was found the given DFSM, by chance, is correct
	"""
	def isCorrect(self, DFSM):

		start_time = time.time()

		initState = DFSM[0]
		finiteStates = DFSM[1]
		ttable = DFSM[2]
		A = DFSM[3]

		# Generate table for mapping state transitions
		stateTransTable = {'': ''}
		stateTransTable.clear()

		for key in ttable:
			for i in range(0, len(A)):
				stateTransTable[(key, A[i].identifier[0])] = ttable[key][i]

		# Generate examples and query them
		for i in range(0, self.tries):

			# Generate random example
			example = []
			for j in range(0, random.randint(0, self.length-1)):
				example.append(A[random.randint(0, len(A)-1)].identifier[0])

			# Calculate membership according to own DFSM
			answer = initState
			for a in example:
				answer = stateTransTable[(answer, a)]
			if answer in finiteStates:
				answer = '1'
			else:
				answer = '0'

			# Generate Query object
			query = self.ObjectClass.IBBFObj('')
			for a in example:
				query += self.ObjectClass.IBBFObj(a)


			# Compare
			if answer != self.membershipQuery(query):
				if self._DEBUG_ and not self._TEST_:
					lstar_printer.LstarPrinter.printDFSM(DFSM, "Following is not the correct DFSM", self.ObjectClass)
				self._TIME_ += time.time()-start_time
				return [''] + example

		self._TIME_ += time.time()-start_time
		if not self._TEST_:
			if self.drawer_para != 0 and drawer != 0:
				lstar_drawer.LstarPrinter().drawDFSM(DFSM, "Following is the correct DFSM", self.ObjectClass, self.drawer_para)
			else:
				lstar_printer.LstarPrinter.printDFSM(DFSM, "Following is the correct DFSM", self.ObjectClass)
		return ''