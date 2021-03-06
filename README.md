###BloggerEngine

[![Build
Status](https://travis-ci.org/cheesesashimi/BloggerEngine.svg?branch=master)](https://travis-ci.org/cheesesashimi/BloggerEngine)

BloggerEngine aims to be a simple, memory-persistent prototype blogging
engine.

Each of the data models, author, blogpost, comment and label is persisted
in memory inside of an OrderedDict(). This allows fast insertion and lookup
time without sacrificing chronological order. Due to how Python handles
references, we can efficiently associate a given blogpost or comment with
a given author as well as a given label with multiple blogposts with very
little overhead.

BloggerEngine only has two major dependencies:
- Flask
- Mock (for testing)

While one shouldn't need to manually install those, it is worth mentioning.

To Get Started:
- Clone this git repo.
- Run the `start_server.sh` script.
- To run all the tests, use the provided `run_tests.sh` script.

The server uses Flask and implements a number of URL methods for
working with authors, blogposts, comments and labels. These URLs accept
a JSON POST request with the required arguments and will return JSON,
assuming the request is successful. URLs missing arguments do not require
them.

Author URLs:
- `/author/create` - username
- `/author/get_all`
- `/author/get_all_blogposts` - username
- `/author/get_all_comments` - username
- `/author/get_all_removed_blogposts` - username
- `/author/get_all_removed_comments` - username
- `/author/get_by_username` - username

Blogpost URLs:
- `/blogpost/add_comment` - username, blogpost_id
- `/blogpost/add_label` - blogpost_id
- `/blogpost/create` - username, headline, body
- `/blogpost/get_all`
- `/blogpost/get_all_by_username` - username
- `/blogpost/get_all_comments`
- `/blogpost/get_all_labels`
- `/blogpost/get_by_id` - blogpost_id
- `/blogpost/get_by_label` - label_text
- `/blogpost/remove` - blogpost_id
- `/blogpost/remove_comment` - comment_id
- `/blogpost/remove_label `- label_text

Comment URLs:
- `/comment/create` - username, comment_content
- `/comment/get_all`
- `/comment/get_all_by_username` - username
- `/comment/get_by_id` - comment_id
- `/comment/remove` - comment_id

Label URLs:
- `/label/add_to_blogpost` - label_text, blogpost_id
- `/label/create` - label_text
- `/label/delete` - label_text
- `/label/get_all`
- `/label/get_all_blogposts_with_label`
- `/label/get_by_id - label_text`
- `/label/remove_from_blogpost` - label_text, blogpost_id
