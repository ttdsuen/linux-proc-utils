import unittest

from linux.proc.swap import *
from linux.common import *

class TestSwapTotal(unittest.TestCase):

    def test_to_kb(self):
        self.assertEqual(_to_kb(1.0, 'kb'), 1.0)
        self.assertEqual(_to_kb(1.0, 'mb'), 1024.0)

    def test_swap_total(self):
        self.assertEqual(isinstance(swap_total(), float), True)

    def test_swap_free(self):
        self.assertEqual(isinstance(swap_free(), float), True)

    def test_swap_info(self):
        sys_swap_info = swap_info()
        self.assertEqual(isinstance(sys_swap_info['swap_total'], float), True)
        self.assertEqual(isinstance(sys_swap_info['swap_free'], float), True)


if __name__ == '__main__':
    unittest.main()
