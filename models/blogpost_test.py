#!/usr/bin/python

import unittest
import mock

import author as author_model
import blogpost as blogpost_model
import comment as comment_model
import label as label_model

from collections import OrderedDict


class BlogpostTests(unittest.TestCase):

    def setUp(self):
        blogpost_model.Blogpost.instances = {}
        self.author = mock.MagicMock(spec=author_model.Author)
        self.comment = self.GenerateComments().next()
        self.label = self.GenerateLabels().next()
        self.headline = 'Hello world!'
        self.body = 'I\'m a blog post!'

    def tearDown(self):
        del self.author
        del self.comment
        del self.label
        del self.headline
        del self.body

    def testConstructor(self):
        blogpost = blogpost_model.Blogpost(self.author, self.headline,
                                           self.body)

        self.assertTrue(self.author.AddBlogpost.called)
        self.assertEquals(self.headline, blogpost.headline)
        self.assertEquals(self.body, blogpost.body)
        self.assertIsInstance(blogpost.comments, OrderedDict)
        self.assertIsInstance(blogpost.labels, OrderedDict)
        self.assertIsNotNone(blogpost.created_timestamp)
        self.assertIsNotNone(blogpost.id)

    def testAddComment(self):
        blogpost = blogpost_model.Blogpost(self.author, self.headline,
                                           self.body)
        blogpost.AddComment(self.comment)

        self.assertTrue(self.comment.id in blogpost.comments)

    def testRemoveComment_CommentFound(self):
        blogpost = blogpost_model.Blogpost(self.author, self.headline,
                                           self.body)
        blogpost.AddComment(self.comment)

        self.assertTrue(self.comment.id in blogpost.comments)

        blogpost.RemoveComment(self.comment)

        self.assertTrue(self.comment.id not in blogpost.comments)

    def testRemoveComment_CommentNotFound(self):
        blogpost = blogpost_model.Blogpost(self.author, self.headline,
                                           self.body)

        self.assertTrue(self.comment.id not in blogpost.comments)

        blogpost.RemoveComment(self.comment)

        self.assertTrue(self.comment.id not in blogpost.comments)

    def testAddComment_MultipleComments(self):
        blogpost = blogpost_model.Blogpost(self.author, self.headline,
                                           self.body)
        for comment in self.GenerateComments():
            blogpost.AddComment(comment)
            self.assertTrue(comment.id in blogpost.comments)

        self.assertEquals(len(blogpost.comments), 5)

    def testAddLabel(self):
        blogpost = blogpost_model.Blogpost(self.author, self.headline,
                                           self.body)
        blogpost.AddLabel(self.label)

        self.assertTrue(self.label.label in blogpost.labels)
        self.assertTrue(self.label.AddToBlogpost.called)

    def testAddLabel_MultipleLabels(self):
        blogpost = blogpost_model.Blogpost(self.author, self.headline,
                                           self.body)

        for label in self.GenerateLabels():
            blogpost.AddLabel(label)
            self.assertTrue(label.label in blogpost.labels)
            self.assertTrue(label.AddToBlogpost.called)

        self.assertEquals(len(blogpost.labels), 5)

    def testRemoveLabel_LabelFound(self):
        blogpost = blogpost_model.Blogpost(self.author, self.headline,
                                           self.body)

        blogpost.AddLabel(self.label)

        self.assertTrue(self.label.label in blogpost.labels)

        blogpost.RemoveLabel(self.label)

        self.assertTrue(self.label.label not in blogpost.labels)
        self.assertTrue(self.label.RemoveFromBlogpost.called)

    def testRemoveLabel_LabelNotFound(self):
        blogpost = blogpost_model.Blogpost(self.author, self.headline,
                                           self.body)

        self.assertTrue(self.label.label not in blogpost.labels)

        blogpost.RemoveLabel(self.label)

        self.assertTrue(self.label.label not in blogpost.labels)

    def testGetComments_WithComments(self):
        blogpost = blogpost_model.Blogpost(self.author, self.headline,
                                           self.body)
        blogpost.AddComment(self.comment)

        result = blogpost.GetComments()
        expected = [self.comment]

        self.assertEquals(result, expected)

    def testGetComments_NoComments(self):
        blogpost = blogpost_model.Blogpost(self.author, self.headline,
                                           self.body)
        result = blogpost.GetComments()
        expected = []

        self.assertEquals(result, expected)

    def testGetLabels_NoLabels(self):
        blogpost = blogpost_model.Blogpost(self.author, self.headline,
                                           self.body)
        result = blogpost.GetLabels()
        expected = []
        self.assertEquals(result, expected)

    def testGetLabels_WithLabels(self):
        blogpost = blogpost_model.Blogpost(self.author, self.headline,
                                           self.body)
        blogpost.AddLabel(self.label)
        result = blogpost.GetLabels()
        expected = [self.label]
        self.assertEquals(result, expected)

    def testPut(self):
        blogpost = blogpost_model.Blogpost(self.author, self.headline,
                                           self.body)
        blogpost.put()

        self.assertTrue(
            blogpost.id in blogpost_model.Blogpost.instances['Blogpost'])
        self.assertEquals(len(blogpost_model.Blogpost.instances['Blogpost']),
                          1)

    def testGetAll(self):
        blogpost = blogpost_model.Blogpost(self.author, self.headline,
                                           self.body)
        blogpost.put()

        result = blogpost_model.Blogpost.GetAll()
        expected = [blogpost]

        self.assertEquals(result, expected)

    def testGetByStorageKey(self):
        blogpost = blogpost_model.Blogpost(self.author, self.headline,
                                           self.body)
        blogpost.put()

        result = blogpost_model.Blogpost.GetByStorageKey(blogpost.id)
        expected = blogpost

        self.assertEquals(result, expected)

    def GenerateComments(self):
        # I used a generator here since I needed to set the id property,
        # otherwise, I would've just used a list comprehension.
        for unused_x in xrange(5):
            comment = mock.MagicMock(spec=comment_model.Comment)
            comment.id = id(comment)
            yield comment

    def GenerateLabels(self):
        # I used a generator here since I needed to set the label property,
        # otherwise, I would've just used a list comprehension.
        for unused_x in xrange(5):
            label = mock.MagicMock(spec=label_model.Label)
            label.label = str(id(label))
            yield label

if __name__ == '__main__':
    unittest.main()
