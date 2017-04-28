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
        }
    ]


def whos_in(event):
    session_id = retrieve_session_id()
    session_cookie = login(session_id)
    people_json = request_json(session_id, session_cookie)
    people = parse_json(people_json)
    logout(session_id, session_cookie)

    return {
        "user": event["user"],
        "channel": event["channel"],
        "event": "asked who was in, ",
        "output": people
    }


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
            if device["macAddr"] in person_macs:
                people_in.append(person)
                break

    if len(people_in) == 0:
        return "Only me :'("
    elif len(people_in) == 1:
        return "Just %s" % people_in[0]
    else:
        return ", ".join(str(name) for name in people_in)
