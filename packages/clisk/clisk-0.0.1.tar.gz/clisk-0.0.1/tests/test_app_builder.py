import unittest

import clisk


class TestDefaultBuilder(unittest.TestCase):
    def test_construction(self):
        @clisk.command('test')
        def _():
            print('hello world!')

        with self.assertRaises(SystemExit):
            clisk.run()
