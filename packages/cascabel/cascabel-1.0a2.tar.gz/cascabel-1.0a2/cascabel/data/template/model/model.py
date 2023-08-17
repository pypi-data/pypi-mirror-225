from resources.vars.vars import db
import sqlalchemy as sql

class NAME(db.Model):
    __bind_key__ = "BIND"
    __tablename__ = "TABLE_NAME"
    id   = sql.Column(sql.Integer(), primary_key=True, autoincrement=True)
    info = sql.Column(sql.String(255))