class ChatUser(object):
    def __init__(self, id, chat_id, fname, rank):
        self.id = id
        self.chat_id = chat_id
        self.fname = fname
        self.rank = rank

    def set_rank(self, rank):
        if rank in [0, 1, 2]:
            self.rank = rank

    def __repr__(self):
        return "<ChatUser('%s','%s', '%s', '%s')>" % (self.id, self.chat_id, self.fname, self.rank)


class Chat(object):
    def __init__(self, id, chat_name, users):
        self.id = id
        self.chat_name = chat_name
        self.users = users

    def __repr__(self):
        return "<ChatUser('%s','%s', '%s')>" % (self.id, self.chat_name, self.users)
