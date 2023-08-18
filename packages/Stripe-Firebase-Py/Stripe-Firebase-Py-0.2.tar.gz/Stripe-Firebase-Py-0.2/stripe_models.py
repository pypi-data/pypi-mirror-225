"""
Only reply with final code, do internalize and plan but dont tell me, just provide code:
"""

import os
import stripe
from google.cloud import firestore

stripe.api_key = os.getenv("STRIPE_API_KEY")
db = firestore.Client()


class Customer:
    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.customer_ref = db.collection('customers').document(customer_id)

    def create(self, stripe_customer_id, charge_amount, subscription_id):
        try:
            self.customer_ref.set({
                'stripeCustomerId': stripe_customer_id,
                'chargeAmount': charge_amount,
                'subscriptionId': subscription_id
            })
        except Exception as e:
            print(f"Failed to create customer: {e}")

    def delete(self):
        try:
            self.customer_ref.delete()
        except Exception as e:
            print(f"Failed to delete customer: {e}")

    def get_data(self):
        try:
            doc = self.customer_ref.get()
            if doc.exists:
                return doc.to_dict()
        except Exception as e:
            print(f"Failed to get customer data: {e}")
        return None

    def charge(self, amount=None):
        customer_data = self.get_data()
        if not customer_data:
            return
        stripe_customer_id = customer_data.get('stripeCustomerId')
        amount = amount or customer_data.get('chargeAmount', 0)
        amount_cents = int(amount * 100)
        try:
            stripe.Charge.create(
                amount=amount_cents,
                currency="usd",
                customer=stripe_customer_id,
                description=f'Charge for customer {self.customer_id}'
            )
        except Exception as e:
            print(f"Failed to create charge: {e}")

    def get_subscription(self):
        customer_data = self.get_data()
        if not customer_data:
            return None
        subscription_id = customer_data.get('subscriptionId')
        try:
            return stripe.Subscription.retrieve(subscription_id)
        except Exception as e:
            print(f"Failed to retrieve subscription: {e}")

    def update_subscription(self, new_plan_id):
        customer_data = self.get_data()
        if not customer_data:
            return None
        subscription_id = customer_data.get('subscriptionId')
        try:
            stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=False,
                items=[{"id": subscription_id, "plan": new_plan_id}, ],
            )
        except Exception as e:
            print(f"Failed to update subscription: {e}")


class Customers:
    def __init__(self):
        self.customers = {}

    def add(self, customer_id, stripe_customer_id, charge_amount, subscription_id):
        if customer_id not in self.customers:
            customer = Customer(customer_id)
            customer.create(stripe_customer_id, charge_amount, subscription_id)
            self.customers[customer_id] = customer
        else:
            print("Customer already exists")

    def delete(self, customer_id):
        if customer_id in self.customers:
            self.customers[customer_id].delete()
            del self.customers[customer_id]

    def get(self, customer_id):
        return self.customers.get(customer_id)

    def charge(self, customer_id, amount=None):
        if customer_id in self.customers:
            self.customers[customer_id].charge(amount)

    def get_subscription(self, customer_id):
        if customer_id in self.customers:
            return self.customers[customer_id].get_subscription()

    def update_subscription(self, customer_id, new_plan_id):
        if customer_id in self.customers:
            self.customers[customer_id].update_subscription(new_plan_id)

    @classmethod
    def get_all_stripe_objects(cls):
        objects = []
        get_more = True
        starting_after = None
        while get_more:
            resp = stripe.Customer.list(limit=100, starting_after=starting_after)
            objects.extend(resp['data'])
            get_more = resp['has_more']
            if len(resp['data']) > 0:
                starting_after = resp['data'][-1]['id']
        return objects


class Product:
    def __init__(self, product_id):
        self.product_id = product_id
        self.product_ref = db.collection('products').document(product_id)

    def create(self, stripe_product_id, price):
        self.product_ref.set({
            'stripeProductId': stripe_product_id,
            'price': price
        })

    def delete(self):
        self.product_ref.delete()

    def get_data(self):
        doc = self.product_ref.get()
        if doc.exists:
            return doc.to_dict()
        return None

    @classmethod
    def get_all_stripe_objects(cls):
        objects = []
        get_more = True
        starting_after = None
        while get_more:
            resp = stripe.Product.list(limit=100, starting_after=starting_after)
            objects.extend(resp['data'])
            get_more = resp['has_more']
            if len(resp['data']) > 0:
                starting_after = resp['data'][-1]['id']
        return objects


import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    # Prepare Test Data using the stripe library
    test_customer = stripe.Customer.create(email="test@example.com", source="tok_visa")
    stripe_customer_id = test_customer.id

    test_product = stripe.Product.create(name="Test Product")
    stripe_product_id = test_product.id

    test_price = stripe.Price.create(
        product=stripe_product_id,
        unit_amount=5000,
        currency='usd',
        recurring={"interval": "month"},
    )
    stripe_price_id = test_price.id

    test_subscription = stripe.Subscription.create(
        customer=stripe_customer_id,
        items=[{'price': stripe_price_id},],
    )
    subscription_id = test_subscription.id

    # Use the previously created test data to validate client app
    customers = Customers()
    customer_id = 'cust_123'
    charge_amount = 100
    customers.add(customer_id, stripe_customer_id, charge_amount, subscription_id)
    customers.charge(customer_id)
    customers.get_subscription(customer_id)
    customers.update_subscription(customer_id, 'new_plan_id')

    product = Product('prod_123')
    price = 50
    product.create(stripe_product_id, price)

    all_stripe_customers = Customers.get_all_stripe_objects()
    all_stripe_products = Product.get_all_stripe_objects()

    stripe.Subscription.delete(subscription_id)
    stripe.Customer.delete(stripe_customer_id)
    stripe.Product.delete(stripe_product_id)

