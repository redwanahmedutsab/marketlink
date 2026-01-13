🛠️ MarketLink – Django Backend (Interview Task)

MarketLink is a small multi-vendor marketplace backend that connects vehicle owners with local repair shops.
This project implements a core subset of the MarketLink backend using Django and Django REST Framework, focusing on order booking, concurrency-safe stock handling, and webhook-based payment confirmation.

This repository was developed as part of a Django Developer Interview Task for Softvence IT Ltd.

⸻

📌 Features Implemented
	•	Custom user authentication with JWT
	•	Role-based users: Customer, Vendor, Admin
	•	Vendor profiles with service offerings
	•	Variant-based services with pricing and stock
	•	Concurrency-safe order creation
	•	Mocked payment redirect flow
	•	Secure & idempotent payment webhook
	•	Admin-friendly Django admin configuration

⸻

🧱 Tech Stack
	•	Python
	•	Django
	•	Django REST Framework
	•	SimpleJWT (JWT Authentication)
	•	SQLite (development database)
	•	HMAC SHA-256 for webhook security

⸻

🔐 Authentication

Why JWT?

JWT (JSON Web Token) authentication is used via djangorestframework-simplejwt because:
	•	Stateless & scalable
	•	Suitable for REST APIs
	•	Easy integration with frontend or mobile clients

Endpoints

POST /api/token/
POST /api/token/refresh/

Authentication is required for order creation.

⸻

👤 User Model & Roles

A custom User model is implemented using AbstractBaseUser and PermissionsMixin.

Roles
	•	customer – Can place repair orders
	•	vendor – Owns a vendor profile and services
	•	admin – Full system access

Email is used as the unique identifier.

⸻

🏪 Vendor & Services

Vendor Profile

Each vendor has a one-to-one relationship with a user account.

Fields:
	•	Business name
	•	Address
	•	Active status

Services & Variants

Vendors offer services, each having multiple variants:

Example:
	•	Oil Change
	•	Basic
	•	Premium
	•	Express

Each ServiceVariant contains:
	•	Price
	•	Estimated time
	•	Stock (number of concurrent bookings allowed)

Services and variants are managed via Django Admin.

⸻

📦 Repair Orders

RepairOrder Model

Each order represents a booking for a specific service variant.

Key fields:
	•	order_id (UUID)
	•	Customer
	•	Vendor
	•	Service Variant
	•	Status (pending, paid, processing, completed, failed, cancelled)
	•	Total amount
	•	Created timestamp

Orders are initially created with status pending.

⸻

🔒 Concurrency & Stock Handling

Problem

If two customers attempt to book the same service variant with stock = 1, double booking must not occur.

Solution (Implemented)

Database-level row locking using:

transaction.atomic()
ServiceVariant.objects.select_for_update()

Why This Works
	•	Locks the service variant row during order creation
	•	Ensures stock is checked and decremented atomically
	•	Prevents race conditions even under concurrent requests

This approach is production-grade and does not rely on application-level locks.

⸻

🔁 Order & Payment Flow
	1.	Customer creates an order
	2.	Stock is locked and decremented atomically
	3.	Order is created with status pending
	4.	API returns a mock payment URL
	5.	Payment provider sends webhook
	6.	Order is validated and marked as paid

Order Creation Endpoint

POST /api/orders/

Response:

{
  "order_id": "UUID",
  "payment_url": "https://fake-payment.com/pay/{order_id}"
}


⸻

💳 Payments & Webhooks

Webhook Endpoint

POST /webhooks/payment/

Webhook Security
	•	Uses HMAC SHA-256
	•	Signature validated using WEBHOOK_SECRET from environment variables
	•	Invalid signatures are rejected

Idempotency

A PaymentEvent model stores processed webhook event_ids.

If the same event arrives more than once:
	•	It is ignored safely
	•	Order state is not changed again

Payment Validation

Before marking an order as paid:
	•	Order must exist
	•	Payment amount must exactly match total_amount

Only then is the order status updated to paid.

⸻

🛠 Admin Panel
	•	Manage users and roles
	•	Create vendors and services
	•	Inline service variant management
	•	View and filter repair orders
	•	Inspect payment webhook events

⸻

⚙️ Environment Variables

Create a .env file using the following example:

SECRET_KEY=your_django_secret_key
DEBUG=True
WEBHOOK_SECRET=your_webhook_secret

Note: Secrets are never hardcoded.

⸻

🚀 Setup Instructions

1️⃣ Clone Repository

git clone <repository-url>
cd marketlink

2️⃣ Create Virtual Environment

python -m venv venv
source venv/bin/activate

3️⃣ Install Dependencies

pip install django djangorestframework djangorestframework-simplejwt

4️⃣ Apply Migrations

python manage.py migrate

5️⃣ Create Superuser

python manage.py createsuperuser

6️⃣ Run Server

python manage.py runserver


⸻

📌 Assumptions & Limitations
	•	Payment gateway is mocked; no real Stripe/SSLCommerz integration
	•	SQLite is used for development only
	•	Background jobs (email/invoice) are not implemented
	•	Services & variants are managed via admin (no public CRUD APIs)

⸻

✅ Evaluation Criteria Mapping

Requirement	Status
Custom User Model	✅
JWT Authentication	✅
Variant-based Services	✅
Concurrency Safe Booking	✅
Webhook Security	✅
Idempotent Webhooks	✅
Clean Code & Structure	✅
Documentation	✅


⸻

📬 Final Notes

This project prioritizes correctness, clarity, and real-world backend practices.
All critical business logic (concurrency, payments, security) is explicitly handled and documented.