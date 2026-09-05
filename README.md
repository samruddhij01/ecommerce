# E-Commerce Order Management API

A RESTful backend API for an e-commerce platform, built with **Flask** and **MySQL**. Handles product catalog management, customer records, transactional order processing, and sales analytics powered by SQL window functions.

## Why this project

Most beginner backend projects stop at basic CRUD. This one focuses on the things that actually come up in backend interviews: **transaction integrity** (what happens when an order is placed but stock runs out mid-way?), **schema normalization** (why is price stored per order-item instead of just referencing the product table?), and **analytical SQL** (window functions for ranking and running totals, not just simple aggregates).

## Features

- **Product Catalog** — Full CRUD for products, linked to categories, with live stock tracking.
- **Customer Management** — Create/manage customers, view per-customer order history.
- **Transactional Order Processing** — Placing an order validates stock, deducts inventory, and calculates the total — all wrapped in a single database transaction (commit/rollback), so a failure at any step leaves the database unchanged rather than partially updated.
- **Sales Analytics** — Endpoints built on `RANK()`, `ROW_NUMBER()`, and `SUM() OVER()` to surface top-selling products, monthly revenue with running totals, and top customers by spend.

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | MySQL |
| DB Driver | mysql-connector-python |

## Project Structure