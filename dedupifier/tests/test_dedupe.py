import os
import unittest

from dedupifier import dedupe

class DedupeTestCase(unittest.TestCase):

	def setUp(self):
		path = os.path.join(os.path.dirname(__file__), 'fixtures')		
		self.dedupifier = dedupe.Dedupifier(path)
		self.dedupifier.dedupify()		

	def test_find_duplicates(self):
		self.assertEqual(len(self.dedupifier.items), 3)




