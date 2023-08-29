import unittest
from sendmail import make_list

class TestListElements(unittest.TestCase):
    def setUp(self):
        self.expected = ['welcome', 'to', 'the', 'jungle']
        self.test = "welcome,\nto , the\n, \n  jungle\n"

    def test_makelist_ShouldReturnTheExpectedList(self):
        """ """
        self.assertListEqual(make_list(self.test), self.expected)


if __name__ == "__main__":
    unittest.main()
