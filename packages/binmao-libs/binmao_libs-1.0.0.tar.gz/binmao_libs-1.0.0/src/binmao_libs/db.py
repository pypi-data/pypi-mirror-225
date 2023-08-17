from peewee import *
from playhouse.db_url import connect as _connect


def connect(url: str):
  return _connect(url)