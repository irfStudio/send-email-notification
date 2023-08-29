import os.path
import sys
import unittest

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) + "/src/"
sys.path.append(src_path)
from sendmail import make_list


class TestListElements(unittest.TestCase):
    def setUp(self):
        self.expected = ["welcome", "to", "the", "jungle"]
        
        self.test = "welcome,\nto , the\n, \n  jungle\n"
        self.test2 = "welcome\nto;the;;, \n  jungle\n"

    def test_makelist_ShouldReturnTheExpectedList_1(self):
        """Test 01"""
        self.assertListEqual(make_list(self.test), self.expected)
        
    def test_makelist_ShouldReturnTheExpectedList_2(self):
        """Test 02"""
        self.assertListEqual(make_list(self.test2), self.expected)


if __name__ == "__main__":
    unittest.main()
