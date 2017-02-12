#!/usr/bin/python

from bloggerengine import engine
from flask import Flask, abort, json, jsonify, request

app = Flask('BloggerEngine')

blogger_engine = engine.BloggerEngine()


"""Author methods."""


@app.route('/author/create', methods=['POST'])
def author_create():
    """Creates a new author.

    Request Args:
      username: string; The author username to create.

    Returns:
      A dictionary containing the new Author.

    """
    request_arguments = request.get_json()
    username = request_arguments.get('username')
    if not username:
        abort(400)

    return jsonify({
        'author': blogger_engine.GetOrInsertAuthor(username).ToJson()
    })


@app.route('/author/get_by_username', methods=['POST'])
def author_get_by_username():
    """Gets an author by their username.

    Request Args:
      username: string; The author username to retrieve.

    Returns:
      A dictionary with the retrieved author, if found.

    """
    request_arguments = request.get_json()
    username = request_arguments.get('username')
    if not username:
        abort(400)

    author = blogger_engine.GetAuthorByUsername(username)
    if author:
        return jsonify({
            'author': author.ToJson()
        })

    return jsonify({
        'author': None
    })


@app.route('/author/get_all_blogposts', methods=['POST'])
def author_get_all_blogposts():
    """Gets all blogposts for a given author.

    Request Args:
      username: string; The author username to retrieve blogposts.

    Returns:
      A dictionary of the the author's blogposts, if found.

    """
    request_arguments = request.get_json()
    username = request_arguments.get('username')
    if not username:
        abort(400)

    author = blogger_engine.GetAuthorByUsername(username)
    if author:
        if author.GetBlogposts():
            return jsonify({
                'blogposts': [blogpost.ToJson()
                              for blogpost in author.GetBlogposts()],
                'author': author.ToJson()
            })
        else:
            return jsonify({
                'blogposts': [],
                'author': author.ToJson()
            })

    return jsonify({
        'blogposts': [],
        'author': None
    })


@app.route('/author/get_all_removed_blogposts', methods=['POST'])
def author_get_all_removed_blogposts():
    """Gets all remobved blogposts associated with an author.

    Request Args:
      username: string; The author username to retrieve blogposts.

    Returns:
      A dictionary of removed blogposts, if found.

    """
    request_arguments = request.get_json()
    username = request_arguments.get('username')
    if not username:
        abort(400)

    author = blogger_engine.GetAuthorByUsername(username)
    if author:
        author_json = author.ToJson()
        if author.GetRemovedBlogposts():
            return jsonify({
                'removed_blogposts': [blogpost.ToJson()
                                      for blogpost in
                                      author.GetRemovedBlogposts()],
                'author': author_json
            })
        else:
            return jsonify({
                'removed_blogposts': [],
                'author': author_json
            })

    return jsonify({
        'author': None,
        'removed_blogposts': []
    })


@app.route('/author/get_all_comments', methods=['POST'])
def author_get_all_comments():
    """Gets all comments from a given author.

    Request Args:
      username: string; The author username to retrieve comments.

    Returns:
      A dictionary of comments, if found.

    """
    request_arguments = request.get_json()
    username = request_arguments.get('username')
    if not username:
        abort(400)

    author = blogger_engine.GetAuthorByUsername(username)
    if author:
        author_json = author.ToJson()
        if author.GetComments():
            return jsonify({
                'comments': [comment.ToJson()
                             for comment in author.GetComments()],
                'author': author_json
            })
        else:
            return jsonify({
                'comments': [],
                'author': author_json
            })

    return jsonify({
        'comments': [],
        'author': None
    })


@app.route('/author/get_all_removed_comments', methods=['POST'])
def author_get_all_removed_comments():
    """Gets all removed comments from an author.

    Request Args:
      username: string; The author to get removed comments.

    Returns:
      A dictionary of removed comments, if found.

    """
    request_arguments = request.get_json()
    username = request_arguments.get('username')
    if not username:
        abort(400)

    author = blogger_engine.GetAuthorByUsername(username)
    if author:
        author_json = author.ToJson()
        if author.GetRemovedComments():
            return jsonify({
                'removed_comments': [comment.ToJson()
                                     for comment in
                                     author.GetRemovedComments()],
                'author': author_json
            })
        else:
            return jsonify({
                'removed_comments': [],
                'author': author_json
            })

    return jsonify({
        'removed_comments': [],
        'author': None
    })


@app.route('/author/get_all', methods=['GET', 'POST'])
def author_get_all():
    """Get all authors.

    Returns:
      A dictionary of all authors in the datastore.

    """
    authors = blogger_engine.GetAllAuthors()
    if authors:
        return jsonify({
            'authors': [author.ToJson() for author in authors]
        })

    return jsonify({
        'authors': []
    })

