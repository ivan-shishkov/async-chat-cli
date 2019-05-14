# Async Chat CLI

This solution allows you to read and write chat messages using the command line interface.

## How to install

For script to work, you need to install **Python 3.7** and then install all dependencies:

```bash

$ pip install -r requirements.txt

```

## Async Chat Reader

This script allows you to read messages from the chat and save them to a text 
file using the [asyncio](https://docs.python.org/3/library/asyncio.html) module.

### How to set up

```bash

$ python chat_reader.py -h
usage: chat_reader.py [-h] --host HOST [--port PORT] [--output OUTPUT]

If an arg is specified in more than one place, then commandline values
override environment variables which override defaults.

optional arguments:
  -h, --help       show this help message and exit
  --host HOST      Host for connect to chat. Required [env var: CHAT_HOST]
  --port PORT      Port for connect to chat for reading messages. Default:
                   5000 [env var: CHAT_READ_PORT]
  --output OUTPUT  Filepath for save chat messages. Default: chat.txt [env
                   var: OUTPUT_FILEPATH]

```

### How to launch

```bash

$ export CHAT_HOST='your.chat.host'
$ python chat_reader.py 

```

## Async Chat Writer

This script allows you to write messages in the chat, as well as register the user in the chat and perform its authorization.

### How to set up

```bash

$ python chat_writer.py -h
usage: chat_writer.py [-h] --host HOST [--port PORT] [--nickname NICKNAME]
                      [--token TOKEN] --message MESSAGE

If an arg is specified in more than one place, then commandline values
override environment variables which override defaults.

optional arguments:
  -h, --help           show this help message and exit
  --host HOST          Host for connect to chat. Required [env var: CHAT_HOST]
  --port PORT          Port for connect to chat for writing messages. Default:
                       5050 [env var: CHAT_WRITE_PORT]
  --nickname NICKNAME  User nickname for registering in chat. [env var:
                       CHAT_NICKNAME]
  --token TOKEN        User token for authorisation in chat. [env var:
                       CHAT_AUTH_TOKEN]
  --message MESSAGE    User message for sending to chat. Required [env var:
                       CHAT_MESSAGE]

```

### How to launch

```bash

$ export CHAT_HOST='your.chat.host'
$ export CHAT_NICKNAME='Your nickname'
$ export CHAT_MESSAGE='Your message'
$ python chat_writer.py 

```

# Project Goals

The code is written for educational purposes - this is a lesson in the course on Python and web development on the site [Devman](https://dvmn.org).