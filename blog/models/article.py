from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from blog.models.article_tag import article_tag_association_table
from blog.models.database import db


class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, ForeignKey("authors.id"), nullable=False)
    title = db.Column(db.String(255))
    text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author = relationship("Author", back_populates="articles")

    tags = relationship(
        "Tag",
        secondary=article_tag_association_table,
        back_populates="articles",
    )
