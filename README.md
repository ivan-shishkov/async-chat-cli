# Async Chat Reader

This script allows you to read messages from the chat and save them to a text 
file using the [asyncio](https://docs.python.org/3/library/asyncio.html) module.

## How to install

For script to work, you need to install **Python 3.7** and then install all dependencies:

```bash

$ pip install -r requirements.txt

```

## How to set up

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

## How to launch

```bash

$ export CHAT_HOST=your.chat.host
$ python chat_reader.py 

```