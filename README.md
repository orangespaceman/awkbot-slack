# Awkbot for Slack

_Awkbot_: A custom slackbot

## Available commands

There are a number of commands that _Awkbot_ will respond to. To see a list, either look through the `commands` directory, or post a message in Slack:

```
@awkbot help
```

(assuming you have called the bot user _awkbot_)


## Running Awkbot

Once you have run through the installation steps below, you can start _Awkbot_ with the following commands:

```
source env/bin/activate
python awkbot.py
```

### Installation

There are two parts to installing _Awkbot_: the creation of a bot user through Slack, and the installation of this script on a machine.

#### Slackbot creation

- Install the _Bot_ Slack integration. Visit the following URL, replacing `{SLACK-ACCOUNT-NAME}` with your account:

  ```
  https://{SLACK-ACCOUNT-NAME}.slack.com/apps/A0F7YS25R-bots
  ```

- Create a new bot user - e.g. `@awkbot`

  ```
  https://{SLACK-ACCOUNT-NAME}.slack.com/apps/new/A0F7YS25R-bots
  ```

- Once saved, take a note of the Slackbot API key

- Create a new channel in Slack for debug messages - e.g. `#awkward-bot`

- Add the bot user to all channels that you want it to work in

#### Installation on Local machine

- Clone this repo

- Duplicate the file `config.example.py` - call it `config.py`

  ```
  cp config.example.py config.py
  ```

- Add the Slackbot API key, bot name and debug channel name to the config file

- Install pip, if you don't have it:

  ```
  sudo easy_install pip
  ```

- Install virtualenv, if you don't have it:

  ```
  sudo pip install virtualenv
  ```

- Create a virtualenv:

  ```
  virtualenv env
  ```

- Install dependencies

  ```
  pip install -r requirements.txt
  ```

- Run _Awkbot_:

  ```
  python awkbot.py
  ```

## Creating new Awkbot commands

Create a new file in the `/commands` directory

Follow the conventions of the existing commands to see how to set the relevant inputs and outputs...
