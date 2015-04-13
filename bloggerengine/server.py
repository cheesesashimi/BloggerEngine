#!/usr/bin/python

import bloggerengine
from flask import Flask, abort, json, jsonify, request

app = Flask('BloggerEngine')

blogger_engine = bloggerengine.BloggerEngine()


@app.route('/')
def index():
    return 'Index Page'

"""Author methods."""


@app.route('/author/create', methods=['POST'])
def author_create():
    content = request.get_json()
    username = content.get('username')
    if not username:
        abort(400)

    return jsonify({
        'author': blogger_engine.GetOrInsertAuthor(username).toJson()
    })


@app.route('/author/get_by_username', methods=['POST'])
def author_get_by_username():
    content = request.get_json()
    username = content.get('username')
    if not username:
        abort(400)

    author = blogger_engine.GetAuthorByUsername(username)
    if author:
        author = author.toJson()
    else:
        author = None

    return jsonify({
        'author': author
    })


@app.route('/author/get_all_blogposts', methods=['POST'])
def author_get_all_blogposts():
    content = request.get_json()
    username = content.get('username')
    if not username:
        abort(400)

    author = blogger_engine.GetAuthorByUsername(username)
    if author:
        author_json = author.toJson()
        if author.GetBlogposts():
            blogposts_json = [blogpost.toJson()
                              for blogpost in author.GetBlogposts()]
        else:
            blogposts_json = []
    else:
        blogposts_json = []
        author_json = None

    return jsonify({
        'blogposts': blogposts_json,
        'author': author_json
    })


@app.route('/author/get_all_removed_blogposts', methods=['POST'])
def author_get_all_removed_blogposts():
    content = request.get_json()
    username = content.get('username')
    if not username:
        abort(400)

    author = blogger_engine.GetAuthorByUsername(username)
    if author:
        author_json = author.toJson()
        if author.GetRemovedBlogposts():
            removed_blogposts_json = [blogpost.toJson()
                                      for blogpost in
                                      author.GetRemovedBlogposts()]
        else:
            removed_blogposts_json = []
    else:
        author_json = None
        removed_blogposts_json = []

    return jsonify({
        'removed_blogposts': removed_blogposts_json,
        'author': author_json
    })


@app.route('/author/get_all_comments', methods=['POST'])
def author_get_all_comments():
    content = request.get_json()
    username = content.get('username')
    if not username:
        abort(400)

    author = blogger_engine.GetAuthorByUsername(username)
    if author:
        author_json = author.toJson()
        if author.GetComments():
            comments_json = [comment.toJson()
                             for comment in author.GetComments()]
        else:
            comments_json = []
    else:
        author_json = None
        comments_json = []

    return jsonify({
        'comments': comments_json,
        'author': author_json
    })


@app.route('/author/get_all_removed_comments', methods=['POST'])
def author_get_all_removed_comments():
    content = request.get_json()
    username = content.get('username')
    if not username:
        abort(400)

    author = blogger_engine.GetAuthorByUsername(username)
    if author:
        author_json = author.toJson()
        if author.GetRemovedComments():
            removed_comments_json = [comment.toJson()
                                     for comment in
                                     author.GetRemovedComments()]
        else:
            removed_comments_json = []
    else:
        author_json = None
        removed_comments_json = []

    return jsonify({
        'removed_comments': removed_comments_json,
        'author': author_json
    })


@app.route('/author/get_all', methods=['GET', 'POST'])
def author_get_all():
    authors = blogger_engine.GetAllAuthors()
    if authors:
        return jsonify({
            'authors': [author.toJson() for author in authors]
        })

    return jsonify({
        'authors': []
    })

"""Blogpost methods."""


@app.route('/blogpost/create', methods=['POST'])
def blogpost_create():
    content = request.get_json()

    username = content.get('username')
    headline = content.get('headline')
    body = content.get('body')

    if not username and not headline and not body:
        abort(400)

    return jsonify({
        'blogpost': blogger_engine.SubmitBlogpost(username,
                                                  headline,
                                                  body).toJson()
    })


@app.route('/blogpost/add_label', methods=['POST'])
def blogpost_add_label():
    content = request.get_json()

    label_text = content.get('label_text')
    blogpost_id = content.get('blogpost_id')

    if not label_text and not blogpost_id:
        abort(400)

    label = blogger_engine.AddLabelToBlogpost(label_text, blogpost_id)
    if label:
        label_json = label.toJson()
        blogpost_json = blogger_engine.GetBlogpostById(blogpost_id).toJson()
    else:
        label_json = None
        blogpost_json = None

    return jsonify({
        'label': label_json,
        'blogpost': blogpost_json
    })


