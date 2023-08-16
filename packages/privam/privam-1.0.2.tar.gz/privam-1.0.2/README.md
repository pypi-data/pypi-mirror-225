# Privam

**privam** is a Pypi package that provides a simple way to create and interact with a bot for the Privam service (https://privam.top/).

## Installation

You can install `privam` using pip:

```bash
pip install privam
```

## Usage
```python
import privam

def hello_command(message):
    sender = message["sender"]
    print(message)
    bot.send(sender, "Hello, {}!".format(sender))

# Create a new PrivamBot instance with your token
bot = PrivamBot("your-token-here")

# Add the 'hello' command to the bot
bot.command("hello", hello_command)

# Start the bot
bot.socket.wait()
```

## Contributing
Contributions are welcome! Please join vnti.top discord server if you have any suggestions or improvements.

## License
This package is open source and available under the MIT License.

*Remember to replace `"your-token-here"` with an actual token in the usage example.*