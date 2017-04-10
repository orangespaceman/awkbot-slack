import subprocess


def init(config):
    pass


def list_actions():
    """ A list of actions in this file that can be called """
    return [
        {
            "type": "message",
            "description": "Say some words!",
            "content": ["say"],
            "function": "parse_say"
        }
    ]


def parse_say(event):
    if "text" not in event:
        return

    text = event["text"].split("say", 1)[1]
    say(text)
    return {
        "user": event["user"],
        "channel": event["channel"],
        "event": "made me say _%s_" % text
    }


def say(content):
    """ say the words! """
    return subprocess.call(["say", content])
