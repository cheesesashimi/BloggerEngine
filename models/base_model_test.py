#!/usr/bin/python

import unittest
import base_model

from collections import OrderedDict


class BaseModelTests(unittest.TestCase):
  def setUp(self):
    base_model.BaseModel.instances = {} 

  def tearDown(self):
    pass

  def testConstructor(self):
    base = base_model.BaseModel()
    self.assertIsNotNone(base.id)
    self.assertIsNotNone(base.created_timestamp)
    self.assertIsNotNone(base.instances.get(base.__class__.__name__))
    self.assertIsInstance(base.instances.get(base.__class__.__name__),
                          OrderedDict)

  def testPut_NewInstance(self):
    base = base_model.BaseModel()
    base.put()

    self.assertEquals(base,
                      base.instances[base.__class__.__name__][base.id])

  def testPut_ExistingInstance(self):
    base = base_model.BaseModel()
    base.put()
    base.put()

    self.assertEquals(base,
                      base.instances[base.__class__.__name__][base.id])
    self.assertTrue(base.id in base.instances[base.__class__.__name__])
    self.assertEquals(len(base.instances[base.__class__.__name__]), 1)

  def testPut_MultipleInstances(self):
    for instance in self.GenerateBaseModelInstances():
      instance.put()
      self.assertTrue(
          instance.id in instance.instances[instance.__class__.__name__])

    self.assertEquals(
          len(instance.instances[instance.__class__.__name__]), 5)

  def testGetStorageKey_NoCustomStorageKeySet(self):
    base = base_model.BaseModel()
    result = base.GetStorageKey_()
    expected = base.id

    self.assertEquals(result, expected)

  def testGetStorageKey_CustomStorageKeySet(self):
    class ChildClass(base_model.BaseModel):
      def __init__(self):
        super(ChildClass, self).__init__()
        self.storage_key = 'hi'

    child_class_instance = ChildClass()
    result = child_class_instance.GetStorageKey_()
    expected = child_class_instance.storage_key

    self.assertEquals(result, expected)

  def testGetAll_ObjectsNotInstantiatedNorStored(self):
    result = base_model.BaseModel.GetAll()
    expected = []
    self.assertEquals(result, expected)

  def testGetAll_ObjectsInstantiatedButNotStored(self):
    base = base_model.BaseModel()
    expected = []
    result = base_model.BaseModel.GetAll()
    self.assertEquals(result, expected)

  def testGetAll_ObjectsStored(self):
    base_instances = list(self.GenerateBaseModelInstances())

  def testGetByStorageKey_StorageKeyFound(self):
    base = base_model.BaseModel()
    base.put()

    result = base_model.BaseModel.GetByStorageKey(base.id)
    expected = base

    self.assertEquals(result, expected)

  def testGetByStorageKey_StorageKeyNotFoundObjectNotInstantiated(self):
    result = base_model.BaseModel.GetByStorageKey('unseen_storage_key')
    self.assertIsNone(result)

  def testGetByStorageKey_StorageKeyNotFoundObjectInstantiated(self):
    base_model.BaseModel()
    result = base_model.BaseModel.GetByStorageKey('unseen_storage_key')
    self.assertIsNone(result)

  def GenerateBaseModelInstances(self):
    for unused_x in xrange(5):
      base = base_model.BaseModel()
      yield base

if __name__ == '__main__':
  unittest.main()
