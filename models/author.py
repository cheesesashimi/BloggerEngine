#!/usr/bin/python

import base_model
from collections import OrderedDict


class Author(base_model.BaseModel):

    def __init__(self, username):
        """Constructor.

        Args:
          username: string; A string of the author's username.

        """
        super(Author, self).__init__()
        self.storage_key = username
        self.username = username
        self.comments = OrderedDict()
        self.blogposts = OrderedDict()

    def AddBlogpost(self, blogpost):
        """Adds a blogpost to the author's dictionary of blogposts.

        Args:
          blogpost: Blogpost; the blog post to add.

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

    def DeleteBlogpost(self, blogpost):
        """Deletes a blogpost from the author's dictionary of blogposts.

        Args:
          blogpost: Blogpsot; the blogpost to delete.
        """
        if blogpost.id in self.blogposts:
            del self.blogposts[blogpost.id]

    def DeleteComment(self, comment):
        """Deletes a comment from the author's dictionary of blogposts.

        Args:
          comment: Comment; the comment to delete.
        """
        if comment.id in self.comments:
            del self.comments[comment.id]

    def GetBlogposts(self):
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
