import os
import requests
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")

# Base URL of the ecommerce API (app.py from the other project, port 1234)
API_BASE = os.environ.get("API_BASE", "http://127.0.0.1:1234")


def api_get(path):
    resp = requests.get(f"{API_BASE}{path}")
    resp.raise_for_status()
    return resp.json()


def api_write(method, path, payload=None):
    """POST/PUT/DELETE against the API. Returns (ok, data)."""
    resp = requests.request(method, f"{API_BASE}{path}", json=payload)
    try:
        data = resp.json()
    except ValueError:
        data = {}
    return resp.ok, data


# ---------- Products ----------

@app.route("/")
def index():
    return redirect(url_for("products_list"))


@app.route("/products")
def products_list():
    try:
        products = api_get("/products")
    except requests.RequestException:
        flash("Could not reach the API. Is app.py running on port 1234?", "error")
        products = []
    return render_template("products_list.html", products=products, active="products")


@app.route("/products/new", methods=["GET", "POST"])
def product_new():
    if request.method == "POST":
        payload = {
            "name": request.form["name"],
            "price": float(request.form["price"]),
            "stock": int(request.form["stock"]),
            "category_id": int(request.form["category_id"]),
        }
        ok, data = api_write("POST", "/products", payload)
        if ok:
            flash("Product created.", "success")
            return redirect(url_for("products_list"))
        flash(data.get("error", "Could not create product."), "error")
    return render_template("product_new.html", active="products")


@app.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
def product_edit(product_id):
    if request.method == "POST":
        payload = {"stock": int(request.form["stock"])}
        ok, data = api_write("PUT", f"/products/{product_id}/stock", payload)
        if ok:
            flash("Stock updated.", "success")
            return redirect(url_for("products_list"))
        flash(data.get("error", "Could not update stock."), "error")

    product = api_get(f"/products/{product_id}")
    return render_template("product_edit.html", product=product, active="products")


@app.route("/products/<int:product_id>/delete", methods=["POST"])
def product_delete(product_id):
    ok, data = api_write("DELETE", f"/products/{product_id}")
    flash("Product deleted." if ok else data.get("error", "Could not delete product."),
          "success" if ok else "error")
    return redirect(url_for("products_list"))


# ---------- Customers ----------

@app.route("/customers")
def customers_list():
    try:
        customers = api_get("/customers")
    except requests.RequestException:
        flash("Could not reach the API. Is app.py running on port 1234?", "error")
        customers = []
    return render_template("customers_list.html", customers=customers, active="customers")


@app.route("/customers/new", methods=["GET", "POST"])
def customer_new():
    if request.method == "POST":
        payload = {"name": request.form["name"], "email": request.form["email"]}
        ok, data = api_write("POST", "/customers", payload)
        if ok:
            flash("Customer created.", "success")
            return redirect(url_for("customers_list"))
        flash(data.get("error", "Could not create customer."), "error")
    return render_template("customer_new.html", active="customers")


@app.route("/customers/<int:customer_id>/edit", methods=["GET", "POST"])
def customer_edit(customer_id):
    if request.method == "POST":
        payload = {"name": request.form["name"], "email": request.form["email"]}
        ok, data = api_write("PUT", f"/customers/{customer_id}", payload)
        if ok:
            flash("Customer updated.", "success")
            return redirect(url_for("customers_list"))
        flash(data.get("error", "Could not update customer."), "error")

    customer = api_get(f"/customers/{customer_id}")
    return render_template("customer_edit.html", customer=customer, active="customers")


@app.route("/customers/<int:customer_id>/delete", methods=["POST"])
def customer_delete(customer_id):
    ok, data = api_write("DELETE", f"/customers/{customer_id}")
    flash("Customer deleted." if ok else data.get("error", "Could not delete customer."),
          "success" if ok else "error")
    return redirect(url_for("customers_list"))


@app.route("/customers/<int:customer_id>/orders")
def customer_orders(customer_id):
    customer = api_get(f"/customers/{customer_id}")
    orders = api_get(f"/customers/{customer_id}/orders")
    return render_template("customer_orders.html", customer=customer, orders=orders, active="customers")


# ---------- Orders ----------

@app.route("/orders/new", methods=["GET", "POST"])
def orders_new():
    if request.method == "POST":
        product_ids = request.form.getlist("product_id[]")
        quantities = request.form.getlist("quantity[]")
        items = [
            {"product_id": int(pid), "quantity": int(qty)}
            for pid, qty in zip(product_ids, quantities) if pid
        ]
        payload = {"customer_id": int(request.form["customer_id"]), "items": items}
        ok, data = api_write("POST", "/orders", payload)
        if ok:
            flash("Order placed.", "success")
            return redirect(url_for("customer_orders", customer_id=request.form["customer_id"]))
        flash(data.get("error", "Could not place order."), "error")

    try:
        customers = api_get("/customers")
        products = api_get("/products")
    except requests.RequestException:
        flash("Could not reach the API. Is app.py running on port 1234?", "error")
        customers, products = [], []

    selected_customer_id = request.args.get("customer_id")
    return render_template(
        "orders_new.html",
        customers=customers,
        products=products,
        selected_customer_id=selected_customer_id,
        active="orders",
    )


# ---------- Analytics ----------

@app.route("/analytics")
def analytics_index():
    try:
        top_products = api_get("/analytics/top-products")
        top_customers = api_get("/analytics/top-customers")
        monthly_revenue = api_get("/analytics/monthly-revenue")
    except requests.RequestException:
        flash("Could not reach the API. Is app.py running on port 1234?", "error")
        top_products, top_customers, monthly_revenue = [], [], []

    max_monthly = max([float(m["monthly_total"]) for m in monthly_revenue], default=1) or 1

    return render_template(
        "analytics.html",
        top_products=top_products,
        top_customers=top_customers,
        monthly_revenue=monthly_revenue,
        max_monthly=max_monthly,
        active="analytics",
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
