#!/usr/bin/python

import unittest

import interface

from models import author as author_model
from models import base_model
from models import blogpost as blogpost_model
from models import comment as comment_model
from models import label as label_model


class BloggerEngineTest(unittest.TestCase):

    def setUp(self):
        author_model.Author.instances = {}
        base_model.BaseModel.instances = {}
        blogpost_model.Blogpost.instances = {}
        comment_model.Comment.instances = {}
        label_model.Label.instances = {}

        colin = author_model.Author('colin')
        colin.put()

        zack = author_model.Author('zack')
        zack.put()

        blogpost1 = blogpost_model.Blogpost(zack,
                                            'Hi!',
                                            'Lorem ipsum...')
        blogpost1.put()

        blogpost2 = blogpost_model.Blogpost(zack,
                                            'Caps lock',
                                            'Not the caps lock!')
        blogpost2.put()

        blogpost3 = blogpost_model.Blogpost(colin,
                                            'Hi!',
                                            'Hello world.')
        blogpost3.put()

        label1 = label_model.Label('intro')
        label1.put()
        label1.AddToBlogpost(blogpost1)
        label1.AddToBlogpost(blogpost3)

        label2 = label_model.Label('funny')
        label2.put()
        label2.AddToBlogpost(blogpost2)

        label3 = label_model.Label('good stuff')
        label3.put()
        label3.AddToBlogpost(blogpost1)
        label3.AddToBlogpost(blogpost2)
        label3.AddToBlogpost(blogpost3)

        comment1 = comment_model.Comment(colin,
                                         blogpost1,
                                         '...et dolar.')
        comment1.put()

        comment2 = comment_model.Comment(colin,
                                         blogpost2,
                                         'Anything but the caps lock!')
        comment2.put()

        comment3 = comment_model.Comment(zack,
                                         blogpost3,
                                         'Welcome!')
        comment3.put()

        self.username = 'zack'
        self.headline = 'Hello world!'
        self.body = 'Yo!'
        self.label_text = 'good'

        self.authors = [colin, zack]
        self.blogposts = [blogpost1, blogpost2, blogpost3]
        self.comments = [comment1, comment2, comment3]
        self.labels = [label1, label2, label3]

        self.blogger_engine = interface.BloggerEngine()

    def tearDown(self):
        del self.blogger_engine
        del self.username
        del self.headline
        del self.body
        del self.label_text
        del self.authors
        del self.blogposts
        del self.comments
        del self.labels

    def testSubmitBlogpost(self):
        result = self.blogger_engine.SubmitBlogpost(self.username,
                                                    self.headline,
                                                    self.body)

        self.assertIsInstance(result, blogpost_model.Blogpost)
        self.assertIsInstance(result.author, author_model.Author)
        self.assertEquals(result.author.username, self.username)
        self.assertEquals(result.headline, self.headline)
        self.assertEquals(result.body, self.body)

        self.assertEquals(
            len(blogpost_model.Blogpost.instances['Blogpost']), 4)

    def testAddLabelToBlogpost_BlogpostFound(self):
        blogpost = self.blogger_engine.SubmitBlogpost(self.username,
                                                      self.headline,
                                                      self.body)

        result = self.blogger_engine.AddLabelToBlogpost(self.label_text,
                                                        blogpost.id)

        self.assertIsInstance(result, label_model.Label)
        self.assertEquals(result.label, self.label_text)

        self.assertEquals(len(label_model.Label.instances['Label']), 4)

    def testAddLabelToBlogpost_BlogpostNotFound(self):
        result = self.blogger_engine.AddLabelToBlogpost(
            self.label_text,
            '12345')

        self.assertIsNone(result)

    def testSubmitComment_BlogpostFound(self):
        blogpost = self.blogger_engine.SubmitBlogpost(self.username,
                                                      self.headline,
                                                      self.body)

        comment_author = 'colin'
        comment_text = 'Anything but the caps lock!'

        result = self. blogger_engine.SubmitComment(comment_author,
                                                    comment_text,
                                                    blogpost.id)

        self.assertIsInstance(result, comment_model.Comment)
        self.assertEquals(result.comment_text, comment_text)
        self.assertIsInstance(result.author, author_model.Author)
        self.assertEquals(result.author.username, comment_author)

    def testSubmitComment_BlogpostNotFound(self):
        comment_author = 'colin'
        comment_text = 'Anything but the caps lock!'
        blogpost_id = '12345'

        result = self.blogger_engine.SubmitComment(comment_author,
                                                   comment_text,
                                                   blogpost_id)

        self.assertIsNone(result)

    def testGetCommentsByUsername_UserFound(self):
        result = self.blogger_engine.GetCommentsByUsername('colin')
        expected = [self.comments[0], self.comments[1]]

        self.assertEquals(result, expected)

    def testGetCommentsByUsername_UserNotFound(self):
        result = self.blogger_engine.GetCommentsByUsername('steve')
        self.assertIsNone(result)

    def testGetCommentsByUsername_UserFoundNoComments(self):
        author_without_comments = author_model.Author('jon')
        author_without_comments.put()

        result = self.blogger_engine.GetCommentsByUsername('jon')
        expected = []

        self.assertEquals(result, expected)

    def testGetBlogpostsByUsername_UsernameFound(self):
        result = self.blogger_engine.GetBlogpostsByUsername('colin')
        expected = [self.blogposts[2]]
        self.assertEquals(result, expected)

    def testGetBlogpostsByUsername_UsernameNotFound(self):
        result = self.blogger_engine.GetBlogpostsByUsername('steve')
        self.assertIsNone(result)

    def testGetBlogpostsByUsername_UsernameFoundNoPosts(self):
        author_without_posts = author_model.Author('jon')
        author_without_posts.put()

        result = self.blogger_engine.GetBlogpostsByUsername('jon')
        expected = []
        self.assertEquals(result, expected)

    def testGetBlogpostById_BlogpostIdFound(self):
        for blogpost in self.blogposts:
            result = self.blogger_engine.GetBlogpostById(blogpost.id)
            expected = blogpost
            self.assertEquals(result, expected)

    def testGetBlogpostById_NoBlogpostFound(self):
        result = self.blogger_engine.GetBlogpostById('12345')
        self.assertIsNone(result)

    def testGetBlogpostsByLabel_LabelExists(self):
        result = self.blogger_engine.GetBlogpostsByLabel('funny')
        expected = [self.blogposts[1]]
        self.assertEquals(result, expected)

        result = self.blogger_engine.GetBlogpostsByLabel('intro')
        expected = [self.blogposts[0], self.blogposts[2]]
        self.assertEquals(result, expected)

        result = self.blogger_engine.GetBlogpostsByLabel('good stuff')
        expected = self.blogposts
        self.assertEquals(result, expected)

    def testGetBlogpostsByLabel_LabelDoesNotExist(self):
        result = self.blogger_engine.GetBlogpostsByLabel('nothing')
        self.assertIsNone(result)

    def testGetOrInsertAuthor_AuthorFound(self):
        result = self.blogger_engine.GetOrInsertAuthor_('zack')
        expected = self.authors[1]
        self.assertEquals(result, expected)
        self.assertEquals(len(author_model.Author.instances['Author']), 2)

    def testGetOrInsertAuthor_AuthorNotFound(self):
        result = self.blogger_engine.GetOrInsertAuthor_('jon')
        self.assertEquals(result.username, 'jon')
        self.assertIsInstance(result, author_model.Author)
        self.assertEquals(len(author_model.Author.instances['Author']), 3)

    def testGetAuthorByUsername_AuthorFound(self):
        result = self.blogger_engine.GetAuthorByUsername('zack')
        expected = self.authors[1]
        self.assertEquals(result, expected)

    def testGetAuthorByUsername_AuthorNotFound(self):
        result = self.blogger_engine.GetAuthorByUsername('steve')
        self.assertIsNone(result)

    def testGetAllBlogposts(self):
        result = self.blogger_engine.GetAllBlogposts()
        expected = self.blogposts
        self.assertEquals(result, expected)

    def testGetCommentsByBlogpost_BlogpostFound(self):
        blogpost_id = self.blogposts[0].id
        result = self.blogger_engine.GetCommentsByBlogpost(blogpost_id)
        expected = [self.comments[0]]
        self.assertEquals(result, expected)

    def testGetCommentsByBlogpost_BlogpostNotFound(self):
        blogpost_id = '12345'
        result = self.blogger_engine.GetCommentsByBlogpost(blogpost_id)
        self.assertIsNone(result)

    def testGetCommentsOnBlogpostFilteredByUser_BlogpostFound(self):
        blogpost_id = self.blogposts[0].id
        result = self.blogger_engine.GetCommentsOnBlogpostFilteredByUser(
            'colin', blogpost_id)
        expected = [self.comments[0]]
        self.assertEquals(result, expected)

    def testGetCommentsOnBlogpostFilteredByUser_NoCommentsForUser(self):
        blogpost_id = self.blogposts[0].id
        result = self.blogger_engine.GetCommentsOnBlogpostFilteredByUser(
            'zack', blogpost_id)
        expected = []
        self.assertEquals(result, expected)

    def testGetCommentsOnBlogpostFilteredByUser_BlogpostNotFound(self):
        blogpost_id = '12345'
        result = self.blogger_engine.GetCommentsOnBlogpostFilteredByUser(
            'colin', blogpost_id)
        self.assertIsNone(result)

    def testGetLabelsByBlogpost_BlogpostFound(self):
        blogpost_id = self.blogposts[0].id
        result = self.blogger_engine.GetLabelsByBlogpost(blogpost_id)
        expected = [self.labels[0], self.labels[2]]
        self.assertEquals(result, expected)

    def testGetLabelsByBlogpost_BlogpostNotFound(self):
        blogpost_id = '12345'
        result = self.blogger_engine.GetLabelsByBlogpost(blogpost_id)
        self.assertIsNone(result)

    def testGetLabelsByBlogpost_BlogpostHasNoLabels(self):
        blogpost = blogpost_model.Blogpost(self.authors[0],
                                           'Garbage Day...',
                                           '...is a very dangerous day.')
        blogpost.put()

        result = self.blogger_engine.GetLabelsByBlogpost(blogpost.id)
        expected = []
        self.assertEquals(result, [])


if __name__ == '__main__':
    unittest.main()
