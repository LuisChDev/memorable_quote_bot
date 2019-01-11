import os
import sys
from pony.orm import Database, Required, PrimaryKey

db = Database()


class Comment(db.Entity):
    id = PrimaryKey(str)
    url = Required(str)


class Message(db.Entity):
    id = PrimaryKey(str)


class Bannedsub(db.Entity):
    name = Required(str)


class Banneduser(db.Entity):
    name = Required(str)


class Historicalfigure(db.Entity):
    name = Required(str)
