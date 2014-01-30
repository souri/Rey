Rey
===

Rey is an intelligent chat-bot written in python. It's based on AIML. Supports XMPP and Hangouts for now.

##Requirements
    - AIML
    - configparser
    - xmpp, sleekxmpp

##Protocol support
    - XMPP
    - Google Hangouts (TODO)
    - IRC (TODO)

##Configuration

You need to create a file - rey.conf. Required contents:
[rey]
jid: xxxxxx@gmail.com
password: xxxxxxxxxxx
server: talk.google.com
nick: Rey

##Example conversation

Rey:  What is your favorite color?
me:  blue
Rey:  Green.
me:  blue
Rey:  Green.
me:  no blue
Rey:  Great.. Green.
me:  green
Rey:  green is a pretty color.
me:  are you joking
Rey:  Yes I am. Sorry if you don't appreciate my sense of humor.




