# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime, timedelta
from config import MYSQL_URI

Engine = create_engine(MYSQL_URI)
Base = declarative_base(bind=Engine)
Session = scoped_session(sessionmaker(Engine))


class Channel(Base):
    __tablename__ = 'irc_channels'

    id = Column('id', Integer, primary_key=True, index=True)
    name = Column('name', String(100), unique=True, nullable=False, index=True)

    def __init__(self, channel):
        self.name = channel

    def __repr__(self):
        return u'<Channel %r>' % self.name


class Log(Base):
    __tablename__ = 'irc_logs'

    id = Column('id', Integer, primary_key=True, index=True)
    nick = Column('nick', String(50), nullable=False)
    channel_id = Column('channel_id', Integer, ForeignKey('irc_channels.id'), index=True)
    channel = relationship('Channel')
    message = Column('message', Text)
    created_at = Column('created_at', DateTime, nullable=False, default=datetime.now() + timedelta(hours=9))

    def __init__(self, nick, channel_id, message, created_at):
        self.nick = nick
        self.channel_id = channel_id
        self.message = message
        self.created_at = created_at

    def __repr__(self):
        return u'<Log %r at. %s>' % (self.nick, self.created_at)


class Link(Base):
    __tablename__ = 'irc_links'

    id = Column('id', Integer, primary_key=True, index=True)
    log_id = Column('log_id', Integer, ForeignKey('irc_logs.id'))
    log = relationship('Log')
    url = Column('url', String(255), nullable=True)

    def __init__(self, log, url):
        self.log_id = log.id
        self.url = url

    def __repr__(self):
        return u'<Link %r>' % self.url


if __name__ == '__main__':
    Base.metadata.create_all()