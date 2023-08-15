import pytest

from discord_alert.discord_alert import DiscordAlert


def alert(hook: DiscordAlert, custom_msg=""):
    """
    Decorator function for error handling and sending alerts via webhook.

    Args:
        func (callable): The function to be wrapped.

    Returns:
        callable: The wrapped function.
    """

    def handler(func):
        def wrapper(*args, **kwargs):
            """
            Wrapper function that executes the wrapped function and handles any exceptions.

            Args:
                *args: Positional arguments to be passed to the wrapped function.
                **kwargs: Keyword arguments to be passed to the wrapped function.

            Returns:
                None
            """
            try:
                func(*args, **kwargs)  # Execute the wrapped function
            except Exception as e:
                # Handle the exception by sending an alert via webhook

                hook.send_alert(
                    "Alert sended via webhook",
                    custom_msg + str(e),
                    0x00FF00,
                    "thumbnail",
                )

        return wrapper

    return handler


@pytest.fixture
def hook():
    return DiscordAlert()


def test_alert(hook):
    assert alert(hook, "test")
