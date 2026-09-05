# Stockroom — frontend for the ecommerce API

A small Flask frontend that gives you a browser UI for the ecommerce API
(products, customers, orders, analytics). It's a separate Flask app that
talks to your existing API over HTTP — it doesn't touch your database
directly.

## Setup

```bash
cd frontend
pip install -r requirements.txt
python app.py
```

This starts the frontend on **http://127.0.0.1:5000**. Your ecommerce API
(the other project) needs to be running separately on **port 1234**
(`python app.py` in that project's folder) — the frontend just forwards
requests to it.

If your API runs somewhere else, set the `API_BASE` environment variable:

```bash
API_BASE=http://127.0.0.1:1234 python app.py
```

## What you can do

- **Products** — list, create, delete, and edit stock.
- **Customers** — list, create, edit, delete, and view a customer's order
  history.
- **Orders** — place a new order for a customer with any number of line
  items.
- **Analytics** — top products by units sold, top customers by spend, and
  a monthly revenue chart.

## Known limitations (from the current API)

These aren't bugs in the frontend — the underlying API doesn't expose the
routes yet:

- **No "list all orders" page.** The API only has `POST /orders`. To see
  orders, open a customer's page and view their order history
  (`GET /customers/<id>/orders`).
- **Product edits are stock-only.** The API's `PUT /products/<id>/stock`
  route only updates stock — name, price, and category can't be changed
  once a product is created.
- **Order item shape is assumed.** `POST /orders` is called with
  `{"customer_id": ..., "items": [{"product_id": ..., "quantity": ...}]}`.
  If your `create_order()` model function expects a different shape,
  update the `orders_new` view in `app.py` to match.

To close these gaps, add routes like `GET /orders`, `GET /orders/<id>`, and
a full `PUT /products/<id>` to the API — the frontend can be pointed at
them once they exist.
