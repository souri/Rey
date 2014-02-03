#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import logging
import getpass
from optparse import OptionParser
import configparser
import aiml
import sleekxmpp
import os
from os import listdir
from os.path import isfile, join

# ensure unicode is handled properly incase python is not v3.0
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input

# Bootstrap
k = aiml.Kernel()

# onlyfiles = [ f for f in listdir('./brain') if isfile(join('./brain',f)) ]
# print ("Training...")
# print onlyfiles
# for file in onlyfiles:
#     k.learn('./brain/'+ file)
# print ("Training done!")

if os.path.isfile("standard.brn"):
    k.bootstrap(brainFile = "standard.brn")
else:
    k.bootstrap(learnFiles = "std-startup.xml", commands = "load aiml b")
    k.saveBrain("standard.brn")

## Bot predicates
k.setBotPredicate("name", "Rey")
k.setBotPredicate("city", "Bangalore")
k.setBotPredicate("email", "reyxi666@gmail.com")
k.setBotPredicate("phylum", "computer program")
k.setBotPredicate("species", "robot")
k.setBotPredicate("nationality", "cyberspace")
k.setBotPredicate("language", "python")
k.setBotPredicate("favortemovie", "Iron Man")
k.setBotPredicate("kindmusic", "Coldplay")
k.setBotPredicate("domain", "Robot")
k.setBotPredicate("gender", "female")


# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input


class Rey(sleekxmpp.ClientXMPP):

    """
    A simple SleekXMPP bot that will echo messages it
    receives, along with a short thank you message.
    """

    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)

        # The message event is triggered whenever a message
        # stanza is received. Be aware that that includes
        # MUC messages and error messages.
        self.add_event_handler("message", self.message)

    def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        """
        Process incoming message stanzas. Be aware that this also
        includes MUC messages and error messages. It is usually
        a good idea to check the messages's type before processing
        or sending replies.

        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """
        if msg['type'] in ('chat', 'normal'):
            response = ''
            print "> %(from)s" % msg, ": ", "%(body)s" % msg
            response = k.respond("%(body)s" % msg, "%(from)s" % msg)
            if not response:
                responce = "I don't know that yet! Tell me something else."
            print "@ %(from)s" % msg, ": ", response
            msg.reply(response).send()


if __name__ == '__main__':
    # Setup the command line arguments.
    optp = OptionParser()

    # Output verbosity options.
    optp.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)
    optp.add_option('-v', '--verbose', help='set logging to COMM',
                    action='store_const', dest='loglevel',
                    const=5, default=logging.INFO)

    # JID and password options.
    optp.add_option("-j", "--jid", dest="jid",
                    help="JID to use")
    optp.add_option("-p", "--password", dest="password",
                    help="password to use")

    opts, args = optp.parse_args()

    # Setup logging.
    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

    #read config file
    config = configparser.ConfigParser()
    config.read('rey.conf')
    opts.jid = config.get('rey', 'jid')
    opts.password = config.get('rey', 'password')

    if opts.jid is None:
        opts.jid = raw_input("Username: ")
    if opts.password is None:
        opts.password = getpass.getpass("Password: ")

    # Setup the Rey and register plugins. Note that while plugins may
    # have interdependencies, the order in which you register them does
    # not matter.
    xmpp = Rey(opts.jid, opts.password)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0004') # Data Forms
    xmpp.register_plugin('xep_0060') # PubSub
    xmpp.register_plugin('xep_0199') # XMPP Ping

    # If you are working with an OpenFire server, you may need
    # to adjust the SSL version used:
    # xmpp.ssl_version = ssl.PROTOCOL_SSLv3

    # If you want to verify the SSL certificates offered by a server:
    # xmpp.ca_certs = "path/to/ca/cert"

    # Connect to the XMPP server and start processing XMPP stanzas.
    if xmpp.connect():
        # If you do not have the dnspython library installed, you will need
        # to manually specify the name of the server if it does not match
        # the one in the JID. For example, to use Google Talk you would
        # need to use:
        #
        # if xmpp.connect(('talk.google.com', 5222)):
        #     ...
        xmpp.process(threaded=False)
        print("Done")
    else:
        print("Unable to connect.")