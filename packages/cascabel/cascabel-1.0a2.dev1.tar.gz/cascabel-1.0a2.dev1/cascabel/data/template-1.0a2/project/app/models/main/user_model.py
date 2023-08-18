from resources.vars.vars import db
import sqlalchemy as sql

class UserModel(db.Model):
    __bind_key__ = "main"
    __tablename__ = "user"
    email    = sql.Column(sql.String(255), primary_key=True)
    name     = sql.Column(sql.String(255))
    password = sql.Column(sql.String(255))
    birth_date = sql.Column(sql.DateTime())