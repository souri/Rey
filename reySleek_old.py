import sys
import time
import os
import subprocess
import aiml
# import logging
import getpass
from os import system, getcwd
import re
from os import listdir
from os.path import isfile, join
import sleekxmpp
import hashlib

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')

#from PyGtalkRobot import GtalkRobot

k = aiml.Kernel()
onlyfiles = [ f for f in listdir('./brain') if isfile(join('./brain',f)) ]

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

############################################################################################################################
class Rey(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password, nickname="Rey"):
      super(Rey, self).__init__(jid, password)
      self.add_event_handler("session_start", self.start)
      self.add_event_handler("message", self.message)
      self.nick = nickname
      self.jid = jid
      self.password = password
      m = hashlib.md5()
      m.update(self.password)
      self.password_hash = m.hexdigest()
      #self.aiml = AIMLBot(self.nick)

    def start(self, event):
      self.send_presence()
      self.get_roster()

    def message(self, msg):
      print 'ok'
      # if msg['body'].endswith(" " + self.password_hash):
      #   if "RESTART" in msg['body'].upper():
      #     system("cd \"" + getcwd() + "\" & " + " ".join(sys.argv) + " &")
      #     sys.exit()
      #   elif "EXIT" in msg['body'].upper():
      #     sys.exit()
      #   elif "UPDATE" in msg['body'].upper():
      #     system("git pull --all")
      #     msg.reply("Update complete; please issue a restart command for changes to take effect.").send()
      #     return
      # user = (msg['mucnick'] if len(msg['mucnick']) > 0 else "person")
      # if msg['body'].startswith('*** '):
      #   print msg
      #   return
      # elif self.nick in msg:
      #   msg = re.compile(self.nick + "[:,]* ?", re.I).sub('', msg['body'])
      #   prefix = "%s: " % (user.split('!', 1)[0], )
      # else:
      #   prefix = ''

      # if msg['type'] in ('chat', 'normal'):
      #   sentence = self.aiml.on_MSG_IN(user.split('!', 1)[0],msg['body'])
      #   msg.reply(prefix + sentence).send()

    #Regular Expression Pattern Tips:
    # I or IGNORECASE <=> (?i)      case insensitive matching
    # L or LOCALE <=> (?L)          make \w, \W, \b, \B dependent on the current locale
    # M or MULTILINE <=> (?m)       matches every new line and not only start/end of the whole string
    # S or DOTALL <=> (?s)          '.' matches ALL chars, including newline
    # U or UNICODE <=> (?u)         Make \w, \W, \b, and \B dependent on the Unicode character properties database.
    # X or VERBOSE <=> (?x)         Ignores whitespace outside character sets

    #"command_" is the command prefix, "001" is the priviledge num, "setState" is the method name.
    #This method is used to change the state and status text of the bot.
    def command_001_setState(self, user, message, args):
        #the __doc__ of the function is the Regular Expression of this command, if matched, this command method will be called.
        #The parameter "args" is a list, which will hold the matched string in parenthesis of Regular Expression.
        '''(available|online|on|busy|dnd|away|idle|out|off|xa)( +(.*))?$(?i)'''
        show = args[0]
        status = args[1]
        jid = user.getStripped()

        # Verify if the user is the Administrator of this bot
        if jid == '0udpg5hnljlj507oz4gq9ekha6@public.talk.google.com':
            print jid, " ---> ",bot.getResources(jid), bot.getShow(jid), bot.getStatus(jid)
            self.setState(show, status)
            #self.notifysend(show.title())
            self.replyMessage(user, "Okay, I'm " + show.title())

    #This method is used to send email for users.
    def command_002_SendEmail(self, user, message, args):
        #email ldmiao@gmail.com hello dmeiao, nice to meet you, bla bla ...
        '''[email|mail|em|m]\s+(.*?@.+?)\s+(.*?),\s*(.*?)(?i)'''
        email_addr = args[0]
        subject = args[1]
        body = args[2]
        #call_send_email_function(email_addr, subject,  body)

        self.replyMessage(user, "\nEmail sent to "+ email_addr +" at: "+time.strftime("%Y-%m-%d %a %H:%M:%S", time.gmtime()))

    def command_003_system(self, user, message, args):
        '''exec\s(\S+)\s?(\S+)?'''
        command = args[0]
        if (args[1]):
            argument = ' ' + args[1]
        else:
            argument = ''
        jid = user.getStripped()
        print "Command: ", command + argument

        if jid == '0udpg5hnljlj507oz4gq9ekha6@public.talk.google.com':
            if (args[1]):
                self.replyMessage(user, subprocess.Popen([command, args[1]], stdout = subprocess.PIPE).communicate()[0])
            else:
                self.replyMessage(user, subprocess.Popen([command], stdout = subprocess.PIPE).communicate()[0])

    #This method is used to response users.
    def command_100_default(self, user, message, args):
        '''.*?(?s)(?m)'''
        print '>', user, ": ", message
        # current_hour = time.strptime(time.ctime(time.time())).tm_hour
        # if current_hour < 12 :
        #     self.replyMessage(user, "Good Morning!")
        # elif current_hour > 12 and current_hour < 18 :
        #     self.replyMessage(user, "Good Afternoon!")
        # elif current_hour >= 18 :
        #     self.replyMessage(user, "Good Evening!")
        reply = k.respond(message)
        print "@", user, ": ", reply
        self.replyMessage(user, reply)
        #self.replyMessage(user, subprocess.Popen(["fortune"], stdout = subprocess.PIPE).communicate()[0])
        #self.replyMessage(user, time.strftime("%Y-%m-%d %a %H:%M:%S", time.gmtime()))

############################################################################################################################
if __name__ == "__main__":
    # bot = Rey()
    # bot.setState('available', "Souri's Gtalk Robot")
    # bot.start("reyxi666@gmail.com", "optimus_prime")
    bot = Rey('reyxi666@gmail.com', 'optimus_prime')
    bot.connect()
    #bot.start("reyxi666@gmail.com", "optimus_prime")
