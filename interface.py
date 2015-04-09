#/usr/bin/python


class BloggerEngine(object):
  """BloggerEngine interface."""
  def SubmitBlogPost(self, username, headline, body):
    """Submits a blog post.

    Args:
      username: string; A string representation a post author's name.
      headline: string; A string representing the blog post's headline.
      body: string; A string representing the body of the blog post.
    """
    pass
    
  def AddLabelToBlogPost(self, label_text, blogpost_id):
    """Adds a label to a given blog post.

    Args:
      label_text: string; The label text to add to a blog post.
      blogpost_id: string; The blog post ID to add the label to.
    """
    pass

  def SubmitComment(self, username, comment_text, blogpost_id):
    """Submits a comment.

    Args:
      username: string; A string representing the comment author's username.
      comment_text: string; The comment text's content.
      blogpost_id: string; The blog post ID to add the comment to.
    """
    pass

  def GetCommentsByUsername(self, username):
    """Gets all comments for a given username.

    Args:
      username: string; A string representing the comment author's username.

    Returns:
      A list of that user's comments.
    """
    pass

  def GetBlogPostsByUsername(self, username):
    """Gets all blog posts for a given username.

    Args:
      username: string; A string representing the blogpost author's username.
    Returns:
      A list of the given user's blogposts.
    """
    pass

  def GetBlogPostById(self, blogpost_id):
    """Gets a specific blogpost by ID.

    Args:
      blogpost_id: string; The blogpost ID to retrieve.

    Returns:
      The requested blogpost or None, if not found.
    """
    pass

  def GetBlogPostsByLabel(self, label_text):
    """Gets all blogposts with a given label attached to them.

    Args:
      label_tset: string; The label text to query for.

    Returns:
      The requested blogposts or None, if not found.
    """
    pass
