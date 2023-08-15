from discord_alert.discord_alert import DiscordAlert


def alert(hook: DiscordAlert, custom_msg=""):
    """
    Decorator function for error handling and sending alerts via webhook.

    This function takes a DiscordAlert object and an optional custom message as arguments.
    It returns a decorator function that wraps another function and handles any exceptions that occur during its execution.
    If an exception occurs, it sends an alert via a webhook using the DiscordAlert object.

    Args:
        hook (DiscordAlert): An instance of the DiscordAlert class representing a webhook URL.
        custom_msg (str, optional): An optional custom message to be included in the alert.

    Returns:
        callable: The wrapped function.

    Example Usage:
        @alert(hook=DiscordAlert(hook="webhook_url"), custom_msg="Custom message: ")
        def my_function():
            # Code to be executed
            pass

        my_function()
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
