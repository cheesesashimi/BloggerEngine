#!/usr/bin/python

import unittest
import base_model


class BaseModelTests(unittest.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def testConstructor(self):
    base = base_model.BaseModel()
    self.assertIsNotNone(base.id)
    self.assertIsNotNone(base.created_timestamp)

if __name__ == '__main__':
  unittest.main()
