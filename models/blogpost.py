#!/usr/bin/python

from collections import OrderedDict
import base_model


class BlogPost(base_model.BaseModel):

    def __init__(self, author, headline, body):
        """Constructor."""
        super(BlogPost, self).__init__()

        self.author = author
        self.author.AddBlogPost(self)

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

    def AddLabel(self, label):
        """Adds a label to this blog post.

        Args:
          label: Label; the label to add.

        """
        if label.label not in self.labels:
            self.labels[label.label] = label

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
