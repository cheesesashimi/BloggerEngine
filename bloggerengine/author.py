#!/usr/bin/python

from bloggerengine import base_model
from collections import OrderedDict


class Author(base_model.BaseModel):

    def __init__(self, username):
        """Constructor.

        Args:
          username: string; A string of the author's username.

        """
        super(Author, self).__init__()
        self.username = username.lower()
        self.storage_key = self.username
        self.comments = OrderedDict()
        self.blogposts = OrderedDict()
        self.removed_blogposts = OrderedDict()
        self.removed_comments = OrderedDict()

    def AddBlogpost(self, blogpost):
        """Adds a blogpost to the author's dictionary of blogposts.

        Args:
          blogpost: Blogpost; the blog post to add.

        """
        if blogpost.id not in self.blogposts:
            self.blogposts[blogpost.id] = blogpost

    def RemoveBlogpost(self, blogpost):
        """Removes a blogpost from the author's dictionary of blogposts.

        Args:
          blogpost: Blogpost; the blogpost to remove.

        """
        if blogpost.id in self.blogposts:
            self.removed_blogposts[blogpost.id] = blogpost
            del self.blogposts[blogpost.id]

    def AddComment(self, comment):
        """Adds a comment to the author's dictionary of comments.

        Args:
          comment: Comment; the comment to add.

        """
        if comment.id not in self.comments:
            self.comments[comment.id] = comment

    def RemoveComment(self, comment):
        """Removes a comment from the author's dictionary of blogposts.

        Args:
          comment: Comment; the comment to remove.

        """
        if comment.id in self.comments:
            self.removed_comments[comment.id] = comment
            del self.comments[comment.id]

    def GetBlogposts(self):
        """Gets all blog posts for this user.

        Returns:
          A list of all blog posts for this user.

        """
        return list(self.blogposts.values())

    def GetRemovedBlogposts(self):
        """Gets a list of removed blogposts.

        Returns:
          A list of removed blogposts.

        """
        return list(self.removed_blogposts.values())

    def GetComments(self):
        """Gets all comments for this user.

        Returns:
          A list of all comments for this user.

        """
        return list(self.comments.values())

    def GetRemovedComments(self):
        """Gets a list of removed comments.

        Returns:
          A list of all removed comments.

        """
        return list(self.removed_comments.values())

    def ToJson(self):
        """Converts this object into a dictionary suitable for serialization.

        Returns:
          A dictionary.

        """
        return {
            'username': self.username,
            'id': self.storage_key,
            'created_timestamp': str(self.created_timestamp),
            'comments': [comment.id for comment in self.GetComments()],
            'blogposts': [blogpost.id for blogpost in self.GetBlogposts()],
            'removed_blogposts': [blogpost.id
                                  for blogpost in
                                  self.removed_blogposts.values()],
            'removed_comments': [comment.id
                                 for comment in
                                 self.removed_comments.values()]
        }