"""Blogpost methods."""


@app.route('/blogpost/create', methods=['POST'])
def blogpost_create():
    """Creates a new blogpost (and author, if not found).

    Request Args:
      username: string; The username of the author.
      headline: string; The headline of the post.
      body: string; The main body of the post.

    Returns:
      A dictionary containing the new blogpost and author.

    """
    request_arguments = request.get_json()

    username = request_arguments.get('username')
    headline = request_arguments.get('headline')
    body = request_arguments.get('body')

    if not username and not headline and not body:
        abort(400)

    return jsonify({
        'blogpost': blogger_engine.SubmitBlogpost(username,
                                                  headline,
                                                  body).ToJson(),
        'author': blogger_engine.GetAuthorByUsername(username).ToJson()
    })


@app.route('/blogpost/add_label', methods=['POST'])
def blogpost_add_label():
    """Adds a label to a blogpost, creating the label if necessary.

    Request Args:
      blogpost_id: string; The blogpost ID.
      label_text: string; The label text.

    Returns:
      A dictionary containing the new label and the affected blogpost.

    """
    request_arguments = request.get_json()

    label_text = request_arguments.get('label_text')
    blogpost_id = request_arguments.get('blogpost_id')

    if not label_text and not blogpost_id:
        abort(400)

    label = blogger_engine.AddLabelToBlogpost(label_text, blogpost_id)
    blogpost = blogger_engine.GetBlogpostById(blogpost_id)

    if label and blogpost:
        return jsonify({
            'label': label.ToJson(),
            'blogpost': blogpost.ToJson()
        })

    return jsonify({
        'label': None,
        'blogpost': None
    })


@app.route('/blogpost/remove_label', methods=['POST'])
def blogpost_remove_label():
    """Removes a label from a blogpost.

    Request Args:
      label_text: string; The label to remove.
      blogpost_id: string; The blogpost to remove the label from.

    Returns:
      A dictionary containing the affected blogpost and label.

    """
    request_arguments = request.get_json()
    label_text = request_arguments.get('label_text')
    blogpost_id = request_arguments.get('blogpost_id')

    if not label_text or not blogpost_id:
        abort(400)

    blogpost = blogger_engine.GetBlogpostById(blogpost_id)
    label = blogger_engine.GetLabel(label_text)

    if blogpost and label:
        result = blogger_engine.RemoveLabelFromBlogpost(label_text,
                                                        blogpost_id)
        return jsonify({
            'label': label.ToJson(),
            'blogpost': blogpost.ToJson()
        })

    if blogpost and not label:
        return jsonify({
            'label': None,
            'blogpost': blogpost.ToJson()
        })

    if label and not blogpost:
        return jsonify({
            'label': label.ToJson(),
            'blogpost': None
        })

    return jsonify({
        'label': None,
        'blogpost': None
    })


@app.route('/blogpost/add_comment', methods=['POST'])
def blogpost_add_comment():
    """Adds a comment to a blogpost.

    Request Args:
      username: string; The comment author's username.
      comment_text: string; The comment text.
      blogpost_id: string; The blogpost ID to associate the comment with.

    Returns:
      A dictionary containing the comment and affected blogpost.

    """
    request_arguments = request.get_json()

    username = request_arguments.get('username')
    comment_text = request_arguments.get('comment_text')
    blogpost_id = request_arguments.get('blogpost_id')

    if not username or not comment_text or not blogpost_id:
        abort(400)

    comment = blogger_engine.SubmitComment(username, comment_text,
                                           blogpost_id)
    if comment:
        blogpost_json = comment.blogpost.ToJson()
        comment_json = comment.ToJson()
    else:
        blogpost_json = None
        comment_json = None

    return jsonify({
        'comment': comment_json,
        'blogpost': blogpost_json,
    })


@app.route('/blogpost/remove_comment', methods=['POST'])
def blogpost_remove_comment():
    """Removes a comment from a blogpost.

    Request Args:
      comment_id: string; The comment to remove from a blogpost.

    Returns:
      A dictionary containing the removed comment and affected blogpost.

    """
    request_arguments = request.get_json()
    comment_id = request_arguments.get('comment_id')

    if not comment_id:
        abort(400)

    comment = blogger_engine.GetCommentById(comment_id)
    if comment:
        removed_comment = blogger_engine.RemoveCommentFromBlogpost(
            comment.id)
        return jsonify({
            'removed_comment': removed_comment.ToJson(),
            'blogpost': removed_comment.blogpost.ToJson()
        })

    return jsonify({
        'removed_comment': None,
        'blogpost': None
    })


