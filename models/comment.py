#!/usr/bin/python

import base_model

class Comment(base_model.BaseModel):
  def __init__(self, author, blogpost, comment_text):
    """Constructor.

    Args:
      author: Author; The author of this comment.
      blogpost: BlogPost; The blogpost this comment belongs to.
      comment_text: String; The comment text.
    """
    super(Comment, self).__init__()

    author.AddComment(self)
    blogpost.AddComment(self)

    self.author = author
    self.blogpost = blogpost
    self.comment_text = comment_text
