#!/usr/bin/python

import mock
import unittest
import author as author_model
import blogpost as blogpost_model
import comment as comment_model

from collections import OrderedDict


class AuthorTests(unittest.TestCase):
  def setUp(self):
    author_model.Author.instances = {}
    self.username = 'zack'
    self.blogpost = self.GenerateBlogPosts().next()
    self.comment = self.GenerateComments().next()

  def tearDown(self):
    del self.username
    del self.blogpost
    del self.comment

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

    for blogpost in self.GenerateBlogPosts():
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

    for comment in self.GenerateComments():
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

    blogposts = list(self.GenerateBlogPosts())
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

    comments = list(self.GenerateComments())
    for comment in comments:
      author.AddComment(comment)

    result = author.GetComments()
    self.assertEquals(result, comments)

  def testPut(self):
    author = author_model.Author(self.username)
    author.put()

    self.assertTrue(
        author.username in author_model.Author.instances['Author'])

  def testGetAll(self):
    author = author_model.Author(self.username)
    author.put()

    result = author_model.Author.GetAll()
    expected = [author]
    self.assertEquals(result, expected)

  def testGetByStorageKey(self):
    author = author_model.Author(self.username)
    author.put()

    result = author_model.Author.GetByStorageKey(self.username)
    expected = author
    self.assertEquals(result, expected)

  def GenerateBlogPosts(self):
    for unused_x in xrange(5):
      blogpost = mock.MagicMock(spec=blogpost_model.BlogPost)
      blogpost.id = id(blogpost)
      yield blogpost

  def GenerateComments(self):
    for unused_x in xrange(5):
      comment = mock.MagicMock(spec=comment_model.Comment)
      comment.id = id(comment)
      yield comment

if __name__ == '__main__':
  unittest.main()
