#!/usr/bin/python

import mock
import unittest

import blogpost as blogpost_model
import label as label_model

from collections import OrderedDict


class LabelTest(unittest.TestCase):

    def setUp(self):
        label_model.Label.instances = {}
        self.blogpost = mock.MagicMock(spec=blogpost_model.Blogpost)

    def tearDown(self):
        del self.blogpost

    def testConstructor(self):
        label = label_model.Label('Test')
        self.assertEquals(label.label, 'test')
        self.assertIsInstance(label.blogposts, OrderedDict)

    def testAddToBlogpost_NewPost(self):
        label = label_model.Label('Test')
        self.blogpost.id = '12345'

        label.AddToBlogpost(self.blogpost)

        self.assertTrue(self.blogpost.id in label.blogposts)

        self.assertEquals(len(label.blogposts), 1)
        self.assertTrue(self.blogpost.AddLabel.called)
        self.assertEquals(self.blogpost.AddLabel.call_count, 1)

    def testAddToBlogpost_AlreadyAdded(self):
        label = label_model.Label('Test')
        self.blogpost.id = '12345'

        label.AddToBlogpost(self.blogpost)
        label.AddToBlogpost(self.blogpost)

        self.assertTrue(self.blogpost.id in label.blogposts)

        self.assertEquals(len(label.blogposts), 1)
        self.assertTrue(self.blogpost.AddLabel.called)
        self.assertEquals(self.blogpost.AddLabel.call_count, 1)

    def testRemoveFromBlogpost_LabelPresent(self):
        label = label_model.Label('Test')
        self.blogpost.id = '12345'

        label.AddToBlogpost(self.blogpost)

        label.RemoveFromBlogpost(self.blogpost)
        
        self.assertTrue(self.blogpost.id not in label.blogposts)
        self.assertTrue(self.blogpost.RemoveLabel.called)
 
    def testRemoveFromBlogpost_LabelNotPresent(self):
        label = label_model.Label('Test')
        self.blogpost.id = '12345'

        label.RemoveFromBlogpost(self.blogpost)
        
        self.assertTrue(self.blogpost.id not in label.blogposts)
        self.assertFalse(self.blogpost.RemoveLabel.called)

    def testGetBlogposts_WithPosts(self):
        label = label_model.Label('Test')
        self.blogpost.id = '12345'

        label.AddToBlogpost(self.blogpost)

        result = label.GetBlogposts()
        expected = [self.blogpost]

        self.assertEquals(result, expected)
        self.assertEquals(result[0].id, self.blogpost.id)

    def testGetBlogposts_NoPosts(self):
        label = label_model.Label('Test')

        result = label.GetBlogposts()
        expected = []

        self.assertEquals(result, expected)

    def testPut(self):
        label = label_model.Label('Test')
        label.put()

        self.assertTrue(
            label.storage_key in label_model.Label.instances['Label'])

    def testGetAll(self):
        label = label_model.Label('Test')
        label.put()

        result = label_model.Label.GetAll()
        expected = [label]

        self.assertEquals(result, expected)

    def testGetByStorageKey(self):
        label = label_model.Label('Test')
        label.put()

        result = label_model.Label.GetByStorageKey(label.storage_key)
        expected = label

        self.assertEquals(result, expected)

if __name__ == '__main__':
    unittest.main()
