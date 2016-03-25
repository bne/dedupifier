import os
import unittest

from dedupifier import dedupe

class DedupeTestCase(unittest.TestCase):

	def setUp(self):
		path = os.path.join(os.path.dirname(__file__), 'fixtures')		
		self.dedupifier = dedupe.Dedupifier(path)

	def test_find_duplicates_by_name(self):
		self.dedupifier.get_items()

		self.assertEqual(len(self.dedupifier.items), 3)
		self.assertEqual(len(self.dedupifier.items['Bennyisawesome.jpg']), 4)
		self.assertEqual(len(self.dedupifier.items['blackmagic_hotpixel_test.jpg']), 5)
		self.assertEqual(len(self.dedupifier.items['hunger-games.png']), 4)

	def test_find_duplicates_by_hash(self):
		self.dedupifier.get_items(use_hash=True)
				
		self.assertEqual(len(self.dedupifier.items), 3)
		self.assertEqual(len(self.dedupifier.items['07486b2d43fe6e8bbba0cf500c56db01']), 6)
		self.assertEqual(len(self.dedupifier.items['9ec4f5e7da187ff44d179d85aac654e4']), 2)
		self.assertEqual(len(self.dedupifier.items['c714aa4f97b706b2cd07b360f2fd1dbb']), 5)
