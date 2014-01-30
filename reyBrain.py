import sys
import time
import os
import subprocess
import aiml
import configparser
from os import listdir
from os.path import isfile, join

from PyGtalkRobot import GtalkRobot

# ensure unicode is handled properly incase python is not v3.0
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input

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
class SampleBot(GtalkRobot):

    #Regular Expression Pattern Tips:
    # I or IGNORECASE <=> (?i)      case insensitive matching
    # L or LOCALE <=> (?L)          make \w, \W, \b, \B dependent on the current locale
    # M or MULTILINE <=> (?m)       matches every new line and not only start/end of the whole string
    # S or DOTALL <=> (?s)          '.' matches ALL chars, including newline
    # U or UNICODE <=> (?u)         Make \w, \W, \b, and \B dependent on the Unicode character properties database.
    # X or VERBOSE <=> (?x)         Ignores whitespace outside character sets

    def notifysend(data):
        data = 'Rexi:' + data
        subprocess.Popen(['notify-send', data], stdout = subprocess.PIPE).communicate()[0]

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
    #read config file
    config = configparser.ConfigParser()
    config.read('rey.conf')
    jid = config.get('rey', 'jid')
    password = config.get('rey', 'password')
    bot = SampleBot()
    bot.setState('available', "Souri's Gtalk Robot")
    bot.start(jid, password)
