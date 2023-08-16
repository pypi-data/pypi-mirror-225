import requests


class _Chatter:
    _api_key = None
    _user_id = None
    _url_prefix = 'https://backend.trychatter.ai/sdk'
    _user = None

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, key):
        print(f"Setting api key: {key}")
        self._api_key = key
        url = f'{self._url_prefix}/auth/{key}'
        response = requests.get(url)
        print(f"Response status: {response.status_code}")
        if response.status_code == 200:
            self._user_id = response.json().get('user_id')
            self._user = response.json().get('user')
        else:
            raise ValueError("Invalid API key.")

    def render_prompt(self, id, variables, debug=False):
        if not self._api_key or not self._user_id:
            raise ValueError("Must authenticate with API key before rendering a prompt.")

        url = f'{self._url_prefix}/prompt/render'
        headers = {'Authorization': f'Bearer {self._api_key}'}
        payload = {
            'user_id': self._user_id,
            'id': id,
            'var_mapping': variables
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code != 200:
            raise ValueError("Error rendering prompt. Response: " + response.text)

        rendered_prompt = response.json().get('prompt')

        if debug:
            print("Debug information about the rendered prompt:", rendered_prompt)

        return rendered_prompt


chatter = _Chatter()

