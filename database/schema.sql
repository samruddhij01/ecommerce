-- 1. Create the database (skips if it already exists)
CREATE DATABASE IF NOT EXISTS ecommerce_db;

-- 2. Switch into it so the tables below get created inside it
USE ecommerce_db;

-- 3. Customers table
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Categories table
CREATE TABLE IF NOT EXISTS categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- 5. Products table (depends on categories)
CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

-- 6. Orders table (depends on customers)
CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    status ENUM('pending','shipped','delivered','cancelled') DEFAULT 'pending',
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10,2) DEFAULT 0,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- 7. Order items table (depends on orders + products)
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price_at_purchase DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- ============================================
-- Optional: sample seed data to test with
-- ============================================

INSERT INTO categories (name) VALUES ('Electronics'), ('Books'), ('Clothing');

INSERT INTO products (name, price, stock, category_id) VALUES
('Wireless Mouse', 599.00, 50, 1),
('Mechanical Keyboard', 2499.00, 30, 1),
('The Pragmatic Programmer', 899.00, 20, 2),
('Cotton T-Shirt', 399.00, 100, 3);

INSERT INTO customers (name, email) VALUES
('Asha Verma', 'asha@example.com'),
('Rohit Sharma', 'rohit@example.com');