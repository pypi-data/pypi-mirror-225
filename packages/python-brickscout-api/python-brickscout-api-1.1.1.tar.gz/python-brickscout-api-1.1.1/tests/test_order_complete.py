import sys, os

sys.path.append(os.getcwd() + '/..')

from brickscout.api import BrickScoutAPI



api = BrickScoutAPI(username='brickstarbelgium', password='Planten11$')
order = api.orders.get('4d4f7a2f-dd78-42ab-a209-6ad6d13fa75a')
api.orders.mark_as_packed(order)
api.orders.mark_as_shipped(order)