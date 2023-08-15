from dataclasses import dataclass

from discord_webhook.webhook import DiscordWebhook


@dataclass(order=True)
class DiscordAlert:
    """
    This class represents a Discord alert and provides a method to send alert messages to a Discord webhook.

    Example Usage:
        # Create a DiscordAlert object
        alert = DiscordAlert()

        # Send an alert message
        alert.send_alert("Alert Title", "Alert Message", 0x00ff00, "thumbnail_url")

    Attributes:
        hook (str): The webhook URL for sending the alert message.

    Methods:
        send_alert(title: str, message: str, color: int, thumbnail_url: str) -> bool:
            Sends an alert message to the Discord webhook.

            Args:
                title (str): The title of the alert message.
                message (str): The message content of the alert.
                color (int): The color of the alert message.
                thumbnail_url (str): The URL of the thumbnail image for the alert.

            Returns:
                bool: True if the alert message was successfully sent, False otherwise.
    """

    hook: str = ""

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
