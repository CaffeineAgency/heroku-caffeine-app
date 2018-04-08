class Post:
    def __init__(self, post_id, sender, text):
        self.post_id = post_id
        self.sender = sender
        self.text = text


class Response:
    def __init__(self, page, posts):
        self.current_page = page
        self.posts = posts
