#!/usr/bin/python

import mock
import unittest

import author as author_model
import blogpost as blogpost_model
import comment as comment_model


class CommentTest(unittest.TestCase):
  def setUp(self):
    comment_model.Comment.instances = {}
    self.author = mock.MagicMock(spec=author_model.Author)
    self.blogpost = mock.MagicMock(spec=blogpost_model.BlogPost)
    self.comment_text = 'The quick brown fox jumps over the lazy dog.'

  def tearDown(self):
    del self.author
    del self.blogpost
    del self.comment_text

  def testConstructor(self):
    comment = comment_model.Comment(self.author, self.blogpost, 
                                    self.comment_text)
    self.assertTrue(self.author.AddComment.called)
    self.assertTrue(self.blogpost.AddComment.called)
    self.assertEquals(comment.comment_text, self.comment_text)
    self.assertIsNotNone(comment.created_timestamp)
    self.assertIsNotNone(comment.id)

  def testPut(self):
    comment = comment_model.Comment(self.author, self.blogpost,
                                    self.comment_text)
    comment.put()

    self.assertTrue(
        comment.id in comment_model.Comment.instances['Comment'])

  def testGetAll(self):
    comment = comment_model.Comment(self.author, self.blogpost,
                                    self.comment_text)
    comment.put()

    result = comment_model.Comment.GetAll()
    expected = [comment]

    self.assertEquals(result, expected)

  def testGetByStorageKey(self):
    comment = comment_model.Comment(self.author, self.blogpost,
                                    self.comment_text)
    comment.put()

    result = comment_model.Comment.GetByStorageKey(comment.id)
    expected = comment

    self.assertEquals(result, expected)



if __name__ == '__main__':
  unittest.main()
