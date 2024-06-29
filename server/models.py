# server/models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Game(db.Model, SerializerMixin):
    __tablename__ = "games"

    serialize_rules = ("-reviews.game",)


    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True)
    genre = db.Column(db.String)
    platform = db.Column(db.String)
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    reviews = db.relationship("Review", back_populates="game")

    # Association proxy to get users for this game through reviews
    users = association_proxy("reviews", "user",
                              creator=lambda user_obj: Review(user=user_obj))
    def __repr__(self):
        return f"<Game {self.title} for {self.platform}>"


class Review(db.Model, SerializerMixin):
    __tablename__ = "reviews"

    serialize_rules = ("-game.reviews", "-user.reviews",)

    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    comment = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    game_id = db.Column(db.Integer, db.ForeignKey("games.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    game = db.relationship("Game", back_populates="reviews")
    user = db.relationship("User", back_populates="reviews")


    def __repr__(self):
        return f"<Review ({self.id}) of {self.game}: {self.score}/10>"


class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    serialize_rules = ("-reviews.user",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    reviews = db.relationship("Review", back_populates="user")

    def __repr__(self):
        return f"<User ({self.id}) {self.name}>"

