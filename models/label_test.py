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
        self.blogpost.id = str(id(self.blogpost))

    def tearDown(self):
        del self.blogpost

    def test_Constructor(self):
        label = label_model.Label('Test')
        self.assertEquals(label.label, 'test')
        self.assertIsInstance(label.blogposts, OrderedDict)

    def test_AddToBlogpost_NewPost(self):
        label = label_model.Label('Test')
        self.blogpost.id = '12345'

        label.AddToBlogpost(self.blogpost)

        self.assertTrue(self.blogpost.id in label.blogposts)

        self.assertEquals(len(label.blogposts), 1)
        self.assertTrue(self.blogpost.AddLabel.called)
        self.assertEquals(self.blogpost.AddLabel.call_count, 1)

    def test_AddToBlogpost_AlreadyAdded(self):
        label = label_model.Label('Test')
        self.blogpost.id = '12345'

        label.AddToBlogpost(self.blogpost)
        label.AddToBlogpost(self.blogpost)

        self.assertTrue(self.blogpost.id in label.blogposts)

        self.assertEquals(len(label.blogposts), 1)
        self.assertTrue(self.blogpost.AddLabel.called)
        self.assertEquals(self.blogpost.AddLabel.call_count, 1)

    def test_RemoveFromBlogpost_LabelPresent(self):
        label = label_model.Label('Test')
        self.blogpost.id = '12345'

        label.AddToBlogpost(self.blogpost)

        label.RemoveFromBlogpost(self.blogpost)

        self.assertTrue(self.blogpost.id not in label.blogposts)
        self.assertTrue(self.blogpost.RemoveLabel.called)

    def test_RemoveFromBlogpost_LabelNotPresent(self):
        label = label_model.Label('Test')
        self.blogpost.id = '12345'

        label.RemoveFromBlogpost(self.blogpost)

        self.assertTrue(self.blogpost.id not in label.blogposts)
        self.assertFalse(self.blogpost.RemoveLabel.called)

    def test_GetBlogposts_WithPosts(self):
        label = label_model.Label('Test')
        self.blogpost.id = '12345'

        label.AddToBlogpost(self.blogpost)

        result = label.GetBlogposts()
        expected = [self.blogpost]

        self.assertEquals(result, expected)
        self.assertEquals(result[0].id, self.blogpost.id)

    def test_GetBlogposts_NoPosts(self):
        label = label_model.Label('Test')

        result = label.GetBlogposts()
        expected = []

        self.assertEquals(result, expected)

    def test_Put(self):
        label = label_model.Label('Test')
        label.put()

        self.assertTrue(
            label.storage_key in label_model.Label.instances['Label'])

    def test_GetAll(self):
        label = label_model.Label('Test')
        label.put()

        result = label_model.Label.GetAll()
        expected = [label]

        self.assertEquals(result, expected)

    def test_GetByStorageKey(self):
        label = label_model.Label('Test')
        label.put()

        result = label_model.Label.GetByStorageKey(label.storage_key)
        expected = label

        self.assertEquals(result, expected)

    def test_ToJson_WithBlogposts(self):
        label = label_model.Label('Test')
        label.blogposts[self.blogpost.id] = self.blogpost

        result = label.toJson()

        self.assertEquals(result['blogposts'], [self.blogpost.id])
        self.assertEquals(result['label'], label.label)
        self.assertEquals(result['id'], label.storage_key)
        self.assertEquals(result['created_timestamp'],
                          str(label.created_timestamp))

    def test_ToJson_NoBlogposts(self):
        label = label_model.Label('Test')

        result = label.toJson()

        self.assertEquals(result['blogposts'], [])
        self.assertEquals(result['label'], label.label)
        self.assertEquals(result['id'], label.storage_key)
        self.assertEquals(result['created_timestamp'],
                          str(label.created_timestamp))

if __name__ == '__main__':
    unittest.main()
