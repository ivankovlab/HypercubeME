import unittest
from utils import *


class TestHypercubes(unittest.TestCase):

    def setUp(self):
        pass

    def test_dimension_1(self):
        self.assertEqual(
            read_file_with_hypercubes('test_expected/hypercubes_1.txt'),
            read_file_with_hypercubes('test_complete_03/hypercubes_1.txt'))

    def test_dimension_2(self):
        self.assertEqual(
            read_file_with_hypercubes('test_expected/hypercubes_2.txt'),
            read_file_with_hypercubes('test_complete_03/hypercubes_2.txt'))

    def test_dimension_3(self):
        self.assertEqual(
            read_file_with_hypercubes('test_expected/hypercubes_3.txt'),
            read_file_with_hypercubes('test_complete_03/hypercubes_3.txt'))


if __name__ == '__main__':
    unittest.main()
