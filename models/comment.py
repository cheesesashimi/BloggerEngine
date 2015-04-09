#!/usr/bin/python

import base_model

class Comment(base_model.BaseModel):
  def __init__(self, author, blogpost, comment):
    super(Comment, self).__init__()
    self.author = author
    self.blogpost = blogpost
    self.comment = comment
