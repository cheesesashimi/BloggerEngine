#!/usr/bin/python

import unittest

import bloggerengine

import author as author_model
import base_model
import blogpost as blogpost_model
import comment as comment_model
import label as label_model


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

        self.blogger_engine = bloggerengine.BloggerEngine()

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

    def test_SubmitBlogpost(self):
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

    def test_AddLabelToBlogpost_BlogpostFound(self):
        blogpost = self.blogger_engine.SubmitBlogpost(self.username,
                                                      self.headline,
                                                      self.body)

        result = self.blogger_engine.AddLabelToBlogpost(self.label_text,
                                                        blogpost.id)

        self.assertIsInstance(result, label_model.Label)
        self.assertEquals(result.label, self.label_text)
        self.assertTrue(result.label in blogpost.labels)
        self.assertTrue(blogpost.id in result.blogposts)
        self.assertEquals(len(label_model.Label.instances['Label']), 4)

    def test_AddLabelToBlogpost_BlogpostNotFound(self):
        result = self.blogger_engine.AddLabelToBlogpost(
            self.label_text,
            '12345')

        self.assertIsNone(result)

    def test_RemoveLabelFromBlogpost_BlogpostAndLabelFound(self):
        blogpost = self.blogposts[0]
        label = self.labels[0]
        result = self.blogger_engine.RemoveLabelFromBlogpost(label.label,
                                                             blogpost.id)

        self.assertTrue(label.label not in blogpost.labels)
        self.assertTrue(blogpost.id not in label.blogposts)
        self.assertEquals(result[0], label)
        self.assertEquals(result[1], blogpost)

    def test_RemoveLabelFromBlogpost_BlogpostNotFound(self):
        label = self.labels[0]
        blogpost_id = '12345'
        result = self.blogger_engine.RemoveLabelFromBlogpost(label.label,
                                                             blogpost_id)
        self.assertIsNone(result)

    def test_RemoveLabelFromBlogpost_LabelNotFound(self):
        blogpost = self.blogposts[0]
        label = 'notfound'
        result = self.blogger_engine.RemoveLabelFromBlogpost(label,
                                                             blogpost.id)
        self.assertIsNone(result)

    def test_DeleteLabel_LabelFound(self):
        label = self.labels[2]
        result = self.blogger_engine.DeleteLabel(label.label)

        for blogpost in self.blogposts:
            self.assertTrue(label.label not in blogpost.labels)

        self.assertTrue(
            label.label not in label_model.Label.instances['Label'])

        self.assertEquals(result, label)
        self.assertEquals(label.GetBlogposts(), [])

    def test_DeleteLabel_LabelFound(self):
        label = 'notfound'
        result = self.blogger_engine.DeleteLabel(label)
        self.assertIsNone(result)

    def test_DeleteBlogpost_BlogpostFound(self):
        author = self.authors[0]
        blogpost = self.blogposts[0]
        label1 = self.labels[0]
        label3 = self.labels[2]
        comment = self.comments[0]

        result = self.blogger_engine.DeleteBlogpost(blogpost.id)

        self.assertEquals(result, blogpost)

        self.assertTrue(blogpost.id not in label1.blogposts)
        self.assertTrue(blogpost.id not in label3.blogposts)

        self.assertTrue(blogpost.id not in author.blogposts)
        self.assertTrue(blogpost.id not in author.removed_blogposts)
        self.assertTrue(comment.id not in comment.author.comments)
        self.assertTrue(comment.id in comment.author.removed_comments)

        self.assertTrue(
            blogpost.id not in blogpost_model.Blogpost.instances['Blogpost'])

    def test_DeleteBlogpost_BlogpostNotFound(self):
        blogpost_id = '12345'

        result = self.blogger_engine.DeleteBlogpost(blogpost_id)

        self.assertIsNone(result)

    def test_SubmitComment_BlogpostFound(self):
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

    def test_SubmitComment_BlogpostNotFound(self):
        comment_author = 'colin'
        comment_text = 'Anything but the caps lock!'
        blogpost_id = '12345'

        result = self.blogger_engine.SubmitComment(comment_author,
                                                   comment_text,
                                                   blogpost_id)

        self.assertIsNone(result)

    def test_RemoveCommentFromBlogpost_CommentFound(self):
        comment = self.comments[0]
        blogpost = comment.blogpost

        result = self.blogger_engine.RemoveCommentFromBlogpost(comment.id)
        self.assertEquals(comment, result)
        self.assertTrue(comment.id not in blogpost.comments)
        self.assertTrue(comment.id not in comment.author.comments)
        self.assertTrue(comment.id in comment.author.removed_comments)

    def test_RemoveCommentFromBlogpost_CommentNotFound(self):
        comment_id = '12345'
        result = self.blogger_engine.RemoveCommentFromBlogpost(comment_id)
        self.assertIsNone(result)

    def test_GetCommentsByUsername_UserFound(self):
        result = self.blogger_engine.GetCommentsByUsername('colin')
        expected = [self.comments[0], self.comments[1]]

        self.assertEquals(result, expected)

    def test_GetCommentsByUsername_UserNotFound(self):
        result = self.blogger_engine.GetCommentsByUsername('steve')
        self.assertIsNone(result)

    def test_GetCommentsByUsername_UserFoundNoComments(self):
        author_without_comments = author_model.Author('jon')
        author_without_comments.put()

        result = self.blogger_engine.GetCommentsByUsername('jon')
        expected = []

        self.assertEquals(result, expected)

    def test_GetBlogpostsByUsername_UsernameFound(self):
        result = self.blogger_engine.GetBlogpostsByUsername('colin')
        expected = [self.blogposts[2]]
        self.assertEquals(result, expected)

    def test_GetBlogpostsByUsername_UsernameNotFound(self):
        result = self.blogger_engine.GetBlogpostsByUsername('steve')
        self.assertIsNone(result)

    def test_GetBlogpostsByUsername_UsernameFoundNoPosts(self):
        author_without_posts = author_model.Author('jon')
        author_without_posts.put()

        result = self.blogger_engine.GetBlogpostsByUsername('jon')
        expected = []
        self.assertEquals(result, expected)

    def test_GetBlogpostById_BlogpostIdFound(self):
        for blogpost in self.blogposts:
            result = self.blogger_engine.GetBlogpostById(blogpost.id)
            expected = blogpost
            self.assertEquals(result, expected)

    def test_GetBlogpostById_NoBlogpostFound(self):
        result = self.blogger_engine.GetBlogpostById('12345')
        self.assertIsNone(result)

    def test_GetBlogpostsByLabel_LabelExists(self):
        result = self.blogger_engine.GetBlogpostsByLabel('funny')
        expected = [self.blogposts[1]]
        self.assertEquals(result, expected)

        result = self.blogger_engine.GetBlogpostsByLabel('intro')
        expected = [self.blogposts[0], self.blogposts[2]]
        self.assertEquals(result, expected)

        result = self.blogger_engine.GetBlogpostsByLabel('good stuff')
        expected = self.blogposts
        self.assertEquals(result, expected)

    def test_GetBlogpostsByLabel_LabelDoesNotExist(self):
        result = self.blogger_engine.GetBlogpostsByLabel('nothing')
        self.assertIsNone(result)

    def test_GetOrInsertAuthorAuthorFound(self):
        result = self.blogger_engine.GetOrInsertAuthor('zack')
        expected = self.authors[1]
        self.assertEquals(result, expected)
        self.assertEquals(len(author_model.Author.instances['Author']), 2)

    def test_GetOrInsertAuthorAuthorNotFound(self):
        result = self.blogger_engine.GetOrInsertAuthor('jon')
        self.assertEquals(result.username, 'jon')
        self.assertIsInstance(result, author_model.Author)
        self.assertEquals(len(author_model.Author.instances['Author']), 3)

    def test_GetAuthorByUsername_AuthorFound(self):
        result = self.blogger_engine.GetAuthorByUsername('zack')
        expected = self.authors[1]
        self.assertEquals(result, expected)

    def test_GetAuthorByUsername_AuthorNotFound(self):
        result = self.blogger_engine.GetAuthorByUsername('steve')
        self.assertIsNone(result)

    def test_GetAllBlogposts(self):
        result = self.blogger_engine.GetAllBlogposts()
        expected = self.blogposts
        self.assertEquals(result, expected)

    def test_GetCommentsByBlogpost_BlogpostFound(self):
        blogpost_id = self.blogposts[0].id
        result = self.blogger_engine.GetCommentsByBlogpost(blogpost_id)
        expected = [self.comments[0]]
        self.assertEquals(result, expected)

    def test_GetCommentsByBlogpost_BlogpostNotFound(self):
        blogpost_id = '12345'
        result = self.blogger_engine.GetCommentsByBlogpost(blogpost_id)
        self.assertIsNone(result)

    def test_GetCommentsOnBlogpostFilteredByUser_BlogpostFound(self):
        blogpost_id = self.blogposts[0].id
        result = self.blogger_engine.GetCommentsOnBlogpostFilteredByUser(
            'colin', blogpost_id)
        expected = [self.comments[0]]
        self.assertEquals(result, expected)

    def test_GetCommentsOnBlogpostFilteredByUser_NoCommentsForUser(self):
        blogpost_id = self.blogposts[0].id
        result = self.blogger_engine.GetCommentsOnBlogpostFilteredByUser(
            'zack', blogpost_id)
        expected = []
        self.assertEquals(result, expected)

    def test_GetCommentsOnBlogpostFilteredByUser_BlogpostNotFound(self):
        blogpost_id = '12345'
        result = self.blogger_engine.GetCommentsOnBlogpostFilteredByUser(
            'colin', blogpost_id)
        self.assertIsNone(result)

    def test_GetLabelsByBlogpost_BlogpostFound(self):
        blogpost_id = self.blogposts[0].id
        result = self.blogger_engine.GetLabelsByBlogpost(blogpost_id)
        expected = [self.labels[0], self.labels[2]]
        self.assertEquals(result, expected)

    def test_GetLabelsByBlogpost_BlogpostNotFound(self):
        blogpost_id = '12345'
        result = self.blogger_engine.GetLabelsByBlogpost(blogpost_id)
        self.assertIsNone(result)

    def test_GetLabelsByBlogpost_BlogpostHasNoLabels(self):
        blogpost = blogpost_model.Blogpost(self.authors[0],
                                           'Garbage Day...',
                                           '...is a very dangerous day.')
        blogpost.put()

        result = self.blogger_engine.GetLabelsByBlogpost(blogpost.id)
        expected = []
        self.assertEquals(result, [])

    def test_GetCommentById_CommentFound(self):
        expected_comment = self.comments[0]
        result = self.blogger_engine.GetCommentById(expected_comment.id)
        self.assertEquals(result, expected_comment)

    def test_GetCommentById_CommentNotFound(self):
        expected_comment_id = '12345'
        result = self.blogger_engine.GetCommentById(expected_comment_id)
        self.assertIsNone(result)

    def test_GetAllLabels(self):
        result = self.blogger_engine.GetAllLabels()
        expected = self.labels
        self.assertEquals(result, expected)

    def test_GetOrInsertLabel_LabelFound(self):
        result = self.blogger_engine.GetOrInsertLabel('good stuff')
        expected = self.labels[2]
        self.assertEquals(result, expected)
        self.assertEquals(len(label_model.Label.instances['Label']), 3)

    def test_GetOrInsertLabel_LabelNotFound(self):
        result = self.blogger_engine.GetOrInsertLabel('new')
        self.assertEquals(result.label, 'new')
        self.assertIsInstance(result, label_model.Label)
        self.assertEquals(len(label_model.Label.instances['Label']), 4)

    def test_GetLabel_LabelFound(self):
        expected_label = self.labels[2]
        result = self.blogger_engine.GetLabel('good stuff')
        self.assertEquals(result, expected_label)

    def test_GetLabel_LabelNotFound(self):
        label_text = 'notfound'
        result = self.blogger_engine.GetLabel(label_text)
        self.assertIsNone(result)

    def test_GetAllAuthors(self):
        result = self.blogger_engine.GetAllAuthors()
        self.assertEquals(result, self.authors)

    def test_GetAllComments(self):
        result = self.blogger_engine.GetAllComments()
        self.assertEquals(result, self.comments)

if __name__ == '__main__':
    unittest.main()
