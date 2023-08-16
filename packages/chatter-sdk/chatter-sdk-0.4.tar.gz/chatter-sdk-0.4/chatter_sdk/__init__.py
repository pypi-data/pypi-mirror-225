from .chatter import chatter


def api_key_setter(self, key):
    chatter.api_key = key


def render_prompt(self, id, variables, debug=False):
    return chatter.render_prompt(id, variables, debug)


api_key = property(chatter.api_key, api_key_setter)
