import requests
from django.conf import settings

class IctApi(object):

    def __init__(self):
        self.key = settings.API_AUTH
        self.url = settings.API_ENDPOINT

    def do_request(self, action, data):
        data['password'] = self.key
        data['action'] = action
        print('request: ', data)
        ret = requests.post(self.url, data)
        return ret.json()

    def signup(self, discord_id):
        return self.do_request('signup', {'username': discord_id})

    def list_nodes(self, discord_id):
        return self.do_request('get_nodes', {'username': discord_id})

    def remove_node(self, discord_id, address):
        res = self.list_nodes(discord_id)
        if address not in res.get('nodes', []):
            return {'success': False, 'error': 'You are only allowed to remove your own nodes, use the `!listnodes` command to find the ones you have!'}

        return self.do_request('remove_node', {'address': address})