@app.route('/blogpost/get_by_id', methods=['POST'])
def blogpost_get_by_id():
    """Gets a blogpost from it's ID.

    Request Args:
      blogpost_id: string; The blogpost ID to retrieve.

    Returns:
      A dictionary containing the blogpost, if found.

    """
    request_arguments = request.get_json()
    blogpost_id = request_arguments.get('blogpost_id')

    if not blogpost_id:
        abort(400)

    blogpost = blogger_engine.GetBlogpostById(blogpost_id)
    if blogpost:
        return jsonify({
            'blogpost': blogpost.ToJson()
        })

    return jsonify({
        'blogpost': None
    })


@app.route('/blogpost/get_all_comments', methods=['POST'])
def blogpost_get_all_comments():
    """Get all comments associated with a blogpost.

    Request Args:
      blogpost_id: string; The blogpost to retrieve comments from.

    Returns:
      A dictionary containing the retrieved comments and the blogpost.

    """
    request_arguments = request.get_json()

    blogpost_id = request_arguments.get('blogpost_id')

    if not blogpost_id:
        abort(400)

    blogpost = blogger_engine.GetBlogpostById(blogpost_id)
    comments = blogger_engine.GetCommentsByBlogpost(blogpost_id)
    if blogpost and comments:
        return jsonify({
            'comments': [comment.ToJson() for comment in comments],
            'blogpost': blogpost.ToJson()
        })

    if blogpost:
        return jsonify({
            'comments': [],
            'blogpost': blogpost.ToJson()
        })

    return jsonify({
        'comments': [],
        'blogpost': None
    })


@app.route('/blogpost/get_all_labels', methods=['POST'])
def blogpost_get_all_labels():
    """Gets all labels associated with a blogpost.

    Request Args:
      blogpost_id: string; The blogpost ID to retrieve labels from.

    Returns:
      A dictionary containing the blogpost and labels found.

    """
    request_arguments = request.get_json()

    blogpost_id = request_arguments.get('blogpost_id')
    if not blogpost_id:
        abort(400)

    labels = blogger_engine.GetLabelsByBlogpost(blogpost_id)
    if labels:
        return jsonify({
            'blogpost': blogger_engine.GetBlogpostById(blogpost_id).ToJson(),
            'labels': [label.ToJson() for label in labels]
        })

    return jsonify({
        'blogpost': None,
        'labels': []
    })


@app.route('/blogpost/get_by_label', methods=['POST'])
def blogpost_get_by_label():
    """Gets all blogposts associated with a given label.

    Request Args:
      label_text: string; The label to query for.

    Returns:
      A dictionary containing the blogposts, if found.

    """
    request_arguments = request.get_json()
    label_text = request_arguments.get('label_text')
    if not label_text:
        abort(400)

    blogposts = blogger_engine.GetBlogpostsByLabel(label_text)
    if blogposts:
        return jsonify({
            'blogposts': [blogpost.ToJson() for blogpost in blogposts]
        })

    return jsonify({
        'blogposts': []
    })


@app.route('/blogpost/get_all', methods=['GET', 'POST'])
def blogpost_get_all():
    """Retrieves all blogposts from the datastore.

    Returns:
      A dictionary containing all blogposts.

    """
    blogposts = blogger_engine.GetAllBlogposts()
    if blogposts:
        return jsonify({
            'blogposts': [blogpost.ToJson() for blogpost in blogposts]
        })

    return jsonify({
        'blogposts': []
    })


@app.route('/blogpost/remove', methods=['POST'])
def blogpost_remove():
    """Removes a blogpost from the datastore, but allows the author to keep it.

    Request Args:
      blogpost_id: string; The blogpost ID to remove.

    """
    request_arguments = request.get_json()
    blogpost_id = request_arguments.get('blogpost_id')

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
            'removed_blogpost': blogpost.ToJson(),
            'author': author.ToJson()
        })


@app.route('/blogpost/get_all_by_username', methods=['POST'])
def blogpost_get_all_by_username():
    """Gets all blogposts for a given author.

    Request Args:
      username: string; The author username to retrieve blogposts for.

    Returns:
      A dictionary containing the blogposts for a given author, if found.

    """
    return author_get_all_blogposts()

"""Comment methods."""


@app.route('/comment/create', methods=['POST'])
def comment_create():
    """Adds a comment to a blogpost.

    Request Args:
      username: string; The comment author's username.
      comment_text: string; The comment text.
      blogpost_id: string; The blogpost ID to associate the comment with.

    Returns:
      A dictionary containing the comment and affected blogpost.

    """
    return blogpost_add_comment()


