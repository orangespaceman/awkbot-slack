import subprocess


def init(config):
    pass


def list_actions():
    """ A list of actions in this file that can be called """
    return [
        {
            "type": "message",
            "description": "Retrieve info about the currently playing track",
            "content": ["info", "song"],
            "function": "info"
        },
        {
            "type": "message",
            "description": "Play Spotify",
            "content": ["play"],
            "function": "play"
        },
        {
            "type": "message",
            "description": "Pause Spotify",
            "content": ["pause", "stop"],
            "function": "pause"
        },
        {
            "type": "message",
            "description": "Skip track",
            "content": ["skip", "next"],
            "function": "skip"
        },
        {
            "type": "message",
            "description": "Back to the previous track",
            "content": ["back", "previous"],
            "function": "back"
        }
    ]


def info(event):
    data = spotify_command("info")
    data = data.strip().split("\n")
    data = {"id": data[0], "artist": data[1], "track": data[2]}
    message = "Track: *%s* \n Artist: *%s* \n Link: %s" % (data["track"],
                                                           data["artist"],
                                                           data["id"])

    return {
        "user": event["user"],
        "channel": event["channel"],
        "event": "triggered spotify current song details",
        "output": message
    }


def play(event):
    spotify_command("play")
    return {
        "user": event["user"],
        "channel": event["channel"],
        "event": "triggered spotify play"
    }


def pause(event):
    spotify_command("pause")
    return {
        "user": event["user"],
        "channel": event["channel"],
        "event": "triggered spotify pause"
    }


def skip(event):
    spotify_command("skip")
    return {
        "user": event["user"],
        "channel": event["channel"],
        "event": "triggered spotify skip"
    }


def back(event):
    spotify_command("back")
    return {
        "user": event["user"],
        "channel": event["channel"],
        "event": "triggered spotify back"
    }


def spotify_command(command):
    script = "./commands/spotify/applescript/%s.applescript" % command
    osa = subprocess.Popen(['osascript', script],
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE)

    result = osa.communicate()[0]
    return result
