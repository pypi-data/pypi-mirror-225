from resources.vars.vars import db
import sqlalchemy as sql

class TestModel(db.Model):
    __bind_key__ = "main"
    __tablename__ = "test"
    id   = sql.Column(sql.Integer(), primary_key=True, autoincrement=True)
    info = sql.Column(sql.String(255))
    