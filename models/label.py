#!/usr/bin/python

from collections import OrderedDict
import base_model


class Label(base_model.BaseModel):
  def __init__(self, label):
    super(Label, self).__init__()
    self.label = label.lower()
    self.blogposts = OrderedDict()
