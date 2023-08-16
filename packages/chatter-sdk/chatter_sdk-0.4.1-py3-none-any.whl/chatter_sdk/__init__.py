from .chatter import chatter


def api_key_setter(key):
    chatter.api_key = key


def render_prompt(id, variables, debug=False):
    return chatter.render_prompt(id, variables, debug)


def api_key_getter():
    return chatter.api_key


api_key = property(api_key_getter, api_key_setter)

