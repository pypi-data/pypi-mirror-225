# Pywebhk

Pywebhk (pronounced Py-webhook) is an ultra-small Discord webhook handler that allows you to create webhook messages quickly and easily. It provides a simple-to-use interface with methods and classes for handling webhooks.

![license](https://img.shields.io/badge/License-MIT-blue) ![python](https://img.shields.io/badge/Python-%3E%3D3.6-yellow) ![discord-webhook-handler](https://img.shields.io/badge/Another%20Discord%20Webhook%20Handler-True-green)

## Features

- Create and send webhook messages with ease.
- Support for embedding rich content in your messages.
- Lightweight and easy to integrate into your projects.
- Compatible with Python 3.6 and above.

## Installation

You can install Pywebhk using pip:

```bash
pip install pywebhk
```

# Usage Example
```python
from pywebhk.webhook import Webhook
from pywebhk.embed import Embed

webhook_url = "WEBHOOK_URL"
hook = Webhook(webhook_url)

hook.set_content("Hello from main.py!")
hook.set_name("My Webhook")
hook.set_avatar("https://example.com/avatar.png")

embed = Embed(title="My Cool Embed", description="This is a sample embed from main.py.", color=0xFF5733)
embed.set_author(name="Author Name", icon_url="https://example.com/author.png")
embed.add_field(name="Field A", value="Value A", inline=False)
embed.add_field(name="Field B", value="Value B", inline=True)
embed.set_footer(text="Footer text from a really cool embed")

hook.add_embed(embed)

try:
    hook.send()
    print("Webhook message sent successfully from main.py!")
except Exception as e:
    print("Error sending webhook message from main.py:", e)
```

# TODO
- Add File Support
- Some Error Handling
- ~~Minor Documentation~~ **Done**

# License
This project is licensed under the [__MIT License__](LICENSE).