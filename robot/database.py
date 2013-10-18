from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime
from config import MYSQL_URI

Engine = create_engine(MYSQL_URI, echo=True)
Base = declarative_base(bind=Engine)
Session = scoped_session(sessionmaker(Engine))


class Log(Base):
    __tablename__ = 'irc_logs'

    id = Column('log_id', Integer, primary_key=True, index=True)
    nick = Column('nick', String(50), nullable=False)
    channel = Column('channel', String(100), index=True)
    message = Column('message', Text)
    created_at = Column('created_at', DateTime, nullable=False, default=datetime.now())

    def __init__(self, nick, channel, message):
        self.nick = nick
        self.channel = channel
        self.message = message

    def __repr__(self):
        return u'<Log %r at. %s>' % (self.nick, self.created_at)


class Link(Base):
    __tablename__ = 'irc_links'

    id = Column('link_id', Integer, primary_key=True, index=True)
    log_id = Column('log_id', Integer, ForeignKey('irc_logs.log_id'))
    log = relationship('Log')
    url = Column('url', String(255), nullable=True)

    def __init__(self, log, url):
        self.log_id = log.id
        self.url = url

    def __repr__(self):
        return u'<Link %r>' % self.url


Base.metadata.create_all()