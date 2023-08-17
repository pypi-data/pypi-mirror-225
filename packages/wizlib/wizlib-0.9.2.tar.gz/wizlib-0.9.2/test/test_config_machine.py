from unittest import TestCase
from argparse import ArgumentParser
import os
from unittest.mock import patch
from pathlib import Path

from wizlib.config_machine import ConfigMachine
from .data_config_machine.sample import SampleMachine
from .data_config_machine.sample import SampleCommandMachine
from .data_config_machine.sample import SampleOtherMachine


class TestConfig(TestCase):

    def test_direct_arg(self):
        test_machine = SampleMachine(foo='bar')
        f = test_machine.config_get('foo')
        self.assertEqual(f, 'bar')

    def test_config_file_arg(self):
        sample = SampleMachine(
            config='test/data_config_machine/test-config.yml')
        f = sample.config_get('foo')
        self.assertEqual(f, 'erg')

    def test_nested_entry(self):
        sample = SampleMachine(
            config='test/data_config_machine/test-config.yml')
        f = sample.config_get('bar-zing')
        self.assertEqual(f, 'ech')

    def test_nested_entry_fail(self):
        sample = SampleMachine(
            config='test/data_config_machine/test-config.yml')
        f = sample.config_get('bar-za')
        self.assertIsNone(f)

    def test_specific_env_var(self):
        os.environ['DEF_G'] = 'ju'
        test_machine = SampleMachine()
        f = test_machine.config_get('def-g')
        del os.environ['DEF_G']
        self.assertEqual(f, 'ju')

    def test_conf_file_env_var(self):
        os.environ['MYAPP_CONFIG'] = 'test/data_config_machine/test-config.yml'
        test_machine = SampleMachine()
        f = test_machine.config_get('bar-zing')
        del os.environ['MYAPP_CONFIG']
        self.assertEqual(f, 'ech')

    def test_conf_file_env_var_specific_name(self):
        os.environ['MYAPP2_CONFIG'] = \
            'test/data_config_machine/test-config.yml'
        test_machine = SampleMachine(appname='myapp2')
        f = test_machine.config_get('bar-zing')
        del os.environ['MYAPP2_CONFIG']
        self.assertEqual(f, 'ech')

    def test_local_config_file(self):
        with patch('pathlib.Path.cwd',
                   lambda: Path('test/data_config_machine')):
            test_machine = SampleMachine()
            f = test_machine.config_get('bar-zing')
        self.assertEqual(f, 'ech')

    def test_home_config_file(self):
        with patch('pathlib.Path.home',
                   lambda: Path('test/data_config_machine')):
            test_machine = SampleMachine()
            f = test_machine.config_get('bar-zing')
        self.assertEqual(f, 'ech')

    def test_works_with_command(self):
        sample = SampleCommandMachine(
            config='test/data_config_machine/test-config.yml')
        f = sample.config_get('foo')
        self.assertEqual(f, 'erg')

    def works_another_way(self):
        with patch('pathlib.Path.cwd',
                   lambda: Path('test/data_config_machine')):
            test_machine = SampleOtherMachine()
            f = test_machine.config_get('bar-zing')
        self.assertEqual(f, 'waa')

    def test_nested_as_attribute(self):
        c = SampleMachine()
        c.a_b = 'c'
        self.assertEqual(c.config_get('a-b'), 'c')
