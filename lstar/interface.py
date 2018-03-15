import re
import system as s


class MQModule:
    """
	Init instance
	"""

    def __init__(self, debugFlag, system):

        self._DEBUG_ = debugFlag
        self.system = system

    @staticmethod
    def getTestParameter():
        return "^[a-z0-9]{1,}@[a-z0-9]{1,}\.[a-z]{2,3}$"

    """
	Makes a membership query to a teacher and returns 1 if string was a member and 0 if not
	"""

    def isMember(self, test_object):

        #print(''.join(test_object.identifier))

        if not isinstance(test_object, str):
            teststring = ''.join(test_object.identifier)
        else:
            teststring = test_object

        return str(self.system.membership_query(teststring))

    """
    DEBUGGING
    """
    def queries(self):
        return self.system.queries

    def isMember_debug(self, test_object):

        #print(''.join(test_object.identifier))

        if not isinstance(test_object, str):
            teststring = ''.join(test_object.identifier)
        else:
            teststring = test_object

        return str(self.system.match(teststring))
