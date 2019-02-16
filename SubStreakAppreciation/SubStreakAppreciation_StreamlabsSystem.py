# ---------------------------------------
# Import Libraries
# ---------------------------------------
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

# ---------------------------------------
# [Required] Script Information
# ---------------------------------------
ScriptName = "SubStreakAppreciation"
Website = "https://joachimdalen.no"
Description = "Post one emote per month of the sub streak"
Creator = "JoachimDalen"
Version = "1.1.2.0"

# ---------------------------------------
# Set Variables
# ---------------------------------------
m_emotes = ""
m_message = ""
m_settings_file = os.path.join(os.path.dirname(__file__), "settings.json")
m_usernotice_regex = re.compile(
    r"(?:^(?:@(?P<irctags>[^\ ]*)\ )?:tmi\.twitch\.tv\ USERNOTICE)")
# ---------------------------------------
# [Required] Intialize Data (Only called on Load)
# ---------------------------------------


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
# ---------------------------------------
# [Required] Execute Data / Process Messages
# ---------------------------------------


def getMonths(tags):
    try:
        streak = int(tags["msg-param-cumulative-months"])
    except ValueError:
        streak = 1
    return streak


def Execute(data):
    if data.IsRawData() and data.IsFromTwitch():
        usernotice = m_usernotice_regex.search(data.RawData)
        if usernotice:
            tags = dict(re.findall(r"([^=]+)=([^;]*)(?:;|$)",
                                   usernotice.group("irctags")))
            if tags["msg-id"] == "resub":
                streak = getMonths(tags)
                emotes = getEmoteCombo(streak)
                formattedMessage = m_message.format(
                    tags["login"], streak, emotes)
                Parent.SendStreamMessage(formattedMessage)
                Parent.Log(
                    ScriptName, 'Sent sub message for {}'.format(tags["login"]))
    return

# ---------------------------------------
# [Required] Tick Function
# ---------------------------------------


def Tick():
    return


def LoadSettings():
    with codecs.open(m_settings_file, encoding="utf-8-sig", mode="r") as f:
        settings = json.load(f, encoding="utf-8")
    global m_emotes
    m_emotes = settings['emotes'].split(",")
    global m_message
    m_message = settings['message']
    return
