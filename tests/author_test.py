#!/usr/bin/python

import mock
import unittest
from bloggerengine import author as author_model
from bloggerengine import blogpost as blogpost_model
from bloggerengine import comment as comment_model

from collections import OrderedDict


class AuthorTests(unittest.TestCase):

    def setUp(self):
        author_model.Author.instances = {}
        self.username = 'zack'
        self.blogpost = self.GenerateBlogposts().next()
        self.comment = self.GenerateComments().next()

    def tearDown(self):
        del self.username
        del self.blogpost
        del self.comment

    def test_Constructor(self):
        author = author_model.Author(self.username)

        self.assertEquals(author.username, self.username)
        self.assertIsInstance(author.comments, OrderedDict)
        self.assertIsInstance(author.blogposts, OrderedDict)
        self.assertIsNotNone(author.created_timestamp)
        self.assertIsNotNone(author.id)

    def test_AddBlogpost_NewPost(self):
        author = author_model.Author(self.username)
        author.AddBlogpost(self.blogpost)

        self.assertTrue(self.blogpost.id in author.blogposts)

    def test_AddBlogpost_ExistingPost(self):
        author = author_model.Author(self.username)
        author.AddBlogpost(self.blogpost)
        author.AddBlogpost(self.blogpost)

        self.assertTrue(self.blogpost.id in author.blogposts)
        self.assertEqual(len(author.blogposts), 1)

    def test_AddBlogpost_MultiplePosts(self):
        author = author_model.Author(self.username)

        for blogpost in self.GenerateBlogposts():
            author.AddBlogpost(blogpost)
            self.assertTrue(blogpost.id in author.blogposts)

        self.assertEquals(len(author.blogposts), 5)

    def test_RemoveBlogpost_PostExists(self):
        author = author_model.Author(self.username)
        author.AddBlogpost(self.blogpost)

        self.assertTrue(self.blogpost.id in author.blogposts)

        author.RemoveBlogpost(self.blogpost)

        self.assertTrue(self.blogpost.id not in author.blogposts)
        self.assertTrue(self.blogpost.id in author.removed_blogposts)

    def test_RemoveBlogpost_PostDoesNotExist(self):
        author = author_model.Author(self.username)

        self.assertTrue(self.blogpost.id not in author.blogposts)

        author.RemoveBlogpost(self.blogpost)

        self.assertTrue(self.blogpost.id not in author.blogposts)
        self.assertTrue(self.blogpost.id not in author.removed_blogposts)

    def test_AddComment_NewComment(self):
        author = author_model.Author(self.username)
        author.AddComment(self.comment)

        self.assertTrue(self.comment.id in author.comments)

    def test_AddComment_ExistingComment(self):
        author = author_model.Author(self.username)
        author.AddComment(self.comment)
        author.AddComment(self.comment)

        self.assertEquals(len(author.comments), 1)
        self.assertTrue(self.comment.id in author.comments)

    def test_AddComment_MultipleComments(self):
        author = author_model.Author(self.username)

        for comment in self.GenerateComments():
            author.AddComment(comment)
            self.assertTrue(comment.id in author.comments)

        self.assertEqual(len(author.comments), 5)

    def test_RemoveComment_CommentPresent(self):
        author = author_model.Author(self.username)
        author.AddComment(self.comment)

        self.assertTrue(self.comment.id in author.comments)

        author.RemoveComment(self.comment)

        self.assertTrue(self.comment.id not in author.comments)

    def test_RemoveComment_CommentNotPresent(self):
        author = author_model.Author(self.username)

        self.assertTrue(self.comment.id not in author.comments)

        author.RemoveComment(self.comment)

        self.assertTrue(self.comment.id not in author.comments)

    def test_GetBlogposts_NoBlogposts(self):
        author = author_model.Author(self.username)
        result = author.GetBlogposts()
        expected = []

        self.assertEquals(result, expected)

    def test_GetBlogposts_WithBlogposts(self):
        author = author_model.Author(self.username)

        blogposts = list(self.GenerateBlogposts())
        for blogpost in blogposts:
            author.AddBlogpost(blogpost)

        result = author.GetBlogposts()
        self.assertEquals(result, blogposts)

    def test_GetComments_NoComments(self):
        author = author_model.Author(self.username)
        result = author.GetComments()
        expected = []

        self.assertEquals(result, expected)

    def test_GetComments_WithComments(self):
        author = author_model.Author(self.username)

        comments = list(self.GenerateComments())
        for comment in comments:
            author.AddComment(comment)

        result = author.GetComments()
        self.assertEquals(result, comments)

    def test_GetRemovedComments_NoComments(self):
        author = author_model.Author(self.username)
        result = author.GetRemovedComments()
        expected = []

        self.assertEquals(result, expected)

    def test_GetRemovedComments_WithComments(self):
        author = author_model.Author(self.username)

        removed_removed_comments = list(self.GenerateComments())
        for removed_comment in removed_removed_comments:
            author.removed_comments[removed_comment.id] = removed_comment

        result = author.GetRemovedComments()
        self.assertEquals(result, removed_removed_comments)

    def test_Put(self):
        author = author_model.Author(self.username)
        author.put()

        self.assertTrue(
            author.username in author_model.Author.instances['Author'])

    def test_GetAll(self):
        author = author_model.Author(self.username)
        author.put()

        result = author_model.Author.GetAll()
        expected = [author]
        self.assertEquals(result, expected)

    def test_GetByStorageKey(self):
        author = author_model.Author(self.username)
        author.put()

        result = author_model.Author.GetByStorageKey(self.username)
        expected = author
        self.assertEquals(result, expected)

    def test_ToJson_WithCommentsAndBlogposts(self):
        author = author_model.Author(self.username)

        blogposts = list(self.GenerateBlogposts())
        for blogpost in blogposts:
            author.AddBlogpost(blogpost)

        comments = list(self.GenerateComments())
        for comment in comments:
            author.AddComment(comment)

        removed_blogposts = list(self.GenerateBlogposts())
        for removed_blogpost in removed_blogposts:
            author.removed_blogposts[removed_blogpost.id] = removed_blogpost

        removed_comments = list(self.GenerateComments())
        for removed_comment in removed_comments:
            author.removed_comments[removed_comment.id] = removed_comment

        result = author.ToJson()

        for blogpost in blogposts:
            self.assertTrue(blogpost.id in result['blogposts'])

        for removed_blogpost in removed_blogposts:
            self.assertTrue(removed_blogpost.id in result['removed_blogposts'])

        for comment in comments:
            self.assertTrue(comment.id in result['comments'])

        for removed_comment in removed_comments:
            self.assertTrue(removed_comment.id in result['removed_comments'])

        self.assertIsNotNone(result['created_timestamp'])
        self.assertIsNotNone(result['id'])
        self.assertEquals(result['username'], self.username)
        self.assertEquals(result['created_timestamp'],
                          str(author.created_timestamp))

    def test_ToJson_WithoutCommentsAndBlogposts(self):
        author = author_model.Author(self.username)

        result = author.ToJson()

        self.assertEquals(result['comments'], [])
        self.assertEquals(result['blogposts'], [])
        self.assertEquals(result['removed_blogposts'], [])
        self.assertEquals(result['removed_comments'], [])
        self.assertIsNotNone(result['created_timestamp'])
        self.assertIsNotNone(result['id'])
        self.assertEquals(result['username'], self.username)
        self.assertEquals(result['created_timestamp'],
                          str(author.created_timestamp))

    def GenerateBlogposts(self):
        for unused_x in xrange(5):
            blogpost = mock.MagicMock(spec=blogpost_model.Blogpost)
            blogpost.id = id(blogpost)
            yield blogpost

    def GenerateComments(self):
        for unused_x in xrange(5):
            comment = mock.MagicMock(spec=comment_model.Comment)
            comment.id = id(comment)
            yield comment

if __name__ == '__main__':
    unittest.main()
