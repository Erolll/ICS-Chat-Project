"""
Created on Sun Apr  5 00:00:32 2015

@author: zhengzhang
"""
from chat_utils import *
import json
from grabFinancialData import *
from chatSystemGUI import *

import http.cookiejar
import urllib.request
import requests
import bs4

class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s
        self.myPort = []

    #All business files
    def theNews(self):
        theDataDict = grab_financial_news()
        fullData = "\nTrending News...\n"
        for x in range(0,5):
            for k,v in theDataDict.items():
                fullData = fullData + k + ": " + v[x]
                fullData += "\n"
            fullData += "\n"
        return fullData

    def theCurrencies(self):
        theDataDict = grab_financial_currencies()
        fullData = "\nTop CryptoCurrencies...\n"
        for x in range(0,5):
            for k,v in theDataDict.items():
                fullData = fullData + " "*10 + k + ": " + v[x]
                fullData += "\n"
            fullData += "\n"
        return fullData

    def theCommodities(self):
        theDataDict = grab_financial_commodities()
        fullData = "\nTop Commodities...\n"
        for x in range(0,5):
            for k,v in theDataDict.items():
                fullData = fullData + " "*10 + k + ": " + v[x]
                fullData += "\n"
            fullData += "\n"
        return fullData
        
    def theTicker(self,my_msg):
        theDataDict = grab_financial_data(my_msg[2:])
        fullData = "\nSnapshot for: " + str(theDataDict["Name"]) + "...\n"
        for k,v in theDataDict.items():
            fullData = fullData + " "*10 + k + ": " + v
            fullData += "\n"
        return fullData

    def isTicker(self, msg):
        try:
            self.theTicker(msg)
            return True
        except:
            return False
        
    def theFinanceFull(self):
        theDataDict = grab_financial_full()
        fullData = "\nTop World Indices...\n"
        for x in range(0,5):
            for k,v in theDataDict.items():
                fullData = fullData + " "*10 + k + ": " + v[x]
                fullData += "\n"
            fullData += "\n"
        return fullData

    def financeCases(self, my_msg):
        if my_msg[0] == "=":                
            if my_msg[1:] == "pc":
                self.myPort = []
                self.out_msg += "Cleared portfolio!"
                
            elif my_msg[1:] == "bp":
                if len(self.myPort) == 0:
                    theMsg = "Portfolio is empty!"
                else:
                    theMsg = "Listing portfolio...\n"
                    for port in self.myPort:
                        port = "!!" + port
                        theMsg = theMsg + self.theTicker(port)
                self.out_msg += theMsg
                
            elif my_msg[1:] == "bNews":
                self.out_msg += self.theNews()
                
            elif my_msg[1:] == "bCommodities":
                self.out_msg += self.theCommodities()
                                
            elif my_msg[1:] == "bCryptocurrencies":
                self.out_msg += self.theCurrencies()

            elif my_msg[1:] == "bWorld":
                self.out_msg += self.theFinanceFull()

            elif my_msg[1] == "r":
                try:
                    self.myPort.remove(my_msg[2:])
                    self.out_msg += "Removed an item!"
                    print(self.myPort)
                except:
                    self.out_msg += "Tried to remove but not in portfolio!"
                                
            elif (my_msg[1] == "b"):
                try:
                    self.out_msg += self.theTicker(my_msg)
                except:
                    self.out_msg += "Attempted invalid ticker!"
                                
            elif (my_msg[1] == "p") & (self.isTicker(my_msg)):
                if my_msg[2:] not in self.myPort:
                    self.myPort.append(my_msg[2:])
                    self.out_msg += "Added ticker to portfolio!"
                else:
                    self.out_msg += "Already added ticker into portfolio!"
                                    
            else:
                self.out_msg += "Attempted invalid ticker!"

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me

    def connect_to(self, peer):
        msg = json.dumps({"action":"connect", "target":peer})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with '+ self.peer + '\n'
            return (True)
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return(False)

    def disconnect(self):
        msg = json.dumps({"action":"disconnect"})
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''

    def proc(self, my_msg, peer_msg):
        self.out_msg = ''
        
#==============================================================================
# Once logged in, do a few things: get peer listing, connect, search
# And, of course, if you are so bored, just go
# This is event handling instate "S_LOGGEDIN"
#==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:

                if my_msg == 'q':
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE
                    
                #Business
                if my_msg[0] == "=":
                    self.financeCases(my_msg)
                    
                elif my_msg == 'time':
                    mysend(self.s, json.dumps({"action":"time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in

                elif my_msg == 'who':
                    mysend(self.s, json.dumps({"action":"list"}))
                    logged_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += logged_in

                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer) == True:
                        self.state = S_CHATTING
                        self.out_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                        self.out_msg += '-----------------------------------\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'

                elif my_msg[0] == '?':
                    term = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"search", "target":term}))
                    search_rslt = json.loads(myrecv(self.s))["results"].strip()
                    if (len(search_rslt)) > 0:
                        self.out_msg += search_rslt + '\n\n'
                    else:
                        self.out_msg += '\'' + term + '\'' + ' not found\n\n'

                elif my_msg[0] == 'p' and my_msg[1:].isdigit():
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"poem", "target":poem_idx}))
                    poem = json.loads(myrecv(self.s))["results"]
                    if (len(poem) > 0):
                        self.out_msg += poem + '\n\n'
                    else:
                        self.out_msg += 'Sonnet ' + poem_idx + ' not found\n\n'

                else:
                    self.out_msg += menu

            if len(peer_msg) > 0:
                try:
                    peer_msg = json.loads(peer_msg)
                except Exception as err :
                    self.out_msg += " json.loads failed " + str(err)
                    return self.out_msg

                if peer_msg["action"] == "connect":
                    # ----------your code here------#
                    print(peer_msg)
                    self.peer = peer_msg["from"]
                    self.out_msg += 'Request from ' + self.peer + '\n'
                    self.out_msg += 'You are connected with ' + self.peer
                    self.out_msg += '. Chat away!\n\n'
                    self.out_msg += '------------------------------------\n'
                    self.state = S_CHATTING
                    # ----------end of your code----#

#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_CHATTING:
            if len(my_msg) > 0:     # my stuff going out
                ###
                if my_msg[0] == "=":
                    self.financeCases(my_msg)
                    my_msg = ""
                    my_msg += self.out_msg
                    
                ###
                #So my_msg is exactly what other person sees
                #self.out_msg is what user sees
                
                mysend(self.s, json.dumps({"action":"exchange", "from":"[" + self.me + "]", "message":my_msg}))
                if my_msg == 'bye':
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''
                    
                    
            if len(peer_msg) > 0:  # peer's stuff, coming in
                # ----------your code here------#
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.out_msg += "(" + peer_msg["from"] + " joined)\n"
                elif peer_msg["action"] == "disconnect":
                    self.out_msg += peer_msg["message"]
                    self.state = S_LOGGEDIN
                else:
                    self.out_msg += peer_msg["from"] + ": "+ peer_msg["message"]
                # ----------end of your code----#
            if self.state == S_LOGGEDIN:
                # Display the menu again
                self.out_msg += menu
#==============================================================================
# invalid state
#==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)

        return self.out_msg
        