@app.route('/blogpost/remove_label', methods=['POST'])
def blogpost_remove_label():
    content = request.get_json()
    label_text = content.get('label_text')
    blogpost_id = content.get('blogpost_id')

    if not label_text or not blogpost_id:
        abort(400)

    blogpost = blogger_engine.GetBlogpostById(blogpost_id)
    label = blogger_engine.GetLabel(label_text)

    if blogpost and label:
        result = blogger_engine.RemoveLabelFromBlogpost(label_text,
                                                        blogpost_id)
        return jsonify({
            'label': label.toJson(),
            'blogpost': blogpost.toJson()
        })

    if blogpost and not label:
        return jsonify({
            'label': None,
            'blogpost': blogpost.toJson()
        })

    if label and not blogpost:
        return jsonify({
            'label': label.toJson(),
            'blogpost': None
        })

    return jsonify({
        'label': None,
        'blogpost': None
    })


@app.route('/blogpost/add_comment', methods=['POST'])
def blogpost_add_comment():
    content = request.get_json()

    username = content.get('username')
    comment_text = content.get('comment_text')
    blogpost_id = content.get('blogpost_id')

    if not username or not comment_text or not blogpost_id:
        abort(400)

    comment = blogger_engine.SubmitComment(username, comment_text,
                                           blogpost_id)
    if comment:
        blogpost_json = comment.blogpost.toJson()
        comment_json = comment.toJson()
    else:
        blogpost_json = None
        comment_json = None

    return jsonify({
        'comment': comment_json,
        'blogpost': blogpost_json,
    })


@app.route('/blogpost/remove_comment', methods=['POST'])
def blogpost_remove_comment():
    content = request.get_json()
    comment_id = content.get('comment_id')

    if not comment_id:
        abort(400)

    comment = blogger_engine.GetCommentById(comment_id)
    if comment:
        removed_comment = blogger_engine.RemoveCommentFromBlogpost(
            comment.id)
        return jsonify({
            'removed_comment': removed_comment.toJson(),
            'blogpost': removed_comment.blogpost.toJson()
        })

    return jsonify({
        'removed_comment': None,
        'blogpost': None
    })


@app.route('/blogpost/get_by_id', methods=['POST'])
def blogpost_get_by_id():
    content = request.get_json()
    blogpost_id = content.get('blogpost_id')

    if not blogpost_id:
        abort(400)

    blogpost = blogger_engine.GetBlogpostById(blogpost_id)
    if blogpost:
        return jsonify({
            'blogpost': blogpost.toJson()
        })

    return jsonify({
        'blogpost': None
    })


@app.route('/blogpost/get_all_comments', methods=['POST'])
def blogpost_get_all_comments():
    content = request.get_json()

    blogpost_id = content.get('blogpost_id')

    if not blogpost_id:
        abort(400)

    blogpost = blogger_engine.GetBlogpostById(blogpost_id)
    comments = blogger_engine.GetCommentsByBlogpost(blogpost_id)
    if blogpost and comments:
        return jsonify({
            'comments': [comment.toJson() for comment in comments],
            'blogpost': blogpost.toJson()
        })

    if blogpost:
        return jsonify({
            'comments': [],
            'blogpost': blogpost.toJson()
        })

    return jsonify({
        'comments': [],
        'blogpost': None
    })


@app.route('/blogpost/get_all_labels', methods=['POST'])
def blogpost_get_all_labels():
    content = request.get_json()

    blogpost_id = content.get('blogpost_id')
    if not blogpost_id:
        abort(400)

    labels = blogger_engine.GetLabelsByBlogpost(blogpost_id)
    if labels:
        return jsonify({
            'blogpost': blogger_engine.GetBlogpostById(blogpost_id).toJson(),
            'labels': [label.toJson() for label in labels]
        })

    return jsonify({
        'blogpost': None,
        'labels': []
    })


@app.route('/blogpost/get_by_label', methods=['POST'])
def blogpost_get_by_label():
    content = request.get_json()
    label_text = content.get('label_text')
    if not label_text:
        abort(400)

    blogposts = blogger_engine.GetBlogpostsByLabel(label_text)
    if blogposts:
        return jsonify({
            'blogposts': [blogpost.toJson() for blogpost in blogposts]
        })

    return jsonify({
        'blogposts': []
    })


