#!/usr/bin/python

from collections import OrderedDict
import base_model


class Blogpost(base_model.BaseModel):

    def __init__(self, author, headline, body):
        """Constructor."""
        super(Blogpost, self).__init__()

        self.author = author
        self.author.AddBlogpost(self)

        self.headline = headline
        self.body = body

        self.comments = OrderedDict()
        self.labels = OrderedDict()

    def AddComment(self, comment):
        """Adds a comment to this blog post.

        Args:
          comment: Comment; the comment to add.

        """
        if comment.id not in self.comments:
            self.comments[comment.id] = comment

    def RemoveComment(self, comment):
        """Removes a comment from this blog post.

        Args:
          comment: Comment; the comment to remove.
        """
        if comment.id in self.comments:
            del self.comments[comment.id]

    def AddLabel(self, label):
        """Adds a label to this blog post.

        Args:
          label: Label; the label to add.

        """
        if label.label not in self.labels:
            self.labels[label.label] = label

    def RemoveLabel(self, label):
        """Removes a label from this blog post.

        Args:
          label: Label; the label to remove.

        """
        if label.label in self.labels:
            del self.labels[label.label]

    def GetComments(self):
        """Gets all the comments associated with this blog post.

        Returns:
          A list of comments.

        """
        return self.comments.values()

    def GetLabels(self):
        """Gets all labels associated with this blog post.

        Returns:
          A list of labels.

        """
        return self.labels.values()
