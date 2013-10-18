# -*- coding: utf-8 -*-

from database import Session, Channel, Log, Link
from datetime import datetime, timedelta
from urlparse import urlparse

import socket
import string


config = {
    'HOST': "irc.ozinger.org",  # Host of irc server
    'PORT': 6667,  # Port to connection
    'IDEN': "beautifuljy",  # Identity
    'REAL': "powerful jy",  # Real name
    'NICK': "be4utyfu1",  # Nick name
}


def run():
    channels = Session.query(Channel).all()
    channel_map = {}
    config['CHAN'] = []
    for channel in channels:
        config['CHAN'].append(channel.name)
        channel_map[channel.name] = channel.id

    s = None
    try:
        s = socket.socket()
        s.connect((config['HOST'], config['PORT']))
        s.send("NICK %s\r\n" % config['NICK'])
        s.send("USER %s %s bla :%s\r\n" % (config['IDEN'], config['HOST'], config['REAL']))
        buf = ""
        flag = 1  # flag for connected loop

        # Operate until it tells us we have connected
        while flag:
            buf = buf + s.recv(1024)
            tmp = string.split(buf, "\n")
            buf = tmp.pop()

            for line in tmp:
                line = string.rstrip(line)
                line = string.split(line)

                if line[0] == "PING":
                    s.send("PONG %s\r\n" % line[1])

                if line[1] == "004":
                    for chan in config['CHAN']:
                        s.send("JOIN %s\r\n" % chan)

                    flag = False  # Loop break

        # Operate whenever socket received
        while 1:
            buf = buf + s.recv(1024)
            tmp = string.split(buf, "\n")
            buf = tmp.pop()

            for line in tmp:
                line = string.rstrip(line)
                line = string.split(line)

                # print line

                # Pong when Ping arrived
                if line[0] == "PING":
                    s.send("PONG %s\r\n" % line[1])

                # Message from Channels
                if line[1] == "PRIVMSG":
                    sender = string.split(line[0], "!")[0][1:]  # User who told
                    obj = line[2]  # Channel(User) where(who) message happened(received)
                    msg = " ".join(line[3:])[1:]  # Message

                    if obj == config['NICK']:
                        pass
                    else:
                        log = Log(sender, channel_map[obj], msg, datetime.now() + timedelta(hours=9))
                        Session.add(log)
                        Session.commit()

                        for m in msg.split(' '):
                            tmp = urlparse(m)
                            if tmp.scheme in ['http', 'https', 'ftp']:
                                link = Link(log, tmp.geturl())
                                Session.add(link)
                                Session.commit()

                    if string.split(msg)[0] == "$$":
                        s.send("%s\r\n" % " ".join(string.split(msg)[1:]))

    finally:
        s.close()


if __name__ == "__main__":
    run()