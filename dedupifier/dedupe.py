
class Dedupifier(object):

	def __init__(self, path):
		self.path = path
		self.items = {}

	def dedupify(self):
		self.items = {1:1,2:2,3:3}

		return self.items