#!/usr/bin/python

import unittest
import author as author_model
from collections import OrderedDict


class AuthorTests(unittest.TestCase):
  def setUp(self):
    self.username = 'zack'

  def tearDown(self):
    pass

  def testConstructor(self):
    author = author_model.Author(self.username)
    self.assertEquals(author.username, self.username)
    self.assertIsInstance(author.comments, OrderedDict)
    self.assertIsInstance(author.blogposts, OrderedDict)
    self.assertIsNotNone(author.created_timestamp)
    self.assertIsNotNone(author.id)

if __name__ == '__main__':
  unittest.main()
