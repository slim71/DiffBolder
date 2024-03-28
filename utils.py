import Logger

utils_logger = Logger.get_logger(__name__)

def logged_input(prompt: str="") -> str:
    """
    Utility function include the user input to some prompt in the logger itself.

    Args:
        prompt (str, optional): Prompt to the user. Defaults to "".

    Returns:
        str: User input
    """
    user_input = input(prompt)
    utils_logger.debug(f"Input received for prompt \"{prompt}\": {user_input}")
    return user_input