# Seiketsu-API

## Installation

Install the library using `pip`:

```
pip install seiketsu-api
```

## Usage

First, import the `ApiSeiketsu` class from the library:

```python
from seiketsu_api import ApiSeiketsu
```

### Initialize the ApiSeiketsu object

Create an instance of the `ApiSeiketsu` class:

```python
seiketsu = ApiSeiketsu()
```

### Read message

To get the latest message, call the `read_message` method::

```python
sender, message_text = seiketsu.read_message()
```

`sender` contains the sender's nickname, `message_text` contains the text of the message.

### Write message

To write a new chat message, call the `write_message` method, passing alias and message_text as arguments:

```python
seiketsu.write_message(alias="John", message_text="Hello, world!")
```

If you want `read_message` to run all the time you can loop:

```python
while True:
    sender, message_text = seiketsu.read_message()
    print(f'{sender}: {message_text}')
```

## Example

Here is a simple example demonstrating the use of the Seiketsu-API. Reads the last message, checks if the bot wrote it himself, if not, repeats it.

```python
from api_seiketsu import ApiSeiketsu

seiketsu = ApiSeiketsu() # Initialize seiketsu API

aliasBot = "TestBot" # Name for Bot

while True:
    # Waiting for a new message
    sender, message = seiketsu.read_message()

    # Checking that this is not a message from a bot
    if sender != aliasBot + '#BOT':
        # Sending a reply message
        seiketsu.write_message(alias=aliasBot, message_text=message)

    # Message output to console
    print(f'Repeated message: {aliasBot}: {message}')
```
