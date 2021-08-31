import unittest
import pandas as pd
import warnings
import os, sys

os.chdir(os.path.abspath(fr"../main"))
sys.path.insert(1, f'{os.getcwd()}')
print(os.getcwd())
import main as t


class TestDf(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		print("-" * 50)

	@classmethod
	def tearDownClass(cls):
		print("-" * 50)

	def setUp(self):
		warnings.simplefilter('ignore', category=ResourceWarning)
		print(self.id().split('.')[-1].strip("."),end=": ")

	def tearDown(self):
		#remove "." from the start of the test name

		print("pass")

	def test_following(self):
		self.assertIsInstance(t.functions.user_following_csv(), pd.DataFrame)

	def test_follower(self):
		self.assertIsInstance(t.functions.user_followers_csv(), pd.DataFrame)

	def test_most_starred_repo(self):
		self.assertIsInstance(t.functions.most_starred_repo(), pd.DataFrame)

	def test_user_fork_csv(self):
		self.assertIsInstance(t.functions.user_fork_csv(), pd.DataFrame)
	
	def test_user_star_csv(self):
		self.assertIsInstance(t.functions.user_star_csv(), pd.DataFrame)

	def test_user_csv(self):
		self.assertIsInstance(t.functions.user_csv(), pd.DataFrame)

		

if __name__ == "__main__":
	unittest.main(warnings='ignore')
