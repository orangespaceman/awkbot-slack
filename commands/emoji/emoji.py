import os
import subprocess

sounds = {}

media_player = ""


def init(config):
    global media_player
    media_player = config.emoji["media_player"]
    parse_sounds()


def list_actions():
    """ A list of actions in this file that can be called """
    return [
        {
            "type": "message",
            "description": "Some emoji trigger a sound effect...",
            "function": "parse_message"
        },
        {
            "type": "reaction_added",
            "description": "Some emoji reactions trigger a sound effect...",
            "function": "parse_reaction"
        }
    ]


def parse_sounds():
    for root, dirs, files in os.walk("commands/emoji/sfx"):
        for file in files:

            if (not file.endswith(".mp3")):
                continue

            sounds.update({
                file.replace(".mp3", ""): "%s/%s" % (root, file)
            })


def parse_message(event):
    if "text" not in event:
        return

    text = event["text"]
    for sound, sound_file in sounds.iteritems():
        if ":%s:" % sound in text:
            play_sound(sound_file)
            return {
                "user": event["user"],
                "channel": event["channel"],
                "event": "triggered the sound _%s_ with an emoji" % sound
            }


def parse_reaction(event):
    reaction = event["reaction"]
    for sound, sound_file in sounds.iteritems():
        if sound == reaction:
            play_sound(sound_file)
            return {
                "user": event["user"],
                "channel": event["item"]["channel"],
                "event": "triggered the sound _%s_ with a reaction" % sound
            }


def play_sound(sound):
    return subprocess.call([media_player, sound])
