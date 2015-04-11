#/usr/bin/python

from models import author as author_model
from models import blogpost as blogpost_model
from models import comment as comment_model
from models import label as label_model


class BloggerEngine(object):

    """BloggerEngine interface."""

    def SubmitBlogPost(self, username, headline, body):
        """Submits a blog post.

        Args:
          username: string; A string representation a post author's name.
          headline: string; A string representing the blog post's headline.
          body: string; A string representing the body of the blog post.

        Returns:
          A BlogPost instance with a nested Author instance.

        """
        author = self.GetOrInsertAuthor_(username)

        post = blogpost_model.BlogPost(author, headline, body)
        post.put()

        return post

    def AddLabelToBlogPost(self, label_text, blogpost_id):
        """Adds a label to a given blog post.

        Args:
          label_text: string; The label text to add to a blog post.
          blogpost_id: string; The blog post ID to add the label to.

        Returns:
          A Label instance.

        """
        post = blogpost_model.BlogPost.GetByStorageKey(blogpost_id)
        if not post:
            return None

        label = label_model.Label.GetByStorageKey(label_text)
        if not label:
            label = label_model.Label(label_text)
            label.put()

        label.AddToBlogPost(post)
        return label

    def SubmitComment(self, username, comment_text, blogpost_id):
        """Submits a comment.

        Args:
          username: string; A string representing the comment author's username.
          comment_text: string; The comment text's content.
          blogpost_id: string; The blog post ID to add the comment to.

        """
        post = blogpost_model.BlogPost.GetByStorageKey(blogpost_id)
        if not post:
            return None

        author = self.GetOrInsertAuthor_(username)
        comment = comment_model.Comment(author, post, comment_text)
        comment.put()

        return comment

    def GetCommentsByBlogPost(self, blogpost_id):
        """Gets all comments for a given blogpost.

        Args:
          blogpost_id: string; The blogpost ID to retrieve comments from.

        Returns:
          A list of comments associated with this blogpost.

        """
        blogpost = blogpost_model.BlogPost.GetByStorageKey(blogpost_id)
        if blogpost:
            return blogpost.GetComments()

    def GetLabelsByBlogPost(self, blogpost_id):
        """Gets all labels associated with a given blogpost.

        Args:
          blogpost_id: string; The blogpost ID to retrieve labels from,

        Returns:
          A list of labels associated with this blogpost.

        """
        blogpost = blogpost_model.BlogPost.GetByStorageKey(blogpost_id)
        if blogpost:
            return blogpost.GetLabels()

    def GetCommentsOnBlogPostFilteredByUser(self, username, blogpost_id):
        """Gets all comments on a given blogpost, filtered by a username.

        Args:
          username: string; The username to retrieve comments for.

        Returns:
          A list of comments, if found.

        """
        comments = self.GetCommentsByBlogPost(blogpost_id)
        if comments:
            return [comment
                    for comment in comments
                    if comment.author.username == username]

    def GetCommentsByUsername(self, username):
        """Gets all comments for a given username.

        Args:
          username: string; A string representing the comment author's username.

        Returns:
          A list of that user's comments, if the author is found.

        """
        author = author_model.Author.GetByStorageKey(username)
        if author:
            return author.GetComments()

    def GetBlogPostsByUsername(self, username):
        """Gets all blog posts for a given username.

        Args:
          username: string; A string representing the blogpost author's username.
        Returns:
          A list of the given user's blogposts.

        """
        author = author_model.Author.GetByStorageKey(username)
        if author:
            return author.GetBlogPosts()

    def GetBlogPostById(self, blogpost_id):
        """Gets a specific blogpost by ID.

        Args:
          blogpost_id: string; The blogpost ID to retrieve.

        Returns:
          The requested blogpost or None, if not found.

        """
        return blogpost_model.BlogPost.GetByStorageKey(blogpost_id)

    def GetBlogPostsByLabel(self, label_text):
        """Gets all blogposts with a given label attached to them.

        Args:
          label_text: string; The label text to query for.

        Returns:
          The requested blogposts or None, if not found.

        """
        label = label_model.Label.GetByStorageKey(label_text)
        if label:
            return label.GetBlogPosts()

    def GetAllBlogPosts(self):
        """Gets all blog posts.

        Returns:
          A list of blog posts.

        """
        return blogpost_model.BlogPost.GetAll()

    def GetAuthorByUsername(self, username):
        """Gets an author object by username.

        Args:
          username: String; The username to look up.

        Returns:
          A populated Author instance, if found.

        """
        return author_model.Author.GetByStorageKey(username)

    def GetOrInsertAuthor_(self, username):
        """Gets or inserts an Author object by username.

        Args:
          username: String; The username to look up.

        Returns:
          A populated Author instance.

        """
        author = author_model.Author.GetByStorageKey(username)
        if author:
            return author

        author = author_model.Author(username)
        author.put()
        return author
