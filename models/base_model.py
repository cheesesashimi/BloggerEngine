#!/usr/bin/python

import datetime
from collections import OrderedDict


class BaseModel(object):
    instances = {}

    def __init__(self):
        """Base model class to inherit from, to avoid duplication."""
        self.id = id(self)
        self.created_timestamp = datetime.datetime.utcnow()

        if self.__class__.__name__ not in self.instances:
            self.instances[self.__class__.__name__] = OrderedDict()

    def put(self):
        """Stores the object in the instances dictionary, if not present."""
        storage_key = self.GetStorageKey_()
        if storage_key not in self.instances[self.__class__.__name__]:
            self.instances[self.__class__.__name__][storage_key] = self

    def delete(self):
        """Deletes the object from the instances dictionary, if present."""
        storage_key = self.GetStorageKey_()
        if storage_key in self.instances[self.__class__.__name__]:
            del self.instances[self.__class__.__name__][storage_key]

    def GetStorageKey_(self):
        """Gets the storage key to use.

        Returns:
          The storage key as a string.

        """
        if hasattr(self, 'storage_key'):
            return getattr(self, 'storage_key')
        return self.id

    @classmethod
    def GetAll(cls):
        """Gets all stored instances of this object.

        Returns:
          A list of object instances, if found. Otherwise, an empty list.

        """
        return cls.instances.get(cls.__name__, {}).values()

    @classmethod
    def GetByStorageKey(cls, storage_key):
        """Gets a specific instance of this object.

        Returns:
          A specific model instance, if found. Otherwise, None.

        """
        return cls.instances.get(cls.__name__, {}).get(storage_key, None)
