class Post:
    def __init__(self, author, images, tags):
        self.author = author
        self.images = images
        self.tags = tags

    def to_str(self):
        return f"author: {self.author}, images: {self.images}, tags: {self.tags}"


class Response:
    def __init__(self, lp, posts):
        self.lp = lp
        self.posts = posts
