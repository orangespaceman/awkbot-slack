#!env/bin/python

from slackclient import SlackClient
from importlib import import_module
from time import sleep
import config
import os


class Bot():
    def __init__(self, config):

        self.config = config

        self.connect()
        self.gather_commands()
        self.listen()

    def connect(self):
        """ connect to slack """

        self.sc = SlackClient(self.config.slack["api_key"])
        self.users = self.sc.api_call("users.list")
        self.channels = self.sc.api_call("channels.list", exclude_archived=1)

        self.debug_channel = self.get_channel_id_by_name(
            self.config.slack["debug_channel"])

        self.bot_user = self.get_user_id_by_name(
            self.config.slack["bot_name"])

    def gather_commands(self):
        """ load all commands from sub-modules """

        self.modules = {}
        self.actions = {}

        for root, dirs, files in os.walk("commands"):
            for file in files:

                if (not file.endswith(".py")) or file.startswith("__"):
                    continue

                path_name = root.replace("/", ".")
                module_name = file.replace(".py", "")
                module = import_module("%s.%s" % (path_name, module_name))

                init = getattr(module, "init")
                init(self.config)

                list_actions = getattr(module, "list_actions")

                self.modules[module_name] = module
                self.actions[module_name] = list_actions()

    def listen(self):
        """ listen for messages from slack """
        READ_WEBSOCKET_DELAY = 1
        if self.sc.rtm_connect():
            while True:
                events = self.sc.rtm_read()
                for event in events:
                    self.process_event(event)

                sleep(READ_WEBSOCKET_DELAY)
        else:
            print("Slack connection failed")

    def process_event(self, event):
        """ process event """
        for module_name, module in self.modules.iteritems():
            for action in self.actions[module_name]:
                if (event.get("type") == action["type"]):

                    # filter - message from a public channel?
                    if event.get("type") == "message":
                        channel = event["channel"]
                    elif (event.get("type") == "reaction_added"
                          and "channel" in event["item"]):
                        channel = event["item"]["channel"]
                    else:
                        return

                    if channel[0] != "C":
                        return

                    # filter - submodule requires a specific message?
                    if "content" in action:
                        match = False
                        for message in action["content"]:
                            string = "<@%s> %s" % (self.bot_user, message)
                            if ("text" in event and
                                    event["text"].startswith(string)):
                                match = True
                        if match is False:
                            continue

                    # filter - list help methods?
                    if (event.get("type") == "message" and "text" in event and
                            event["text"] == "<@%s> help" % self.bot_user):
                        self.log_help(event["channel"])

                    func = getattr(module, action["function"])
                    log = func(event)
                    self.log_event(log)

    def log_event(self, log):
        """log event"""
        if log is None:
            return

        if self.debug_channel is None:
            return

        user = self.get_user_name_by_id(log["user"])
        channel = self.get_channel_name_by_id(log["channel"])

        self.sc.rtm_send_message(self.debug_channel,
                                 "%s %s in %s" % (user, log["event"], channel))

        if "output" in log:
            self.sc.rtm_send_message(log["channel"], log["output"])

    def log_help(self, channel):
        msg = "Available commands:\r"
        for module_name, module in self.modules.iteritems():
            msg += "\r_%s:_\r" % module_name
            for action in self.actions[module_name]:
                if ("content" in action):
                    msg += "- *@%s %s*: %s\r" % (self.config.slack['bot_name'],
                                                 '/'.join(action["content"]),
                                                 action["description"])
                else:
                    msg += " - %s\r" % (action["description"])
        self.sc.rtm_send_message(channel, msg)

    def get_user_name_by_id(self, user_id):
        for user in self.users["members"]:
            if user["id"] == user_id:
                return user["name"]
        return "someone"

    def get_user_id_by_name(self, user_name):
        for user in self.users["members"]:
            if user["name"] == user_name:
                return user["id"]

    def get_channel_name_by_id(self, channel_id):
        for channel in self.channels["channels"]:
            if channel["id"] == channel_id:
                return "#%s" % channel["name"]
        return "a channel"

    def get_channel_id_by_name(self, channel_name):
        for channel in self.channels["channels"]:
            if channel["name"] == channel_name:
                return channel["id"]


awkbot = Bot(config)
