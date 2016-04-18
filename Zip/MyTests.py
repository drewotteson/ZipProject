import unittest
import subprocess


class SimplisticTest(unittest.TestCase):

    def test(self):
        self.assertTrue(True)
        subprocess.call("C:\\WINDOWS\\system32\\notepad")
        subprocess.call("ping google.com")


    def practice_test(self):


        if __name__ == '__main__':
            unittest.main()

