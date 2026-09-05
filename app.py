from flask import Flask
from routes.products import products_bp
from routes.customers import customers_bp
from routes.orders import orders_bp
from routes.analytics import analytics_bp
app=Flask(__name__)
app.register_blueprint(products_bp)
app.register_blueprint(customers_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(analytics_bp)
@app.route('/')
def home():
    return "API is running"
if __name__=="__main__":
    app.run(debug=True,port=1234)