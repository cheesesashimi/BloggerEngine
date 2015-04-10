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
    self.storage_key = username
    self.username = username
    self.comments = OrderedDict()
    self.blogposts = OrderedDict()

  def AddBlogPost(self, blogpost):
    """Adds a blogpost to the author's dictionary of blogposts.

    Args:
      blogpost: BlogPost; the blog post to add.
    """
    if blogpost.id not in self.blogposts:
      self.blogposts[blogpost.id] = blogpost

  def AddComment(self, comment):
    """Adds a comment to the author's dictionary of comments.

    Args:
      comment: Comment; the comment to add.
    """
    if comment.id not in self.comments:
      self.comments[comment.id] = comment

  def GetBlogPosts(self):
    """Gets all blog posts for this user.

    Returns:
      A list of all blog posts for this user.
    """
    return self.blogposts.values()

  def GetComments(self):
    """Gets all comments for this user.

    Returns:
      A list of all comments for this user.
    """
    return self.comments.values()
