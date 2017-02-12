#!/usr/bin/python

from collections import OrderedDict
from bloggerengine import base_model


class Label(base_model.BaseModel):

    def __init__(self, label_text):
        """Constructor.

        Args:
          label_text: string; The text to make up the label.

        """
        super(Label, self).__init__()
        self.label = label_text.lower()
        self.storage_key = self.label
        self.blogposts = OrderedDict()

    def AddToBlogpost(self, blogpost):
        """Adds this label to a given blogpost.

        Args:
          blogpost: Blogpost; The blogpost to remove this label from.

        """
        if blogpost.id not in self.blogposts:
            self.blogposts[blogpost.id] = blogpost
            blogpost.AddLabel(self)

    def RemoveFromBlogpost(self, blogpost):
        """Removes this label from a given blogpost.

        Args:
          blogpost: Blogpost; The blogpost to remove this label from.

        """
        if blogpost.id in self.blogposts:
            del self.blogposts[blogpost.id]
            blogpost.RemoveLabel(self)

    def GetBlogposts(self):
        """Gets all blogposts with this label.

        Returns:
          A list of Blogposts.

        """
        return list(self.blogposts.values())

    def ToJson(self):
        """Converts this object into a dictionary suitable for serialization.

        Returns:
          A dictionary.

        """
        return {
            'label': self.label,
            'id': self.storage_key,
            'created_timestamp': str(self.created_timestamp),
            'blogposts': [blogpost.id for blogpost in self.GetBlogposts()]
        }
