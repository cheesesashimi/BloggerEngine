#!/usr/bin/python

import unittest

from bloggerengine import base_model

from collections import OrderedDict


class BaseModelTests(unittest.TestCase):

    def setUp(self):
        base_model.BaseModel.instances = {}

    def tearDown(self):
        pass

    def test_Constructor(self):
        base = base_model.BaseModel()
        self.assertIsNotNone(base.id)
        self.assertIsInstance(base.id, str)
        self.assertIsNotNone(base.created_timestamp)
        self.assertIsNotNone(base.instances.get(base.__class__.__name__))
        self.assertIsInstance(base.instances.get(base.__class__.__name__),
                              OrderedDict)

    def test_Put_NewInstance(self):
        base = base_model.BaseModel()
        base.put()

        self.assertEquals(base,
                          base.instances[base.__class__.__name__][base.id])

    def test_Put_ExistingInstance(self):
        base = base_model.BaseModel()
        base.put()
        base.put()

        self.assertEquals(base,
                          base.instances[base.__class__.__name__][base.id])
        self.assertTrue(base.id in base.instances[base.__class__.__name__])
        self.assertEquals(len(base.instances[base.__class__.__name__]), 1)

    def test_Put_MultipleInstances(self):
        for instance in self.GenerateBaseModelInstances():
            instance.put()
            self.assertTrue(
                instance.id in instance.instances[instance.__class__.__name__])

        self.assertEquals(
            len(instance.instances[instance.__class__.__name__]), 5)

    def test_Delete_InstanceExists(self):
        base = base_model.BaseModel()
        base.put()

        self.assertEquals(len(base.instances[base.__class__.__name__]), 1)

        base.delete()

        self.assertEquals(len(base.instances[base.__class__.__name__]), 0)

    def test_Delete_InstanceDoesNotExist(self):
        base = base_model.BaseModel()

        self.assertEquals(len(base.instances[base.__class__.__name__]), 0)

        base.delete()

        self.assertEquals(len(base.instances[base.__class__.__name__]), 0)

    def test_GetStorageKey_NoCustomStorageKeySet(self):
        base = base_model.BaseModel()
        result = base.GetStorageKey_()
        expected = base.id

        self.assertEquals(result, expected)

    def test_GetStorageKey_CustomStorageKeySet(self):
        class ChildClass(base_model.BaseModel):

            def __init__(self):
                super(ChildClass, self).__init__()
                self.storage_key = 'hi'

        child_class_instance = ChildClass()
        result = child_class_instance.GetStorageKey_()
        expected = child_class_instance.storage_key

        self.assertEquals(result, expected)

    def test_GetAll_ObjectsNotInstantiatedNorStored(self):
        result = base_model.BaseModel.GetAll()
        expected = []
        self.assertEquals(result, expected)

    def test_GetAll_ObjectsInstantiatedButNotStored(self):
        base = base_model.BaseModel()
        expected = []
        result = base_model.BaseModel.GetAll()
        self.assertEquals(result, expected)

    def test_GetAll_ObjectsStored(self):
        base_instances = list(self.GenerateBaseModelInstances())

    def test_GetByStorageKey_StorageKeyFound(self):
        base = base_model.BaseModel()
        base.put()

        result = base_model.BaseModel.GetByStorageKey(base.id)
        expected = base

        self.assertEquals(result, expected)

    def test_GetByStorageKey_StorageKeyNotFoundObjectNotInstantiated(self):
        result = base_model.BaseModel.GetByStorageKey('unseen_storage_key')
        self.assertIsNone(result)

    def test_GetByStorageKey_StorageKeyNotFoundObjectInstantiated(self):
        base_model.BaseModel()
        result = base_model.BaseModel.GetByStorageKey('unseen_storage_key')
        self.assertIsNone(result)

    def GenerateBaseModelInstances(self):
        for unused_x in range(5):
            base = base_model.BaseModel()
            yield base

if __name__ == '__main__':
    unittest.main()
