import sys, os

sys.path.append(os.getcwd() + '/..')

from brickscout.api import BrickScoutAPI


api = BrickScoutAPI(username='brickstarbelgium', password='Planten11$')

# order = api.orders.get('406c2bfa-1bc1-40ae-9b25-8e6e13ee3205')
order = api.orders.get('6b7519d1-18f1-4308-9142-f935d4659642')

print(vars(order.payment))
print(vars(order.payment.paymentAmount))