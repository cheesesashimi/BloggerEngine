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
        self.author.id = str(id(self.author))
        self.blogpost = mock.MagicMock(spec=blogpost_model.Blogpost)
        self.comment_text = 'The quick brown fox jumps over the lazy dog.'

    def tearDown(self):
        del self.author
        del self.blogpost
        del self.comment_text

    def test_Constructor(self):
        comment = comment_model.Comment(self.author, self.blogpost,
                                        self.comment_text)
        self.assertTrue(self.author.AddComment.called)
        self.assertTrue(self.blogpost.AddComment.called)
        self.assertEquals(comment.comment_text, self.comment_text)
        self.assertIsNotNone(comment.created_timestamp)
        self.assertIsNotNone(comment.id)

    def test_RemoveFromBlogpost(self):
        comment = comment_model.Comment(self.author, self.blogpost,
                                        self.comment_text)
        comment.RemoveFromBlogpost()

        self.assertTrue(self.author.AddComment.called)
        self.assertTrue(self.blogpost.RemoveComment.called)

    def test_Put(self):
        comment = comment_model.Comment(self.author, self.blogpost,
                                        self.comment_text)
        comment.put()

        self.assertTrue(
            comment.id in comment_model.Comment.instances['Comment'])

    def test_GetAll(self):
        comment = comment_model.Comment(self.author, self.blogpost,
                                        self.comment_text)
        comment.put()

        result = comment_model.Comment.GetAll()
        expected = [comment]

        self.assertEquals(result, expected)

    def test_GetByStorageKey(self):
        comment = comment_model.Comment(self.author, self.blogpost,
                                        self.comment_text)
        comment.put()

        result = comment_model.Comment.GetByStorageKey(comment.id)
        expected = comment

        self.assertEquals(result, expected)

    def test_ToJson(self):
        comment = comment_model.Comment(self.author, self.blogpost,
                                        self.comment_text)

        self.author.toJson.return_value = {
            'username': 'zack',
            'id': self.author.id
        }

        self.blogpost.toJson.return_value = {
            'headline': 'hi',
            'body': 'hello',
            'id': str(id(self.blogpost))
        }

        result = comment.toJson()

        self.assertTrue(self.author.toJson.called)
        self.assertTrue(self.blogpost.toJson.called)
        self.assertEquals(result['author'], self.author.toJson.return_value)
        self.assertEquals(result['blogpost'],
                          self.blogpost.toJson.return_value)
        self.assertEquals(result['created_timestamp'],
                          str(comment.created_timestamp))
        self.assertEquals(result['comment_text'],
                          comment.comment_text)
        self.assertEquals(result['id'],
                          comment.id)

if __name__ == '__main__':
    unittest.main()
