# -*- coding: utf-8 -*-

import unittest
import logging

from pyutil_cfg import cfg


class TestCfg(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init(self):
        logger, config = cfg.init('test_cfg', 'tests/data/test.ini', params={'test_params': 'test'})

        assert config['a'] == 'b'
        assert config['test_params'] == 'test'
        assert config['test_ini'] == 'test2'
        assert config['test_list'] == ['test0', 'test1', 2]
        assert config['test_dict'] == {'test_key': 'test_val', 'test_key2': 'test_val2'}
        assert config['test_set'] == set(['a', 'b', 'c'])
        assert config['test_list_dict'] == [
            {'A': 1, 'B': 'b'},
            {'A': 2, 'B': 'c'},
            {'A': 3, 'B': 'd'},
            {'A': 4, 'B': 'e'},
        ]

    def test_init_no_logger(self):
        logger, config = cfg.init('test_cfg', 'tests/data/test_no_logger.ini', params={'test_params': 'test'})

        assert config['a'] == 'b'
        assert config['test_params'] == 'test'
        assert config['test_ini'] == 'test2'
        assert config['test_list'] == ['test0', 'test1', 2]
        assert config['test_dict'] == {'test_key': 'test_val', 'test_key2': 'test_val2'}
        assert config['test_set'] == set(["a", "b", "c"])

    def test_init_none(self):
        logger, config = cfg.init('test_cfg', 'tests/data/test_none.ini', params={'test_params': 'test'})

        assert type(config) == dict
        assert config['test_params'] == 'test'
