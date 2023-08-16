from .chatter import chatter


def set_api_key(key: str):
    print(f"Setting API key: {key}")
    chatter.api_key = key


def get_api_key():
    print(f"Getting API key: {chatter.api_key}")
    return chatter.api_key


api_key = property(get_api_key, set_api_key)


def render_prompt(id: str, variables: dict, debug=False):
    return chatter.render_prompt(id, variables, debug)


