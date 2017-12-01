import random
import requests
import re

router_login = {}
people = []


def init(config):
    global router_login
    global people
    router_login = config.router
    people = config.people


def list_actions():
    """ A list of actions in this file that can be called """
    return [
        {
            "type": "message",
            "description": "See who's in!",
            "content": ["who is in"],
            "function": "whos_in"
        },
        {
            "type": "message",
            "description": "Who's turn to make tea?",
            "content": ["tea", "brew", "splosh"],
            "function": "tea"
        }
    ]


def whos_in(event):
    people_in = get_people()
    if len(people_in) == 0:
        output = "Only me :'("
    elif len(people_in) == 1:
        output = "Just %s" % people_in[0]
    else:
        output = ", ".join(str(name) for name in people_in)

    return {
        "user": event["user"],
        "channel": event["channel"],
        "event": "asked who was in,",
        "output": output
    }


def tea(event):
    people_in = get_people()
    if len(people_in) == 0:
        output = "Looks like I'm making my own tea again :'("
    else:
        output = "%s, get the kettle on" % random.choice(people_in)

    return {
        "user": event["user"],
        "channel": event["channel"],
        "event": "asked who should make the tea,",
        "output": output
    }


def get_people():
    session_id = retrieve_session_id()
    session_cookie = login(session_id)
    people_json = request_json(session_id, session_cookie)
    people = parse_json(people_json)
    logout(session_id, session_cookie)
    return people


def retrieve_session_id():
    url = router_login["url"]
    r = requests.head(url)
    return re.search("%s(.*)%s" % ("=", "; "),
                     r.headers["Set-Cookie"]).group(1)


def login(session_id):
    url = "%s/goform/login" % router_login["url"]
    data = {
        "usr": router_login["username"],
        "pwd": router_login["password"],
        "preSession": session_id
    }
    r = requests.post(url, data=data)
    return re.search("%s(.*)%s" % ("sessionindex=", "; "),
                     r.headers["Set-Cookie"]).group(1)


def request_json(session_id, session_cookie):
    url = "%s/data/getConnectInfo.asp" % router_login["url"]
    cookies = {
        "preSession": session_id,
        "sessionindex": session_cookie
    }
    r = requests.get(url, cookies=cookies)
    return r.json()


def logout(session_id, session_cookie):
    url = "%s/goform/logout" % router_login["url"]
    cookies = {
        "preSession": session_id,
        "sessionindex": session_cookie
    }
    r = requests.get(url, cookies=cookies)


def parse_json(json):
    people_in = []
    for person, person_macs in people.iteritems():
        for device in json:
            if (device["macAddr"] in person_macs and
                    device["online"] == "active"):
                people_in.append(person)
                break

    return people_in
