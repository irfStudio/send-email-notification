import sys
import os.path  
import unittest

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) + "/src/"
sys.path.append(src_path)
from sendmail import make_list


class TestListElements(unittest.TestCase):
    def setUp(self):
        self.expected = ["welcome", "to", "the", "jungle"]
        self.test = "welcome,\nto , the\n, \n  jungle\n"

    def test_makelist_ShouldReturnTheExpectedList(self):
        """Test 01"""
        self.assertListEqual(make_list(self.test), self.expected)


if __name__ == "__main__":
    unittest.main()
