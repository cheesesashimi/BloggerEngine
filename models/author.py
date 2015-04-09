#!/usr/bin/python

import base_model
from collections import OrderedDict


class Author(base_model.BaseModel):
  def __init__(self, username):
    """Constructor.

    Args:
      username: String; A string of the author's username.
    """
    super(Author, self).__init__()
    self.username = username
    self.comments = OrderedDict()
    self.blogposts = OrderedDict()
