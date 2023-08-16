import sys, os

sys.path.append(os.getcwd() + '/..')

from brickscout.api import BrickScoutAPI


api = BrickScoutAPI(username='brickstarbelgium', password='Planten11$')
cache_handler = api._cache_handler
tokens = api._auth_handler.get_tokens()

print(tokens)

