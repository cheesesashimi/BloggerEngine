#!/usr/bin/python

import base_model


class Comment(base_model.BaseModel):

    def __init__(self, author, blogpost, comment_text):
        """Constructor.

        Args:
          author: Author; The author of this comment.
          blogpost: Blogpost; The blogpost this comment belongs to.
          comment_text: string; The comment text.

        """
        super(Comment, self).__init__()

        author.AddComment(self)
        blogpost.AddComment(self)

        self.author = author
        self.blogpost = blogpost
        self.comment_text = comment_text

    def RemoveFromBlogpost(self):
        """Removes this comment from the attached blogpost."""
        self.author.RemoveComment(self)
        self.blogpost.RemoveComment(self)

    def toJson(self):
        """Converts this object into a dictionary suitable for serialization.

        Returns:
          A dictionary.

        """
        return {
            'author': self.author.toJson(),
            'blogpost': self.blogpost.toJson(),
            'created_timestamp': str(self.created_timestamp),
            'comment_text': self.comment_text,
            'id': self.id
        }
