#!/usr/bin/python

import interface
from flask import Flask, json, jsonify, request
from models import base_model

app = Flask('BloggerEngine')

blogger_engine = interface.BloggerEngine()


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
    }

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

@app.route('/author/delete', methods=['POST'])
def author_delete():
    pass

@app.route('/author/get_all_blogposts', methods=['POST'])
def author_get_all_blogposts():
    content = request.get_json()
    username = content.get('username')
    if not username:
        abort(400)

    author = blogger_engine.GetAuthorByUsername(username)
    if author:
        author_json = author.toJson()
    else:
        author_json = None

    if author.GetBlogposts():
        blogposts_json = [blogpost.toJson()
                          for blogpost in author.GetBlogposts()]
    else:
        blogposts_json = None

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
    else:
        author_json = None

    if author.GetRemovedBlogposts():
        removed_blogposts_json = [blogpost.toJson()
                                  for blogpost in
                                      author.GetRemovedBlogposts()]
    else:
        removed_blogposts_json = None

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
    else:
        author_json = None

    if author.GetComments():
        comments_json = [comment.toJson()
                         for comment in author.GetComments()]
    else:
        comments_json = None

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
    else:
        author_json = None

    if author.GetRemovedComments():
        removed_comments_json = [comment.toJson()
                                 for comment in author.GetRemovedComments()]
    else:
        removed_comments_json = None

    return jsonify({
        'removed_comments': removed_comments_json,
        'author': author_json
    })

@app.route('/author/get_all', methods=['POST'])
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

@app.route('/blogpost/add_label', methods['POST'])
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
        'label': label_json
        'blogpost': blogpost_json
    })
        
@app.route('/blogpost/remove_label', methods=['POST'])
def blogpost_remove_label():
    content = request.get_json()
    label_text = content.get('label_text')
    blogpost_id = content.get('blogpost_id')

    if not label_text and not blogpost_id:
        abort(400)

    result = blogger_engine.RemoveLabelFromBlogpost(label_text, blogpost_id)

    if result:
        label, blogpost = result
        return jsonify({
            'label': label.toJson(),
            'blogpost': blogpost.toJson()
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

    if not username and not comment_text and not blogpost_id:
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
        blogpost_json = comment.blogpost.toJson()
        removed_comment = blogger_engine.RemoveCommentFromBlogpost(
            comment.id)
        return jsonify({
            'removed_comment': removed_comment.toJson(),
            'blogpost': blogpost_json
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
        blogpost_json = blogpost.toJson()
    else:
        blogpost_json = None

    return jsonify({
        'blogpost': blogpost_json
    })

@app.route('/blogpost/get_all_comments', methods=['POST'])
def blogpost_get_all_comments():
    content = request.get_json()

    blogpost_id = content.get('blogpost_id')

    if not blogpost_id:
        abort(400)

    comments = blogger_engine.GetCommentsByBlogpost(blogpost_id)
    if not comments:
        return jsonify({
            'comments': None,
            'blogpost': None
        })

    return jsonify({
        'comments': [comment.toJson() for comment in comments],
        'blogpost': blogger_engine.GetBlogpostById(blogpost_id).toJson()
    })

@app.route('/blogpost/get_all_labels', methods=['POST'])
def blogpost_get_all_labels():
    content = request.get_json()

    blogpost_id = content.get('blogpost_id')
    if not blogpost_id:
        abort(400)

    labels = blogger_engine.GetLabelsByBlogpost(blogpost_id)
    if not labels:
        return jsonify({
            'blogpost': [],
            'labels': None
        })

    return jsonify({
        'blogpost': blogger_engine.GetBlogpostById(blogpost_id).toJson(),
        'labels': [label.toJson() for label in labels]
    })

@app.route('/blogpost/get_by_label', methods=['POST'])
def blogpost_get_by_label():
    content = request.get_json()
    label_text = content.get('label_text')
    if not label_text:
        abort(400)

    blogposts = blogger_engine.GetBlogpostsByLabel()
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
    pass

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
    comment_id = content.get('content')
    
    if not comment_id:
        abort(400)

    comment = blogger_engine.GetCommentById(comment_id)
    if comment:
        comment_json = comment.toJson()

    return jsonify({
        'comment': comment_json
    })

@app.route('/comment/remove', methods=['POST'])
def comment_remove():
    return blogpost_remove_comment()

@app.route('/comment/get_all_by_username', methods=['POST'])
def comment_get_all_by_username():
    return author_get_all_comments()
    
@app.route('/comment/get_all', methods=['POST'])
def comments_get_all():
    comments = blogger_engine.GetAllComments()
    if comments:
        comments_json = [comment.toJson() for comment in comments]
    else:
        comments_json = []

    return jsonify({
        'comments': comments_json
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

@app.route('/label/get_all', methods=['POST'])
def label_get_all():
    labels = blogger_engine.GetAllLabels()
    if labels:
        labels_json = [label.toJson() for label in labels]
    else:
        labels_json = []

    return jsonify({
        'labels': labels_json
    })

@app.route('/label/get_by_id', methods['POST'])
def label_get_by_id():
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

@app.route('/label/get_all_blogposts_with_label')
def label_get_all_blogposts_with_label():
    return blogpost_get_by_label()

@app.route('/label/delete', methods=['POST'])
def label_delete():
    content = request.get_json()
    label_text = content.get('label_text')


    if not label_text:
        abort(400)

    deleted_label = blogger_engine.DeleteLabel(label_text)
    if deleted_label:
        return jsonify({
            'deleted_label': deleted_label.toJson()
        })

    return jsonify({
        'deleted_label': None
    })

if __name__ == '__main__':
    app.run(debug=True)
