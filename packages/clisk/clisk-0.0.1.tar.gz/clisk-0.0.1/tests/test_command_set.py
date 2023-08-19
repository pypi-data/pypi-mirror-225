import unittest

from clisk._clisk import CommandSet, Command, KeywordError  # NOQA


class TestCommandSet(unittest.TestCase):
    def test_construction(self):
        cmdset = CommandSet({})

        func1 = lambda _: True  # NOQA
        args1 = {'number': 1}
        cmdset.add(['a', 'b', 'c'], func1, args1, False)
        self.assertEqual(func1, cmdset._commands['a']._commands['b']._commands['c']._function)  # NOQA
        self.assertEqual(args1, cmdset._commands['a']._commands['b']._commands['c']._command_arguments)  # NOQA

        func2 = lambda _: True  # NOQA
        args2 = {'number': 2}
        cmdset.add(['a', 'b', 'd'], func2, args2, False)
        self.assertEqual(func2, cmdset._commands['a']._commands['b']._commands['d']._function)  # NOQA
        self.assertEqual(args2, cmdset._commands['a']._commands['b']._commands['d']._command_arguments)  # NOQA

        with self.assertRaises(KeywordError):
            cmdset.add(['a'], func1, args1, False)

        cmdset.add(['e'], None, args1, True)
        cmdset.add(['e', 'f'], func1, args1, False)
        self.assertEqual(func1, cmdset._commands['e']._commands['f']._function)  # NOQA
        self.assertEqual(args1, cmdset._commands['e']._commands['f']._command_arguments)  # NOQA

        args3 = {'number': 3}
        cmdset.add(['a'], None, args3, True)  # NOQA
        self.assertEqual(args3, cmdset._commands['a']._arguments)  # NOQA
        args4 = {'number': 4}
        cmdset.add(['a'], None, args4, True)  # NOQA
        self.assertEqual(args4, cmdset._commands['a']._arguments)  # NOQA
