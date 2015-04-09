#!/usr/bin/python

import datetime


class BaseModel(object):
  def __init__(self):
    """Base model class to inherit from, to avoid duplication."""
    self.created_timestamp = datetime.datetime.now()
    self.id = id(self)
