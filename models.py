from sqlalchemy.ext.orderinglist import ordering_list

from app import db


class ChatUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    chat_id = db.Column(db.Integer, nullable=False)
    fname = db.Column(db.String(32), nullable=False)
    rank = db.Column(db.Integer, nullable=False)

    def set_rank(self, rank):
        if rank in [0, 1, 2]:
            self.rank = rank


class Chat(db.Model):
    __tablename__ = "chats"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    chat_name = db.Column(db.String(32), nullable=False)
    users = db.relationship("ChatUser", order_by="ChatUser.id", collection_class=ordering_list("id"))
