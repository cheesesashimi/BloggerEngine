#!/usr/bin/python

from collections import OrderedDict
import base_model


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
        return self.blogposts.values()