@app.route('/blogpost/get_all', methods=['GET', 'POST'])
def blogpost_get_all():
    blogposts = blogger_engine.GetAllBlogposts()
    if blogposts:
        return jsonify({
            'blogposts': [blogpost.toJson() for blogpost in blogposts]
        })

    return jsonify({
        'blogposts': []
    })


@app.route('/blogpost/remove', methods=['POST'])
def blogpost_remove():
    content = request.get_json()
    blogpost_id = content.get('blogpost_id')

    if not blogpost_id:
        abort(400)

    blogpost = blogger_engine.GetBlogpostById(blogpost_id)
    if not blogpost:
        return jsonify({
            'removed_blogpost': None,
            'author': None
        })

    author = blogpost.author
    deleted_blogpost = blogger_engine.DeleteBlogpost(blogpost.id)
    if blogpost:
        return jsonify({
            'removed_blogpost': blogpost.toJson(),
            'author': author.toJson()
        })


@app.route('/blogpost/get_all_by_username', methods=['POST'])
def blogpost_get_all_by_username():
    return author_get_all_blogposts()

"""Comment methods."""


@app.route('/comment/create', methods=['POST'])
def comment_create():
    return blogpost_add_comment()


@app.route('/comment/get_by_id', methods=['POST'])
def comment_get_by_id():
    content = request.get_json()
    comment_id = content.get('comment_id')

    if not comment_id:
        abort(400)

    comment = blogger_engine.GetCommentById(comment_id)
    if comment:
        return jsonify({
            'comment': comment.toJson()
        })

    return jsonify({
        'comment': None
    })


@app.route('/comment/remove', methods=['POST'])
def comment_remove():
    return blogpost_remove_comment()


@app.route('/comment/get_all_by_username', methods=['POST'])
def comment_get_all_by_username():
    return author_get_all_comments()


@app.route('/comment/get_all', methods=['GET', 'POST'])
def comments_get_all():
    comments = blogger_engine.GetAllComments()
    if comments:
        return jsonify({
            'comments': [comment.toJson() for comment in comments]
        })

    return jsonify({
        'comments': []
    })

"""Label methods."""


@app.route('/label/create', methods=['POST'])
def label_create():
    content = request.get_json()
    label_text = content.get('label_text')

    if not label_text:
        abort(400)

    return jsonify({
        'label': blogger_engine.GetOrInsertLabel(label_text).toJson()
    })


@app.route('/label/get_all', methods=['GET', 'POST'])
def label_get_all():
    labels = blogger_engine.GetAllLabels()
    if labels:
        return jsonify({
            'labels': [label.toJson() for label in labels]
        })

    return jsonify({
        'labels': []
    })


@app.route('/label/get_by_id', methods=['POST'])
def label_get_by_id():
    content = request.get_json()
    label_text = content.get('label_text')

    if not label_text:
        abort(400)

    label = blogger_engine.GetLabel(label_text)
    if label:
        label_json = label.toJson()
    else:
        label_json = None

    return jsonify({
        'label': label_json
    })


@app.route('/label/add_to_blogpost', methods=['POST'])
def label_add_to_blogpost():
    return blogpost_add_label()


@app.route('/label/remove_from_blogpost', methods=['POST'])
def label_remove_from_blogpost():
    return blogpost_remove_label()


@app.route('/label/get_all_blogposts_with_label', methods=['POST'])
def label_get_all_blogposts_with_label():
    return blogpost_get_by_label()


@app.route('/label/delete', methods=['POST'])
def label_delete():
    content = request.get_json()
    label_text = content.get('label_text')

    if not label_text:
        abort(400)

    blogposts = blogger_engine.GetBlogpostsByLabel(label_text)
    deleted_label = blogger_engine.DeleteLabel(label_text)
    if deleted_label:
        if blogposts:
            return jsonify({
                'deleted_label': deleted_label.toJson(),
                'blogposts': [blogpost.toJson() for blogpost in blogposts]
            })
        else:
            return jsonify({
                'deleted_label': deleted_label.toJson(),
                'blogposts': []
            })

    return jsonify({
        'deleted_label': None,
        'blogposts': []
    })

if __name__ == '__main__':
    app.run()
