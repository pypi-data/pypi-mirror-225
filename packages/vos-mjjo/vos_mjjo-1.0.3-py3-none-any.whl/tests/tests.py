import unittest
from test_convaddr import TestClass as TestClass1
from test_cordate import TestClass as TestClass2


def suite():
    test_loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()

    test_suite.addTest(test_loader.loadTestsFromTestCase(TestClass1))
    test_suite.addTest(test_loader.loadTestsFromTestCase(TestClass2))

    return test_suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = suite()
    result = runner.run(test_suite)
