import unittest

from clisk._clisk import Command  # NOQA


class TestCommand(unittest.TestCase):
    def test_construction(self):
        func = lambda _: True  # NOQA
        args = {}
        cmd = Command(func, args)

        self.assertEqual(func, cmd._function)
        self.assertEqual(args, cmd._command_arguments)
