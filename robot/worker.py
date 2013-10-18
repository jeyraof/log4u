# -*- coding: utf-8 -*-

from database import Log, Link

import socket
import string


config = {
    'HOST': "irc.ozinger.org",  # Host of irc server
    'PORT': 6667,  # Port to connection
    'IDEN': "",  # Identity
    'REAL': "",  # Real name
    'NICK': "",  # Nick name
    'CHAN': ["#freyja"],  # Auto join channel list (add prefix '#' to channel name)
    'NSRV': "Nickserv",  # Nick service bot Nick name
    'NSID': "",  # Nick service auth ID
    'NPWD': "",  # Nick service auth Password
}


def main():
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

                    if len(config['NPWD']) > 0:  # When Auth service config was set
                        s.send("PRIVMSG %s :IDENTIFY %s %s \r\n" % (config['NSRV'],
                                                                    config['NSID'],
                                                                    config['NPWD']))
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
                        print "(Query) <%s> %s" % (sender, msg)  # When message was direct query
                    else:
                        print "(%s) <%s> %s" % (obj, sender, msg)  # When message happened in channels

                    if string.split(msg)[0] == "$$":
                        s.send("%s\r\n" % " ".join(string.split(msg)[1:]))

    finally:
        s.close()


if __name__ == "__main__":
    main()