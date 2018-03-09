import re

class MQModule:

	"""
	Init instance
	"""
	def __init__(self, debugFlag, regex):

		self._DEBUG_ = debugFlag
		self.regex = re.compile(regex)

	@staticmethod
	def getTestParameter():
		return "^[a-z0-9]{1,}@[a-z0-9]{1,}\.[a-z]{2,3}$"

	"""
	Makes a membership query to a teacher and returns 1 if string was a member and 0 if not
	"""
	def isMember(self, test_object):

		#print test_object.identifier

		if not isinstance(test_object, basestring):
			teststring = ''.join(test_object.identifier)
		else:
			teststring = test_object

		if self.regex.match(teststring):
			return '1'
		else:
			return '0'
