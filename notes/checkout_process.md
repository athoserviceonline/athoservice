# Checkout Process

1. Cart -> Checkout View
   ?
   - Login/Register or Enter an Email (as Guest)
   - Shipping Address
   - Billing Address
   - Credit Card / Payment

2. Billing App/Component
	- Billing Profile
		- User or Email (Guest Email)
		- generate payment processor token (Stripe or Braintree)

3. Orders/ Invoices Component
	- Connecting the Billing Profile
	- Shipping / Billing Address
	- Cart
	- Status -- Shipping? Cancelled?

4. Backup Fixtures
	python manage.py dumpdata products --format json --indent 4 > shopping/fixtures/products.json

