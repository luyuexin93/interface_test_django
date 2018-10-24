from test.module import Calculator
import unittest

class ModuleTest(unittest.TestCase):

    def setUp(self):
        self.cal= Calculator(3,8)

    def tearDown(self):
        pass

    def test_add(self):
        result=self.cal.add()
        self.assertEqual(result,11)

    def test_sub(self):
        result = self.cal.sub()
        self.assertEqual(result,-5)

    def test_mul(self):
        result = self.cal.mul()
        self.assertEqual(result,24)

    def test_div(self):
        result = self.cal.div()
        self.assertEqual(result,0.375)

if __name__ == "__main__":
    #unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(ModuleTest("test_add"))
    suite.addTest(ModuleTest("test_sub"))
    suite.addTest(ModuleTest("test_mul"))
    suite.addTest(ModuleTest("test_div"))
    runner = unittest.TextTestRunner()
    runner.run(suite)