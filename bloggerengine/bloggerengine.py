#/usr/bin/python

import author as author_model
import blogpost as blogpost_model
import comment as comment_model
import label as label_model


class BloggerEngine(object):

    """BloggerEngine interface."""

    def SubmitBlogpost(self, username, headline, body):
        """Submits a blog post.

        Args:
          username: string; A string representation a post author's name.
          headline: string; A string representing the blog post's headline.
          body: string; A string representing the body of the blog post.

        Returns:
          A Blogpost instance with a nested Author instance.

        """
        author = self.GetOrInsertAuthor(username)

        post = blogpost_model.Blogpost(author, headline, body)
        post.put()

        return post

    def AddLabelToBlogpost(self, label_text, blogpost_id):
        """Adds a label to a given blog post.

        Args:
          label_text: string; The label text to add to a blog post.
          blogpost_id: string; The blog post ID to add the label to.

        Returns:
          A Label instance.

        """
        post = blogpost_model.Blogpost.GetByStorageKey(blogpost_id)
        if not post:
            return None

        label = label_model.Label.GetByStorageKey(label_text)
        if not label:
            label = label_model.Label(label_text)
            label.put()

        post.AddLabel(label)
        label.AddToBlogpost(post)
        return label

    def SubmitComment(self, username, comment_text, blogpost_id):
        """Submits a comment.

        Args:
          username: string; A string representing the comment author's username.
          comment_text: string; The comment text's content.
          blogpost_id: string; The blog post ID to add the comment to.

        """
        post = blogpost_model.Blogpost.GetByStorageKey(blogpost_id)
        if not post:
            return None

        author = self.GetOrInsertAuthor(username)
        comment = comment_model.Comment(author, post, comment_text)
        comment.put()

        return comment

    def GetCommentsByBlogpost(self, blogpost_id):
        """Gets all comments for a given blogpost.

        Args:
          blogpost_id: string; The blogpost ID to retrieve comments from.

        Returns:
          A list of comments associated with this blogpost.

        """
        blogpost = blogpost_model.Blogpost.GetByStorageKey(blogpost_id)
        if blogpost:
            return blogpost.GetComments()

    def GetLabelsByBlogpost(self, blogpost_id):
        """Gets all labels associated with a given blogpost.

        Args:
          blogpost_id: string; The blogpost ID to retrieve labels from,

        Returns:
          A list of labels associated with this blogpost.

        """
        blogpost = blogpost_model.Blogpost.GetByStorageKey(blogpost_id)
        if blogpost:
            return blogpost.GetLabels()

    def GetCommentsOnBlogpostFilteredByUser(self, username, blogpost_id):
        """Gets all comments on a given blogpost, filtered by a username.

        Args:
          username: string; The username to retrieve comments for.

        Returns:
          A list of comments, if found.

        """
        comments = self.GetCommentsByBlogpost(blogpost_id)
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

    def GetCommentById(self, comment_id):
        """Gets a comment from a given comment_id.

        Args:
          comment_id: string; The comment id to get.

        Returns:
          A comment, if found. None, otherwise.

        """
        return comment_model.Comment.GetByStorageKey(comment_id)

    def GetBlogpostsByUsername(self, username):
        """Gets all blog posts for a given username.

        Args:
          username: string; A string representing the blogpost author's username.
        Returns:
          A list of the given user's blogposts.

        """
        author = author_model.Author.GetByStorageKey(username)
        if author:
            return author.GetBlogposts()

    def GetBlogpostById(self, blogpost_id):
        """Gets a specific blogpost by ID.

        Args:
          blogpost_id: string; The blogpost ID to retrieve.

        Returns:
          The requested blogpost or None, if not found.

        """
        return blogpost_model.Blogpost.GetByStorageKey(blogpost_id)

    def GetBlogpostsByLabel(self, label_text):
        """Gets all blogposts with a given label attached to them.

        Args:
          label_text: string; The label text to query for.

        Returns:
          The requested blogposts or None, if not found.

        """
        label = label_model.Label.GetByStorageKey(label_text)
        if label:
            return label.GetBlogposts()

    def GetAllBlogposts(self):
        """Gets all blog posts.

        Returns:
          A list of blog posts.

        """
        return blogpost_model.Blogpost.GetAll()

    def GetAuthorByUsername(self, username):
        """Gets an author object by username.

        Args:
          username: string; The username to look up.

        Returns:
          A populated Author instance, if found.

        """
        return author_model.Author.GetByStorageKey(username)

    def RemoveLabelFromBlogpost(self, label_text, blogpost_id):
        """Removes a label from a given blogpost.

        Args:
          label_text: string; The label to remove.
          blogpost_id: string; The blogpost to remove the label from.

        """
        label = label_model.Label.GetByStorageKey(label_text)
        blogpost = blogpost_model.Blogpost.GetByStorageKey(blogpost_id)
        if label and blogpost:
            label.RemoveFromBlogpost(blogpost)
            blogpost.RemoveLabel(label)
            return (label, blogpost)

    def RemoveCommentFromBlogpost(self, comment_id):
        """Removes a given comment from a blogpost.

        Args:
          comment_id: string; The comment ID to remove.

        """
        comment = comment_model.Comment.GetByStorageKey(comment_id)
        if not comment:
            return None

        comment.RemoveFromBlogpost()
        return comment

    def DeleteLabel(self, label_text):
        """Removes a label from all blogposts and deletes it.

        Args:
          label_text: string; The label to delete.

        """
        label = label_model.Label.GetByStorageKey(label_text)
        if not label:
            return None

        for blogpost in label.GetBlogposts():
            blogpost.RemoveLabel(label)
            label.RemoveFromBlogpost(blogpost)

        label.delete()
        return label

    def DeleteBlogpost(self, blogpost_id):
        """Removes a blogpost from the datastore and associated comments.

        Args:
          blogpost_id: string; The blogpost ID to delete.

        Returns:
          The deleted blogpost object.

        """
        blogpost = blogpost_model.Blogpost.GetByStorageKey(blogpost_id)
        if not blogpost:
            return None

        blogpost.author.RemoveBlogpost(blogpost)
        for comment in blogpost.GetComments():
            comment.RemoveFromBlogpost()

        for label in blogpost.GetLabels():
            label.RemoveFromBlogpost(blogpost)

        blogpost.delete()
        return blogpost

    def GetAllLabels(self):
        """Gets all labels.

        Returns:
          A list of all label instances.

        """
        return label_model.Label.GetAll()

    def GetOrInsertLabel(self, label_text):
        """Gets or inserts a label.

        Args:
          label_text: string; The label text to get or insert.

        Returns:
          A populated Label instance.

        """
        label = label_model.Label.GetByStorageKey(label_text)
        if not label:
            label = label_model.Label(label_text)
            label.put()
        return label

    def GetLabel(self, label_text):
        """Gets a label by it's label text.

        Args:
          label_text: string; The label text to get.

        Returns:
          A populated Label instance, if found. Otherwise, None.

        """
        return label_model.Label.GetByStorageKey(label_text)

    def GetOrInsertAuthor(self, username):
        """Gets or inserts an Author object by username.

        Args:
          username: string; The username to look up.

        Returns:
          A populated Author instance.

        """
        author = author_model.Author.GetByStorageKey(username)
        if author:
            return author

        author = author_model.Author(username)
        author.put()
        return author

    def GetAllAuthors(self):
        """Gets all authors.

        Returns:
          A list of all author instances.

        """
        return author_model.Author.GetAll()

    def GetAllComments(self):
        """Gets all comments.

        Returns:
          A list of all comment instances.

        """
        return comment_model.Comment.GetAll()
