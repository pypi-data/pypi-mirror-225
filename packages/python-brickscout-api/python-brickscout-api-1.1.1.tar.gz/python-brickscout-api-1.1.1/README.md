# python-brickscout-api
Wrapper for the BrickScout API

## Install
This package is published on PyPi: https://pypi.org/project/python-brickscout-api/

Install with pip

```python
pip install python-brickscout-api
```

## Usage

Usage at this point is minimal. I will extend this package as I go and as I need.

### Create connection

You will need your username and password.

Create a new API connection

```python
from brickscout.api import BrickScoutAPI
api = BrickScoutAPI(username='xxx', password='xxx')
```

### Orders

1. Get all open orders

Orders are considered open if they have not been marked as deleted or shipped.

```python
orders = api.orders.get_open_orders()
for order in orders.iterator():
    print(vars(order))
```

2. Retrieve an order

```python
order = api.orders.get(id)
print(vars(order))
```

3. Update an order

```python
order = api.orders.get(id)
order.internalComment = 'this is my new comment'
api.orders.update(order)
```

4. Mark an order as **PAID**

```python
order = api.orders.get(id)
api.orders.mark_as_paid(order)
```

5. Mark an order as **PACKED**

```python
order = api.orders.get(id)
api.orders.mark_as_packed(order)
```

4. Mark an order as **SHIPPED**

```python
order = api.orders.get(id)
api.orders.mark_as_shipped(order)
```

### Error handling

Basic error handling has been added. You can check if an error has occured during a call by checking the ```has_error``` attribute on an object. If the ```has_error``` has been set to ```True```, an ```Error``` object will be attached to the ```error``` attribute of the same object. The ```Error``` object contains following attributes: ```type```, ```exception_code```, ```developer_message```, ```more_info_url``` and ```timestamp```.

```python
order = api.orders.get(id)

if order.has_error:
    print(order.error.exception_code)
    print(order.error.developer_message)
```