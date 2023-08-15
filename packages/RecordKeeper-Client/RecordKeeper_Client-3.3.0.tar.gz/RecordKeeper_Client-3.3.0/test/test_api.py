import os
import unittest
from uuid import UUID

from rkclient import RKClient, RKClientFactory


class TestAPIUnit(unittest.TestCase):

    def test_prepare_pem(self):
        rk = RKClient('http://receiver', 'emitter-name')
        pred = rk.prepare_pem('', None)
        pem = rk.prepare_pem('some_type_name', pred.ID, {"value_int": -123})

        self.assertIs(type(pem.ID), UUID)
        self.assertEqual(pem.Predecessor, pred.ID)
        self.assertEqual(pem.Type, 'some_type_name')
        self.assertEqual(pem.Emitter, 'emitter-name')
        self.assertEqual(pem.Properties["value_int"], -123)

    def test_rk_factory_mock(self):
        os.environ['RK_MOCK'] = 'true'
        rk = RKClientFactory.get('http://receiver', 'emitter-name')
        del os.environ['RK_MOCK']

        pred = rk.prepare_pem('', None)
        self.assertIsNotNone(pred)

        pem = rk.prepare_pem('some_type_name', pred.ID, {"value_int": -123})
        self.assertIsNotNone(pem)

        _, ok = rk.send_pem(pred)
        self.assertTrue(ok)

        _, ok = rk.set_tag('test-namespace-unique-name', 'bar', pem)
        self.assertTrue(ok)
