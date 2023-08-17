from unittest import TestCase
from unittest.mock import patch
from io import StringIO
import os

from wizlib.command_handler import CommandHandler
from .data_command import TestCommand


class TestCommandSync(TestCase):

    def test_from_handler(self):
        r, s = CommandHandler(TestCommand).handle(['play'])
        self.assertEqual(r, 'Play!')

    def test_default(self):
        r, s = CommandHandler(TestCommand).handle()
        self.assertEqual(r, 'Play!')

    @patch('sys.stdout', StringIO())
    def test_wrong_command(self):
        h = CommandHandler(TestCommand)
        c = h.get_command(['eat'])
        self.assertIsNone(c)

    @patch('sys.stdout', StringIO())
    def test_handle_wrong_command(self):
        h = CommandHandler(TestCommand)
        r, s = h.handle(['eat'])
        self.assertIsNone(r)

    def test_command_arg(self):
        h = CommandHandler(TestCommand)
        c = h.get_command(['play', '--dd', 't'])
        self.assertEqual(c.dd, 't')

    def test_atriarch_args(self):
        h = CommandHandler(TestCommand)
        c = h.get_command(['--xx', 'y', 'play'])
        self.assertEqual(c.xx, 'y')

    def test_error(self):
        with patch('sys.stdout', o := StringIO()):
            with patch('sys.argv', ['', 'error']):
                CommandHandler.shell(TestCommand)
        o.seek(0)
        r = o.read()
        self.assertIn('division by zero', r)
        self.assertEqual(len(r.splitlines()), 3)

    @patch('sys.stdout', StringIO())
    def test_error_debug(self):
        os.environ['DEBUG'] = '1'
        with self.assertRaises(ZeroDivisionError):
            with patch('sys.argv', ['', 'error']):
                CommandHandler.shell(TestCommand)
        del os.environ['DEBUG']
