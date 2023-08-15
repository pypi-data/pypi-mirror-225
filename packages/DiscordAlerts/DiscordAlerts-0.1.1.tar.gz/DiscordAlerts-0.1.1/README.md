
# DiscordAlerts Documentation

## Table of Contents

- [DiscordAlerts Documentation](#discordalerts-documentation)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Simple Usage](#simple-usage)
  - [Sub-modules](#sub-modules)
  - [alerts](#alerts)
    - [`alert(hook: DiscordAlert, custom_msg='')`](#alerthook-discordalert-custom_msg)
  - [Module `discord_alert`](#module-discord_alert)
  - [Class `DiscordAlert`](#class-discordalert)
    - [Example Usage](#example-usage)
    - [Attributes](#attributes)
    - [Method `send_alert(title: str, message: str, color: int, thumbnail_url: str) -> bool`](#method-send_alerttitle-str-message-str-color-int-thumbnail_url-str---bool)

## Introduction

Welcome to the `DiscordAlerts` documentation. This document provides information on how to use the `DiscordAlerts` package.

## Simple Usage

To implement an alert to one function, you need to call a `DiscordAlert` object and build this object with your Discord hook. Look at the example below:

```python
from discord_alert.discord_alert import DiscordAlert
from alerts.alerts import alert

hook = DiscordAlert(hook="Your URL hook here")

@alert(hook=hook, custom_msg="You can add a custom message here")
def add(x, y):
    return x + y
```

## Sub-modules
## alerts 

### `alert(hook: DiscordAlert, custom_msg='')`

Decorator function for error handling and sending alerts via webhook.

This function takes a DiscordAlert object and an optional custom message as arguments. It returns a decorator function that wraps another function and handles any exceptions that occur during its execution. If an exception occurs, it sends an alert via a webhook using the DiscordAlert object.

**Args:**

- `hook`: An instance of the DiscordAlert class representing a webhook URL.
- `custom_msg`: An optional custom message to be included in the alert.

**Returns:**

A callable wrapper function.

**Example Usage:**

```python
@alert(hook=DiscordAlert(hook="webhook_url"), custom_msg="Custom message: ")
def my_function():
    # Code to be executed
    pass

my_function()
```
## Module `discord_alert`

## Class `DiscordAlert`

This class represents a Discord alert and provides a method to send alert messages to a Discord webhook.

### Example Usage

```python
# Create a DiscordAlert object
alert = DiscordAlert(hook="Your Hook")

# Send an alert message
alert.send_alert("Alert Title", "Alert Message", 0x00ff00, "thumbnail_url")
```

### Attributes

- `hook`: The webhook URL for sending the alert message.

### Method `send_alert(title: str, message: str, color: int, thumbnail_url: str) -> bool`

Sends an alert message to the Discord webhook.

**Args:**

- `title (str)`: The title of the alert message.
- `message (str)`: The message content of the alert.
- `color (int)`: The color of the alert message.
- `thumbnail_url (str)`: The URL of the thumbnail image for the alert.

**Returns:**

- `bool`: True if the alert message was successfully sent, False otherwise.

```python
def send_alert(
    self, title: str, message: str, color: int, thumbnail_url: str
) -> bool:
    """
    Sends an alert message to the Discord webhook.

    Args:
        title (str): The title of the alert message.
        message (str): The message content of the alert.
        color (int): The color of the alert message.
        thumbnail_url (str): The URL of the thumbnail image for the alert.

    Returns:
        bool: True if the alert message was successfully sent, False otherwise.
    """
    embeds = [
        {
            "title": title,
            "description": message,
            "color": color,
            "thumbnail": {"url": thumbnail_url},
        },
    ]
    try:
        webhook = DiscordWebhook(url=self.hook, embeds=embeds)
        webhook.execute()
        return True
    except Exception:
        return False
```