@app.route('/comment/get_by_id', methods=['POST'])
def comment_get_by_id():
    """Gets a comment by ID.

    Request Args:
      comment_id: string; The ID of the comment to retrieve.

    Returns:
      A dictinoary containing the comment, if found.

    """
    request_arguments = request.get_json()
    comment_id = request_arguments.get('comment_id')

    if not comment_id:
        abort(400)

    comment = blogger_engine.GetCommentById(comment_id)
    if comment:
        return jsonify({
            'comment': comment.ToJson()
        })

    return jsonify({
        'comment': None
    })


@app.route('/comment/remove', methods=['POST'])
def comment_remove():
    """Removes a comment from a blogpost.

    Request Args:
      comment_id: string; The comment to remove from a blogpost.

    Returns:
      A dictionary containing the removed comment and affected blogpost.

    """
    return blogpost_remove_comment()


@app.route('/comment/get_all_by_username', methods=['POST'])
def comment_get_all_by_username():
    """Gets all comments from a given author.

    Request Args:
      username: string; The author username to retrieve comments.

    Returns:
      A dictionary of comments, if found.

    """
    return author_get_all_comments()


@app.route('/comment/get_all', methods=['GET', 'POST'])
def comments_get_all():
    """Gets all comments from the datastore.

    Returns:
      A dictionary of comments.

    """
    comments = blogger_engine.GetAllComments()
    if comments:
        return jsonify({
            'comments': [comment.ToJson() for comment in comments]
        })

    return jsonify({
        'comments': []
    })

"""Label methods."""


@app.route('/label/create', methods=['POST'])
def label_create():
    """Creates a label.

    Request Args:
      label_text: string; The label text.

    Returns:
      A dictionary containing the new label.

    """
    request_arguments = request.get_json()
    label_text = request_arguments.get('label_text')

    if not label_text:
        abort(400)

    return jsonify({
        'label': blogger_engine.GetOrInsertLabel(label_text).ToJson()
    })


@app.route('/label/get_all', methods=['GET', 'POST'])
def label_get_all():
    """Gets all labels from the datastore.

    Returns:
      A dictionary containing the labels.

    """
    labels = blogger_engine.GetAllLabels()
    if labels:
        return jsonify({
            'labels': [label.ToJson() for label in labels]
        })

    return jsonify({
        'labels': []
    })


@app.route('/label/get_by_id', methods=['POST'])
def label_get_by_id():
    """Gets a label by it's ID, which is also it's text.

    Request Args:
      label_text: string; The label to retrieve.

    Returns:
      A dictionary containing the label, if found.

    """
    request_arguments = request.get_json()
    label_text = request_arguments.get('label_text')

    if not label_text:
        abort(400)

    label = blogger_engine.GetLabel(label_text)
    if label:
        label_json = label.ToJson()
    else:
        label_json = None

    return jsonify({
        'label': label_json
    })


@app.route('/label/add_to_blogpost', methods=['POST'])
def label_add_to_blogpost():
    """Adds a label to a blogpost, creating the label if necessary.

    Request Args:
      blogpost_id: string; The blogpost ID.
      label_text: string; The label text.

    Returns:
      A dictionary containing the new label and the affected blogpost.

    """
    return blogpost_add_label()


@app.route('/label/remove_from_blogpost', methods=['POST'])
def label_remove_from_blogpost():
    """Removes a label from a blogpost.

    Request Args:
      label_text: string; The label to remove.
      blogpost_id: string; The blogpost to remove the label from.

    Returns:
      A dictionary containing the affected blogpost and label.

    """
    return blogpost_remove_label()


@app.route('/label/get_all_blogposts_with_label', methods=['POST'])
def label_get_all_blogposts_with_label():
    """Gets all blogposts associated with a given label.

    Request Args:
      label_text: string; The label to query for.

    Returns:
      A dictionary containing the blogposts, if found.

    """
    return blogpost_get_by_label()


@app.route('/label/delete', methods=['POST'])
def label_delete():
    """Recursively deletes a label from the datastore and all blogposts.

    Request Args:
      label_text: string; The label to delete.

    Returns:
      A dictionary containing the deleted label and affected blogposts.

    """
    request_arguments = request.get_json()
    label_text = request_arguments.get('label_text')

    if not label_text:
        abort(400)

    blogposts = blogger_engine.GetBlogpostsByLabel(label_text)
    deleted_label = blogger_engine.DeleteLabel(label_text)
    if deleted_label:
        if blogposts:
            return jsonify({
                'deleted_label': deleted_label.ToJson(),
                'blogposts': [blogpost.ToJson() for blogpost in blogposts]
            })
        else:
            return jsonify({
                'deleted_label': deleted_label.ToJson(),
                'blogposts': []
            })

    return jsonify({
        'deleted_label': None,
        'blogposts': []
    })

if __name__ == '__main__':
    app.run()
