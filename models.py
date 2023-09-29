from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# модель заказа
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(50))
    items = relationship("Item", backref="order", cascade="all, delete")
    
# модель товара
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    price = db.Column(db.Float)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id", ondelete="CASCADE"))