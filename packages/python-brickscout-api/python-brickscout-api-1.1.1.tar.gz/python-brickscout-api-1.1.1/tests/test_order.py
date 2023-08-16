import sys, os
from decimal import Decimal

sys.path.append(os.getcwd() + '/..')

from brickscout.api import BrickScoutAPI


api = BrickScoutAPI(username='brickstarbelgium', password='Planten11$')

orders = api.orders.get_open_orders()

for order in orders.iterator():
    print(f'Order ID: {order.uuid}')
    
    order_shipping_cost = order.selectedOrderHandlingOption.shippingMethodCost.amount
    order_shipping_method = order.selectedOrderHandlingOption.shippingMethodName
    
    order_additional_cost = order.selectedOrderHandlingOption.paymentCost.amount
    order_tax_rate = Decimal(str(order.taxRate))
    
    print(f'Shipping cost with {order_shipping_method}: {order_shipping_cost} | Additional cost: {order_additional_cost} | Tax rate: {order_tax_rate}%')
    
    shipmentAddress = order.shipmentAddress
    shipment_address = f'{shipmentAddress.streetName} {shipmentAddress.houseNumber}, {shipmentAddress.postalCode} {shipmentAddress.locality} ({shipmentAddress.state}), {shipmentAddress.country.isoalpha2}'
    print(f'Shipment address: {shipment_address}')
    
    invoiceAddress = order.invoiceAddress
    invoice_address = f'{invoiceAddress.streetName} {invoiceAddress.houseNumber}, {invoiceAddress.postalCode} {invoiceAddress.locality} ({invoiceAddress.state}), {invoiceAddress.country.isoalpha2}'
    print(f'Invoice address: {invoice_address}')
    print('')
    
    print('Items')
    print('-------')
    basket = order.basket
    total_basket_price = basket.basketItemTotal.amount
    total_basket_price_net = basket.netBasketItemTotal.amount

    print(f'Total basket price: {total_basket_price} {basket.basketItemTotal.currency} | Total basket price net: {total_basket_price_net} {basket.netBasketItemTotal.currency}')
    
    check_basket_price = Decimal('0')
    check_basket_price_net = Decimal('0')
    total_vat_amount = Decimal('0')
    for batch in basket.batches.iterator():
        for item in batch.items.iterator():
            vat_percentage = order_tax_rate
            
            name = item.name
            quantity = item.quantity
            currency = item.lineTotal.currency
            
            total_price = Decimal(str(item.lineTotal.amount))
            net_price = round(total_price / Decimal(str(1 + (vat_percentage / 100))),2)
            vat_amount = total_price - net_price
            
            unit_total_price = round(Decimal(total_price / quantity),2)
            unit_net_price = round(Decimal(net_price / quantity),2)
            
            check_basket_price += total_price
            check_basket_price_net += net_price
            
            print(f'Item: {name} | Quantity: {quantity} | Total price: {total_price} {currency} | Net price: {net_price} {currency} | VAT: {vat_percentage}% | Unit price: {unit_total_price} {currency} | Unit net price: {unit_net_price} {currency}')
    
    print('')
    
    if check_basket_price_net != total_basket_price_net:
        print(f'WARNING: Basket price net does not match! Expected: {total_basket_price_net} | Actual: {check_basket_price_net}')
    
    if check_basket_price != total_basket_price:
        print(f'WARNING: Basket price does not match! Expected: {total_basket_price} | Actual: {check_basket_price}')
    
    print('')
    print('')
    print('')