#!/usr/bin/python

import unittest
import author as author_model
from collections import OrderedDict


class BlogPost(object):
  """Stub BlogPost class."""
  def __init__(self):
    self.id = id(self)


class Comment(object):
  """Stub Comment class."""
  def __init__(self):
    self.id = id(self)    


class AuthorTests(unittest.TestCase):
  def setUp(self):
    self.username = 'zack'
    self.blogpost = BlogPost()
    self.comment = Comment()

  def tearDown(self):
    pass

  def testConstructor(self):
    author = author_model.Author(self.username)

    self.assertEquals(author.username, self.username)
    self.assertIsInstance(author.comments, OrderedDict)
    self.assertIsInstance(author.blogposts, OrderedDict)
    self.assertIsNotNone(author.created_timestamp)
    self.assertIsNotNone(author.id)

  def testAddBlogPost_NewPost(self):
    author = author_model.Author(self.username)
    author.AddBlogPost(self.blogpost)

    self.assertTrue(self.blogpost.id in author.blogposts)

  def testAddBlogPost_ExistingPost(self):
    author = author_model.Author(self.username)
    author.AddBlogPost(self.blogpost)
    author.AddBlogPost(self.blogpost)

    self.assertTrue(self.blogpost.id in author.blogposts)
    self.assertEqual(len(author.blogposts), 1)

  def testAddBlogPost_MultiplePosts(self):
    author = author_model.Author(self.username)

    for unused_x in xrange(5):
      blogpost = BlogPost()
      author.AddBlogPost(blogpost)
      self.assertTrue(blogpost.id in author.blogposts)

    self.assertEquals(len(author.blogposts), 5)

  def testAddComment_NewComment(self):
    author = author_model.Author(self.username)
    author.AddComment(self.comment)

    self.assertTrue(self.comment.id in author.comments)

  def testAddComment_ExistingComment(self):
    author = author_model.Author(self.username)
    author.AddComment(self.comment)
    author.AddComment(self.comment)

    self.assertEquals(len(author.comments), 1)
    self.assertTrue(self.comment.id in author.comments)

  def testAddComment_MultipleComments(self):
    author = author_model.Author(self.username)

    for unused_x in xrange(5):
      comment = Comment()
      author.AddComment(comment)
      self.assertTrue(comment.id in author.comments)

    self.assertEqual(len(author.comments), 5)

  def testGetBlogPosts_NoBlogPosts(self):
    author = author_model.Author(self.username)
    result = author.GetBlogPosts()
    expected = []

    self.assertEquals(result, expected)

  def testGetBlogPosts_WithBlogPosts(self):
    author = author_model.Author(self.username)

    blogposts = [BlogPost() for unused_x in xrange(5)]
    for blogpost in blogposts:
      author.AddBlogPost(blogpost)

    result = author.GetBlogPosts()
    self.assertEquals(result, blogposts)

  def testGetComments_NoComments(self):
    author = author_model.Author(self.username)
    result = author.GetComments()
    expected = []

    self.assertEquals(result, expected)

  def testGetComments_WithComments(self):
    author = author_model.Author(self.username)

    comments = [Comment() for unused_x in xrange(5)]
    for comment in comments:
      author.AddComment(comment)

    result = author.GetComments()
    self.assertEquals(result, comments) 

if __name__ == '__main__':
  unittest.main()
