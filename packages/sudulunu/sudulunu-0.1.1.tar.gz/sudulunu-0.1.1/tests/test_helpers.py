import unittest

from sudulunu.helpers import rand_delay

print("hi")

class TestDivideByThree(unittest.TestCase):
	def test_divide_by_three(self):
		self.assertEqual(rand_delay(5))

unittest.main()

print("hi")