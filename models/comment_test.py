#!/usr/bin/python

import mock
import unittest

import author as author_model
import blogpost as blogpost_model
import comment as comment_model


class CommentTest(unittest.TestCase):
  def setUp(self):
    self.author = mock.MagicMock(spec=author_model.Author)
    self.blogpost = mock.MagicMock(spec=blogpost_model.BlogPost)
    self.comment_text = 'The quick brown fox jumps over the lazy dog.'

  def tearDown(self):
    del self.author
    del self.blogpost

  def testConstructor(self):
    comment = comment_model.Comment(self.author, self.blogpost, 
                                    self.comment_text)
    self.assertTrue(self.author.AddComment.called)
    self.assertTrue(self.blogpost.AddComment.called)
    self.assertEquals(comment.comment_text, self.comment_text)
    self.assertIsNotNone(comment.created_timestamp)
    self.assertIsNotNone(comment.id)

if __name__ == '__main__':
  unittest.main()
