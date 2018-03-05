#---------------------------------------
# Import Libraries
#---------------------------------------
import codecs
import datetime
import json
import os
import re
import sys
import clr
import random

clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#---------------------------------------
# [Required] Script Information
#---------------------------------------
ScriptName = "SubStreakAppreciation"
Website = "https://joachimdalen.no"
Description = "Post one emote per month of the sub streak"
Creator = "JoachimDalen"
Version = "1.0.1.0"

#---------------------------------------
# Set Variables
#---------------------------------------
m_emotes = ""
m_message = ""
m_settings_file = os.path.join(os.path.dirname(__file__), "settings.json")
m_usernotice_regex = re.compile(
    r"(?:^(?:@(?P<irctags>[^\ ]*)\ )?:tmi\.twitch\.tv\ USERNOTICE)")
#---------------------------------------
# [Required] Intialize Data (Only called on Load)
#---------------------------------------


def Init():
    Parent.Log(ScriptName, "Loaded script")
    LoadSettings()
    return


def ReloadSettings(jsonData):
    LoadSettings()
    return


def getEmoteCombo(streak):
    emotes = list(map(lambda _: random.choice(m_emotes), range(streak)))
    return " ".join(emotes)


def Unload():
    # Triggers when the bot closes / script is reloaded
    return
#---------------------------------------
# [Required] Execute Data / Process Messages
#---------------------------------------
def getMonths(tags):
    try:
        streak = int(tags["msg-param-months"])
    except ValueError:
        streak = 1
    return streak

def Execute(data):
    # We only want raw data from Twitch to check for sub
    if data.IsRawData() and data.IsFromTwitch():

        # Apply regex on raw data to detect subscription usernotice
        usernotice = m_usernotice_regex.search(data.RawData)
        if usernotice:

            # Parse IRCv3 tags in a dictionary
            tags = dict(re.findall(r"([^=]+)=([^;]*)(?:;|$)",
                        usernotice.group("irctags")))
            # user-id> User id of the subscriber/gifter
            # login> User name of the subscriber/gifter
            # display-name> Display name of the subscriber/gifter
            # msg-id> Type of notice; sub, resub, charity, subgift
            # msg-param-months> Amount of consecutive months
            # msg-param-sub-plan> sub plan; prime, 1000, 2000, 3000
            # msg-param-recipient-id> user id of the gift receiver
            # msg-param-recipient-user-name> user name of the gift receiver
            # msg-param-recipient-display-name> display name of the gift receiver

            # Gifted subscription
            if tags["msg-id"] == "resub":
                streak = getMonths(tags)
                emotes = getEmoteCombo(streak)
                formattedMessage = m_message.format(tags["login"], streak, emotes)
                Parent.SendTwitchMessage(formattedMessage)
                Parent.Log(ScriptName, 'Sent sub message for {}'.format(tags["login"]))
            
    return

#---------------------------------------
# [Required] Tick Function
#---------------------------------------
def Tick():
    return


def LoadSettings():
    with codecs.open(m_settings_file, encoding="utf-8-sig", mode="r") as f:
        settings=json.load(f, encoding="utf-8")
    global m_emotes
    m_emotes=settings['emotes'].split(",")
    global m_message
    m_message=settings['message']
    return


