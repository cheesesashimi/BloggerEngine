#!/usr/bin/python

import datetime
from collections import OrderedDict


class BaseModel(object):
  instances = {}

  def __init__(self):
    """Base model class to inherit from, to avoid duplication."""
    self.id = id(self)
    self.created_timestamp = datetime.datetime.utcnow()
    self.plural_class_name = '%ss' % self.__class__.__name__.lower()
    
    if not self.instances.get(self.plural_class_name):
      self.instances[self.plural_class_name] = OrderedDict()

  def put(self):
    storage_key = self.GetStorageKey_()
    if not self.instances[self.plural_class_name].get(storage_key):
      self.instances[self.plural_class_name][storage_key] = self
      print '%s, a %s, has been put.' % (storage_key,
                                         self.__class__.__name__)
    else:
      print '%s, a %s, has already been put.' % (storage_key,
                                                 self.__class__.__name__)
 
  def GetStorageKey_(self):
    if hasattr(self, 'storage_key'):
      return getattr(self, 'storage_key')
    return self.id

  @classmethod
  def GetAll(cls):
    plural_class_name = cls.get_plural_class_name_()
    return cls.instances[plural_class_name].values()

  @classmethod
  def GetByStorageKey(cls, storage_key):
    plural_class_name = cls.get_plural_class_name_()
    if not cls.instances.get(plural_class_name):
      return None
    return cls.instances[plural_class_name].get(storage_key, None)

  @classmethod
  def get_plural_class_name_(cls):
    return '%ss' % cls.__name__.lower()
