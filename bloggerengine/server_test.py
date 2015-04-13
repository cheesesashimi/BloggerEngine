#!/usr/bin/python

import unittest
import json
import bloggerengine
import server

import author as author_model
import base_model
import blogpost as blogpost_model
import comment as comment_model
import label as label_model


class ServerTest(unittest.TestCase):

    def setUp(self):
        self.app = server.app.test_client()

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

    def tearDown(self):
        del self.username
        del self.headline
        del self.body
        del self.label_text
        del self.authors
        del self.blogposts
        del self.comments
        del self.labels

    """Author method tests."""

    def test_author_create_successful(self):
        post_data = {'username': 'steve'}

        response = self.app.post('/author/create',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)

        self.assertEquals(response_data['author']['username'],
                          post_data['username'])

        self.assertEquals(response_data['author']['id'],
                          post_data['username'])
        self.assertIsNotNone(response_data['author']['created_timestamp'])

    def test_author_create_unsuccessful(self):
        post_data = {'username': ''}

        response = self.app.post('/author/create',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 400)

    def test_author_get_by_username_successful(self):
        post_data = {'username': 'zack'}
        response = self.app.post('/author/get_by_username',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)

        expected_author = self.authors[1].ToJson()
        self.assertEquals(response_data['author'], expected_author)

    def test_author_get_by_username_unsuccessful(self):
        post_data = {'username': ''}
        response = self.app.post('/author/get_by_username',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 400)

    def test_author_get_by_username_usernotfound(self):
        post_data = {'username': 'steve'}
        response = self.app.post('/author/get_by_username',
                                 data=json.dumps(post_data),
                                 content_type='application/json')

        self.assertEquals(response.status_code, 200)
        response_data = json.loads(response.data)

        self.assertIsNone(response_data['author'])

    def test_author_get_all_blogposts_successful(self):
        post_data = {'username': 'zack'}
        response = self.app.post('/author/get_all_blogposts',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)

        expected_blogposts = [self.blogposts[0].ToJson(),
                              self.blogposts[1].ToJson()]

        expected_author = self.authors[1].ToJson()

        self.assertEquals(response_data['blogposts'], expected_blogposts)
        self.assertEquals(response_data['author'], expected_author)

    def test_author_get_all_blogposts_unsuccessful(self):
        post_data = {'username': ''}
        response = self.app.post('/author/get_all_blogposts',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 400)

    def test_author_get_all_blogposts_usernotfound(self):
        post_data = {'username': 'steve'}
        response = self.app.post('/author/get_all_blogposts',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)
        response_data = json.loads(response.data)

        self.assertEquals(response_data['author'], None)
        self.assertEquals(response_data['blogposts'], [])

    def test_author_get_all_blogposts_noblogposts(self):
        steve = author_model.Author('steve')
        steve.put()

        post_data = {'username': 'steve'}
        response = self.app.post('/author/get_all_blogposts',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)
        response_data = json.loads(response.data)

        self.assertEquals(response_data['author'], steve.ToJson())
        self.assertEquals(response_data['blogposts'], [])

    def test_author_get_all_comments_successful(self):
        post_data = {'username': 'zack'}
        response = self.app.post('/author/get_all_comments',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)
        response_data = json.loads(response.data)

        expected_author = self.authors[1].ToJson()
        expected_comments = [self.comments[2].ToJson()]

        self.assertEquals(response_data['author'], expected_author)
        self.assertEquals(response_data['comments'], expected_comments)

    def test_author_get_all_comments_usernotfound(self):
        post_data = {'username': 'steve'}
        response = self.app.post('/author/get_all_comments',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)

    def test_author_get_all_comments_userhasnocomments(self):
        steve = author_model.Author('steve')
        steve.put()

        post_data = {'username': 'steve'}
        response = self.app.post('/author/get_all_comments',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)
        response_data = json.loads(response.data)

        expected_author = steve.ToJson()
        expected_comments = []

        self.assertEquals(response_data['author'], expected_author)
        self.assertEquals(response_data['comments'], expected_comments)

    def test_author_get_all_removed_blogposts_userfoundnoremovedposts(self):
        post_data = {'username': 'zack'}
        response = self.app.post('/author/get_all_removed_blogposts',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)
        expected_author = self.authors[1].ToJson()
        self.assertEquals(response_data['author'], expected_author)
        self.assertEquals(response_data['removed_blogposts'], [])

    def test_author_get_all_removed_blogposts_userfoundremovedposts(self):
        expected_author = self.authors[1]
        removed_blogpost = expected_author.GetBlogposts()[0]
        expected_author.RemoveBlogpost(removed_blogpost)

        post_data = {'username': 'zack'}
        response = self.app.post('/author/get_all_removed_blogposts',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertEquals(response_data['author'], expected_author.ToJson())
        self.assertEquals(response_data['removed_blogposts'],
                          [removed_blogpost.ToJson()])

    def test_author_get_all_removed_blogposts_usernotfound(self):
        post_data = {'username': 'steve'}
        response = self.app.post('/author/get_all_removed_blogposts',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)
        response_data = json.loads(response.data)

        self.assertIsNone(response_data['author'])
        self.assertEquals(response_data['removed_blogposts'], [])

    def test_author_get_all_removed_comments_userfoundnocomments(self):
        post_data = {'username': 'zack'}
        response = self.app.post('/author/get_all_removed_comments',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)
        expected_author = self.authors[1].ToJson()
        self.assertEquals(response_data['author'], expected_author)
        self.assertEquals(response_data['removed_comments'], [])

    def test_author_get_all_removed_comments_userfoundremovedcomments(self):
        expected_author = self.authors[1]
        removed_comment = expected_author.GetComments()[0]
        expected_author.RemoveComment(removed_comment)

        post_data = {'username': 'zack'}
        response = self.app.post('/author/get_all_removed_comments',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertEquals(response_data['author'], expected_author.ToJson())
        self.assertEquals(response_data['removed_comments'],
                          [removed_comment.ToJson()])

    def test_author_get_all_removed_comments_usernotfound(self):
        post_data = {'username': 'steve'}
        response = self.app.post('/author/get_all_removed_comments',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)
        response_data = json.loads(response.data)

        self.assertIsNone(response_data['author'])
        self.assertEquals(response_data['removed_comments'], [])

    def test_author_get_all_post(self):
        post_data = {}
        response = self.app.post('/author/get_all',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)
        response_data = json.loads(response.data)

        expected_authors = [self.authors[0].ToJson(),
                            self.authors[1].ToJson()]

        self.assertEquals(response_data['authors'], expected_authors)

    def test_author_get_all_get(self):
        post_data = {}
        response = self.app.get('/author/get_all',
                                content_type='application/json')
        self.assertEquals(response.status_code, 200)
        response_data = json.loads(response.data)

        expected_authors = [self.authors[0].ToJson(),
                            self.authors[1].ToJson()]

        self.assertEquals(response_data['authors'], expected_authors)

    """Blogpost tests."""

    def test_blogpost_add_label_blogpostfound(self):
        expected_blogpost = self.blogposts[0]
        post_data = {'label_text': 'something',
                     'blogpost_id': expected_blogpost.id}
        response = self.app.post('/blogpost/add_label',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)
        response_data = json.loads(response.data)

        expected_label = label_model.Label.GetByStorageKey('something')
        self.assertEquals(response_data['label'], expected_label.ToJson())
        self.assertEquals(response_data['blogpost'],
                          expected_blogpost.ToJson())
        self.assertTrue('something' in response_data['blogpost']['labels'])

    def test_blogpost_add_label_blogpostnotfound(self):
        post_data = {'label_text': 'something',
                     'blogpost_id': '12345'}
        response = self.app.post('/blogpost/add_label',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)
        response_data = json.loads(response.data)

        self.assertIsNone(response_data['label'])
        self.assertIsNone(response_data['blogpost'])

    def test_blogpost_add_label_unsuccessful(self):
        post_data = {}
        response = self.app.post('/blogpost/add_label',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 400)

    def test_blogpost_remove_label_blogpostfound(self):
        expected_blogpost = self.blogposts[0]
        expected_label = self.labels[2]

        post_data = {'label_text': expected_label.label,
                     'blogpost_id': expected_blogpost.id}
        response = self.app.post('/blogpost/remove_label',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)

        self.assertEquals(response_data['label'], expected_label.ToJson())
        self.assertEquals(response_data['blogpost'],
                          expected_blogpost.ToJson())
        self.assertTrue(expected_label.label not in
                        expected_blogpost.labels)
        self.assertTrue(expected_blogpost.id not in
                        expected_label.blogposts)

    def test_blogpost_remove_label_blogpostnotfound(self):
        expected_label = self.labels[2]

        post_data = {'label_text': expected_label.label,
                     'blogpost_id': '12345'}

        response = self.app.post('/blogpost/remove_label',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)

        self.assertEquals(response_data['label'], expected_label.ToJson())
        self.assertIsNone(response_data['blogpost'])

    def test_blogpost_remove_label_labelnotfound(self):
        expected_blogpost = self.blogposts[0]

        post_data = {'label_text': 'notfound',
                     'blogpost_id': expected_blogpost.id}

        response = self.app.post('/blogpost/remove_label',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)

        self.assertIsNone(response_data['label'])
        self.assertEquals(response_data['blogpost'],
                          expected_blogpost.ToJson())

    def test_blogpost_remove_unsuccessful(self):
        post_data = {}
        response = self.app.post('/blogpost/remove_label',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 400)

    def test_blogpost_add_comment_successful(self):
        expected_author = self.authors[0]
        expected_blogpost = self.blogposts[0]
        comment_text = 'Bienvenidos!'

        post_data = {'username': expected_author.username,
                     'comment_text': comment_text,
                     'blogpost_id': expected_blogpost.id}

        response = self.app.post('/blogpost/add_comment',
                                 data=json.dumps(post_data),
                                 content_type='application/json')

        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)

        comment_id = response_data['comment']['id']

        self.assertEquals(response_data['blogpost'],
                          expected_blogpost.ToJson())
        self.assertEquals(response_data['comment']['comment_text'],
                          comment_text)
        self.assertTrue(comment_id in response_data['blogpost']['comments'])
        self.assertTrue(comment_id in
                        response_data['comment']['author']['comments'])

    def test_blogpost_add_comment_unsuccessful(self):
        expected_author = self.authors[0]
        expected_blogpost = self.blogposts[0]
        comment_text = 'Bienvenidos!'

        post_data = {'username': expected_author.username,
                     'comment_text': comment_text}

        response = self.app.post('/blogpost/add_comment',
                                 data=json.dumps(post_data),
                                 content_type='application/json')

        self.assertEquals(response.status_code, 400)

    def test_blogpost_add_comment_blogpostnotfound(self):
        expected_author = self.authors[0]
        expected_blogpost_id = '12345'
        comment_text = 'Bienvenidos!'

        post_data = {'username': expected_author.username,
                     'comment_text': comment_text,
                     'blogpost_id': expected_blogpost_id}

        response = self.app.post('/blogpost/add_comment',
                                 data=json.dumps(post_data),
                                 content_type='application/json')

        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertIsNone(response_data['comment'])
        self.assertIsNone(response_data['blogpost'])

    def test_blogpost_remove_comment_successful(self):
        expected_blogpost = self.blogposts[0]
        expected_comment = self.comments[0]

        post_data = {'comment_id': expected_comment.id}
        response = self.app.post('/blogpost/remove_comment',
                                 data=json.dumps(post_data),
                                 content_type='application/json')

        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertEquals(response_data['removed_comment'],
                          expected_comment.ToJson())
        self.assertEquals(response_data['removed_comment']['blogpost'],
                          expected_blogpost.ToJson())
        self.assertTrue(response_data['removed_comment']['id'] in
                        response_data['removed_comment']['author']['removed_comments'])
        self.assertTrue(response_data['removed_comment']['id'] not in
                        response_data['removed_comment']['author']['comments'])

    def test_blogpost_remove_comment_commentidnotfound(self):
        expected_comment_id = '12345'

        post_data = {'comment_id': expected_comment_id}
        response = self.app.post('/blogpost/remove_comment',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)

        self.assertIsNone(response_data['blogpost'])
        self.assertIsNone(response_data['removed_comment'])

    def test_blogpost_remove_comment_unsuccessful(self):
        post_data = {'comment_id': ''}
        response = self.app.post('/blogpost/remove_comment',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 400)

    def test_blogpost_get_by_id_successful(self):
        expected_blogpost = self.blogposts[0]
        post_data = {'blogpost_id': expected_blogpost.id}
        response = self.app.post('/blogpost/get_by_id',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)

        self.assertEquals(response_data['blogpost'],
                          expected_blogpost.ToJson())

    def test_blogpost_get_by_id_unsuccessful(self):
        post_data = {'blogpost_id': ''}
        response = self.app.post('/blogpost/get_by_id',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 400)

    def test_blogpost_get_by_id_blogpostnotfound(self):
        post_data = {'blogpost_id': '12345'}
        response = self.app.post('/blogpost/get_by_id',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)

        self.assertIsNone(response_data['blogpost'])

    def test_blogpost_get_all_comments_successful(self):
        expected_blogpost = self.blogposts[0]
        expected_comments = self.comments[0]

        post_data = {'blogpost_id': expected_blogpost.id}
        response = self.app.post('/blogpost/get_all_comments',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)

        self.assertEquals(response_data['blogpost'],
                          expected_blogpost.ToJson())

        self.assertEquals(response_data['comments'],
                          [expected_comments.ToJson()])

    def test_blogpost_get_all_comments_nocomments(self):
        expected_blogpost = self.blogposts[0]
        expected_blogpost.comments = {}

        post_data = {'blogpost_id': expected_blogpost.id}
        response = self.app.post('/blogpost/get_all_comments',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)

        self.assertEquals(response_data['blogpost'],
                          expected_blogpost.ToJson())

        self.assertEquals(response_data['comments'], [])

    def test_blogpost_get_all_comments_blogpostnotfound(self):
        post_data = {'blogpost_id': '12345'}
        response = self.app.post('/blogpost/get_all_comments',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)

        self.assertIsNone(response_data['blogpost'])
        self.assertEquals(response_data['comments'], [])

    def test_blogpost_get_all_comments_unsuccessful(self):
        post_data = {'blogpost_id': ''}
        response = self.app.post('/blogpost/get_all_comments',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 400)

    def test_blogpost_get_all_labels_successful(self):
        expected_blogpost = self.blogposts[0]
        expected_labels = [self.labels[0], self.labels[2]]

        post_data = {'blogpost_id': expected_blogpost.id}
        response = self.app.post('/blogpost/get_all_labels',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)

        self.assertEquals(response_data['blogpost'],
                          expected_blogpost.ToJson())

        self.assertEquals(response_data['labels'],
                          [expected_labels[0].ToJson(),
                           expected_labels[1].ToJson()])

    def test_blogpost_get_all_labels_unsuccessful(self):
        post_data = {'blogpost_id': ''}
        response = self.app.post('/blogpost/get_all_labels',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 400)

    def test_blogpost_get_all_labels_blogpostnotfound(self):
        post_data = {'blogpost_id': '12345'}

        response = self.app.post('/blogpost/get_all_labels',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)

        self.assertIsNone(response_data['blogpost'])
        self.assertEquals(response_data['labels'], [])

    def test_blogpost_get_by_label_successful(self):
        expected_label = self.labels[2]
        expected_blogposts = self.blogposts

        post_data = {'label_text': expected_label.label}

        response = self.app.post('/blogpost/get_by_label',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)
        expected_blogposts_json = [blogpost.ToJson()
                                   for blogpost in self.blogposts]
        self.assertEquals(response_data['blogposts'],
                          expected_blogposts_json)

    def test_blogpost_get_by_label_unsuccessful(self):
        post_data = {'label_text': ''}

        response = self.app.post('/blogpost/get_by_label',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 400)

    def test_blogpost_get_by_label_labelnotfound(self):
        post_data = {'label_text': 'notfound'}
        response = self.app.post('/blogpost/get_by_label',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertEquals(response_data['blogposts'], [])

    def test_blogpost_get_all_post(self):
        post_data = {}
        response = self.app.post('/blogpost/get_all',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)

        expected_blogposts_json = [blogpost.ToJson()
                                   for blogpost in self.blogposts]
        self.assertEquals(response_data['blogposts'],
                          expected_blogposts_json)

    def test_blogpost_get_all_get(self):
        post_data = {}
        response = self.app.get('/blogpost/get_all',
                                content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)

        expected_blogposts_json = [blogpost.ToJson()
                                   for blogpost in self.blogposts]
        self.assertEquals(response_data['blogposts'],
                          expected_blogposts_json)

    def test_blogpost_remove_successful(self):
        expected_blogpost = self.blogposts[0]
        expected_author = self.authors[1]

        post_data = {'blogpost_id': expected_blogpost.id}
        response = self.app.post('/blogpost/remove',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertEquals(response_data['removed_blogpost'],
                          expected_blogpost.ToJson())
        self.assertEquals(response_data['author'],
                          response_data['removed_blogpost']['author'])
        self.assertEquals(response_data['author'],
                          expected_author.ToJson())

    def test_blogpost_remove_unsuccessful(self):
        post_data = {}
        response = self.app.post('/blogpost/remove',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 400)

    def test_blogpost_remove_blogpostnotfound(self):
        post_data = {'blogpost_id': '12345'}
        response = self.app.post('/blogpost/remove',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertIsNone(response_data['removed_blogpost'])
        self.assertIsNone(response_data['author'])

    def test_blogpost_get_all_by_username_successful(self):
        post_data = {'username': 'zack'}
        response = self.app.post('/blogpost/get_all_by_username',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)

        expected_blogposts = [self.blogposts[0].ToJson(),
                              self.blogposts[1].ToJson()]

        expected_author = self.authors[1].ToJson()

        self.assertEquals(response_data['blogposts'], expected_blogposts)
        self.assertEquals(response_data['author'], expected_author)

    def test_blogpost_get_all_by_username_unsuccessful(self):
        post_data = {'username': ''}
        response = self.app.post('/blogpost/get_all_by_username',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 400)

    def test_blogpost_get_all_by_username_usernotfound(self):
        post_data = {'username': 'steve'}
        response = self.app.post('/blogpost/get_all_by_username',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)
        response_data = json.loads(response.data)

        self.assertEquals(response_data['author'], None)
        self.assertEquals(response_data['blogposts'], [])

    def test_blogpost_get_all_by_username_noblogposts(self):
        steve = author_model.Author('steve')
        steve.put()

        post_data = {'username': 'steve'}
        response = self.app.post('/blogpost/get_all_by_username',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)
        response_data = json.loads(response.data)

        self.assertEquals(response_data['author'], steve.ToJson())
        self.assertEquals(response_data['blogposts'], [])

    """Comment Tests"""

    def test_comment_create_successful(self):
        expected_author = self.authors[0]
        expected_blogpost = self.blogposts[0]
        comment_text = 'Bienvenidos!'

        post_data = {'username': expected_author.username,
                     'comment_text': comment_text,
                     'blogpost_id': expected_blogpost.id}

        response = self.app.post('/comment/create',
                                 data=json.dumps(post_data),
                                 content_type='application/json')

        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)

        comment_id = response_data['comment']['id']

        self.assertEquals(response_data['blogpost'],
                          expected_blogpost.ToJson())
        self.assertEquals(response_data['comment']['comment_text'],
                          comment_text)
        self.assertTrue(comment_id in response_data['blogpost']['comments'])
        self.assertTrue(comment_id in
                        response_data['comment']['author']['comments'])

    def test_comment_create_unsuccessful(self):
        expected_author = self.authors[0]
        expected_blogpost = self.blogposts[0]
        comment_text = 'Bienvenidos!'

        post_data = {'username': expected_author.username,
                     'comment_text': comment_text}

        response = self.app.post('/comment/create',
                                 data=json.dumps(post_data),
                                 content_type='application/json')

        self.assertEquals(response.status_code, 400)

    def test_comment_create_blogpostnotfound(self):
        expected_author = self.authors[0]
        expected_blogpost_id = '12345'
        comment_text = 'Bienvenidos!'

        post_data = {'username': expected_author.username,
                     'comment_text': comment_text,
                     'blogpost_id': expected_blogpost_id}

        response = self.app.post('/comment/create',
                                 data=json.dumps(post_data),
                                 content_type='application/json')

        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertIsNone(response_data['comment'])
        self.assertIsNone(response_data['blogpost'])

    def test_comment_get_by_id_successful(self):
        expected_comment = self.comments[0]
        post_data = {'comment_id': expected_comment.id}
        response = self.app.post('/comment/get_by_id',
                                 data=json.dumps(post_data),
                                 content_type='application/json')

        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertEquals(response_data['comment'],
                          expected_comment.ToJson())

    def test_comment_get_by_id_notfound(self):
        post_data = {'comment_id': '12345'}
        response = self.app.post('/comment/get_by_id',
                                 data=json.dumps(post_data),
                                 content_type='application/json')

        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertIsNone(response_data['comment'])

    def test_comment_get_by_id_unsuccessful(self):
        post_data = {'comment_id': ''}
        response = self.app.post('/comment/get_by_id',
                                 data=json.dumps(post_data),
                                 content_type='application/json')

        self.assertEquals(response.status_code, 400)

    def test_comment_remove_successful(self):
        expected_blogpost = self.blogposts[0]
        expected_comment = self.comments[0]

        post_data = {'comment_id': expected_comment.id}
        response = self.app.post('/comment/remove',
                                 data=json.dumps(post_data),
                                 content_type='application/json')

        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertEquals(response_data['removed_comment'],
                          expected_comment.ToJson())
        self.assertEquals(response_data['removed_comment']['blogpost'],
                          expected_blogpost.ToJson())
        self.assertTrue(response_data['removed_comment']['id'] in
                        response_data['removed_comment']['author']['removed_comments'])
        self.assertTrue(response_data['removed_comment']['id'] not in
                        response_data['removed_comment']['author']['comments'])

    def test_comment_remove_commentidnotfound(self):
        expected_comment_id = '12345'

        post_data = {'comment_id': expected_comment_id}
        response = self.app.post('/comment/remove',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)

        self.assertIsNone(response_data['blogpost'])
        self.assertIsNone(response_data['removed_comment'])

    def test_comment_remove_unsuccessful(self):
        post_data = {'comment_id': ''}
        response = self.app.post('/comment/remove',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 400)

    def test_comment_get_all_by_username_successful(self):
        post_data = {'username': 'zack'}
        response = self.app.post('/comment/get_all_by_username',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)
        response_data = json.loads(response.data)

        expected_author = self.authors[1].ToJson()
        expected_comments = [self.comments[2].ToJson()]

        self.assertEquals(response_data['author'], expected_author)
        self.assertEquals(response_data['comments'], expected_comments)

    def test_comment_get_all_by_username_usernotfound(self):
        post_data = {'username': 'steve'}
        response = self.app.post('/comment/get_all_by_username',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)

    def test_comment_get_all_by_username_userhasnocomments(self):
        steve = author_model.Author('steve')
        steve.put()

        post_data = {'username': 'steve'}
        response = self.app.post('/comment/get_all_by_username',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)
        response_data = json.loads(response.data)

        expected_author = steve.ToJson()
        expected_comments = []

        self.assertEquals(response_data['author'], expected_author)
        self.assertEquals(response_data['comments'], expected_comments)

    def test_comments_get_all_comments_successful(self):
        post_data = {}
        response = self.app.post('/comment/get_all',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)
        response_data = json.loads(response.data)

        expected_comments_json = [comment.ToJson()
                                  for comment in self.comments]

        self.assertEquals(response_data['comments'],
                          expected_comments_json)

    def test_comments_get_all_comments_successful_get(self):
        response = self.app.get('/comment/get_all',
                                content_type='application/json')
        self.assertEquals(response.status_code, 200)
        response_data = json.loads(response.data)

        expected_comments_json = [comment.ToJson()
                                  for comment in self.comments]

        self.assertEquals(response_data['comments'],
                          expected_comments_json)

    def test_comments_get_all_comments_nocomments(self):
        comment_model.Comment.instances = {}

        post_data = {}
        response = self.app.post('/comment/get_all',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)
        response_data = json.loads(response.data)

        self.assertEquals(response_data['comments'], [])

    """Label tests."""

    def test_label_create_successful(self):
        label_text = 'welcome'
        post_data = {'label_text': label_text}

        response = self.app.post('/label/create',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)
        response_data = json.loads(response.data)

        self.assertEquals(response_data['label']['label'], label_text)

    def test_label_get_all_labelsfound(self):
        post_data = {}
        response = self.app.post('/label/get_all',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)
        response_data = json.loads(response.data)

        expected_label_json = [label.ToJson() for label in self.labels]

        self.assertEquals(response_data['labels'], expected_label_json)

    def test_label_get_all_nolabels(self):
        label_model.Label.instances = {}
        post_data = {}
        response = self.app.post('/label/get_all',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)
        response_data = json.loads(response.data)

        self.assertEquals(response_data['labels'], [])

    def test_label_get_all_get(self):
        response = self.app.get('/label/get_all',
                                content_type='application/json')
        self.assertEquals(response.status_code, 200)
        response_data = json.loads(response.data)

        expected_label_json = [label.ToJson() for label in self.labels]

        self.assertEquals(response_data['labels'], expected_label_json)

    def test_label_get_by_id_successful(self):
        expected_label = self.labels[0]
        post_data = {'label_text': expected_label.label}

        response = self.app.post('/label/get_by_id',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)
        response_data = json.loads(response.data)

        self.assertEquals(response_data['label'], expected_label.ToJson())

    def test_label_get_by_id_notfound(self):
        post_data = {'label_text': 'notfound'}

        response = self.app.post('/label/get_by_id',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)
        response_data = json.loads(response.data)

        self.assertIsNone(response_data['label'])

    def test_label_get_by_id_unsuccessful(self):
        post_data = {'label_text': ''}

        response = self.app.post('/label/get_by_id',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 400)

    def test_label_add_to_blogpost_blogpostfound(self):
        expected_blogpost = self.blogposts[0]
        post_data = {'label_text': 'something',
                     'blogpost_id': expected_blogpost.id}
        response = self.app.post('/label/add_to_blogpost',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)
        response_data = json.loads(response.data)

        expected_label = label_model.Label.GetByStorageKey('something')
        self.assertEquals(response_data['label'], expected_label.ToJson())
        self.assertEquals(response_data['blogpost'],
                          expected_blogpost.ToJson())
        self.assertTrue('something' in response_data['blogpost']['labels'])

    def test_label_add_to_blogpost_blogpostnotfound(self):
        post_data = {'label_text': 'something',
                     'blogpost_id': '12345'}
        response = self.app.post('/label/add_to_blogpost',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)
        response_data = json.loads(response.data)

        self.assertIsNone(response_data['label'])
        self.assertIsNone(response_data['blogpost'])

    def test_label_add_to_blogpost_unsuccessful(self):
        post_data = {}
        response = self.app.post('/label/add_to_blogpost',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 400)

    def test_label_remove_from_blogpost_label_blogpostfound(self):
        expected_blogpost = self.blogposts[0]
        expected_label = self.labels[2]

        post_data = {'label_text': expected_label.label,
                     'blogpost_id': expected_blogpost.id}
        response = self.app.post('/label/remove_from_blogpost',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)

        self.assertEquals(response_data['label'], expected_label.ToJson())
        self.assertEquals(response_data['blogpost'],
                          expected_blogpost.ToJson())
        self.assertTrue(expected_label.label not in
                        expected_blogpost.labels)
        self.assertTrue(expected_blogpost.id not in
                        expected_label.blogposts)

    def test_label_remove_from_blogpost_label_blogpostnotfound(self):
        expected_label = self.labels[2]

        post_data = {'label_text': expected_label.label,
                     'blogpost_id': '12345'}

        response = self.app.post('/label/remove_from_blogpost',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)

        self.assertEquals(response_data['label'], expected_label.ToJson())
        self.assertIsNone(response_data['blogpost'])

    def test_label_remove_from_blogpost_label_labelnotfound(self):
        expected_blogpost = self.blogposts[0]

        post_data = {'label_text': 'notfound',
                     'blogpost_id': expected_blogpost.id}

        response = self.app.post('/label/remove_from_blogpost',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)

        self.assertIsNone(response_data['label'])
        self.assertEquals(response_data['blogpost'],
                          expected_blogpost.ToJson())

    def test_label_remove_from_blogpost_unsuccessful(self):
        post_data = {}
        response = self.app.post('/label/remove_from_blogpost',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 400)

    def test_label_get_all_blogposts_with_label_successful(self):
        expected_label = self.labels[2]
        expected_blogposts = self.blogposts

        post_data = {'label_text': expected_label.label}

        response = self.app.post('/label/get_all_blogposts_with_label',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)
        expected_blogposts_json = [blogpost.ToJson()
                                   for blogpost in self.blogposts]
        self.assertEquals(response_data['blogposts'],
                          expected_blogposts_json)

    def test_label_get_all_blogposts_with_label_unsuccessful(self):
        post_data = {'label_text': ''}

        response = self.app.post('/label/get_all_blogposts_with_label',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 400)

    def test_label_get_all_blogposts_with_label_labelnotfound(self):
        post_data = {'label_text': 'notfound'}
        response = self.app.post('/label/get_all_blogposts_with_label',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertEquals(response_data['blogposts'], [])

    def test_label_delete_successful(self):
        expected_label = self.labels[2]
        expected_blogposts = self.blogposts

        post_data = {'label_text': expected_label.label}

        response = self.app.post('/label/delete',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)

        self.assertEquals(response_data['deleted_label'],
                          expected_label.ToJson())

        for blogpost in response_data['blogposts']:
            self.assertTrue(expected_label.label not in blogpost['labels'])

    def test_label_delete_labelnotfound(self):
        post_data = {'label_text': 'notfound'}

        response = self.app.post('/label/delete',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertIsNone(response_data['deleted_label'])
        self.assertEquals(response_data['blogposts'], [])

    def test_label_delete_labelnotassociated(self):
        label = label_model.Label('unassociated')
        label.put()

        post_data = {'label_text': label.label}

        response = self.app.post('/label/delete',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertEquals(response_data['deleted_label'],
                          label.ToJson())
        self.assertEquals(response_data['blogposts'], [])

    def test_label_delete_unsuccessful(self):
        post_data = {}

        response = self.app.post('/label/delete',
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        self.assertEquals(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
