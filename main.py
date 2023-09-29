from flask_restful import Api, Resource, marshal_with, abort
from flask import Flask
from models import db, Item, Order
from parsers import item_parser, order_parser
from fields import item_fields, order_fields

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.app = app
db.init_app(app)

api = Api(app)

#db.drop_all()
#db.create_all()

class OrderRes(Resource):
    """Класс заказа"""
    @marshal_with(order_fields)
    def post(self):
        """Создание заказа"""
        data = order_parser.parse_args()
        new_order = Order(customer=data["customer"])
        db.session.add(new_order)
        db.session.commit()
        return new_order, 201

    @marshal_with(item_fields) # item_fields потому что выводим товары
    def get(self, order_id):
        """Получение товаров, входящий в заказ по order_id"""
        order=Order.query.filter_by(id=order_id).first()
        if(order is None):
            abort(404, message="order with this ID doesn't exist!")
        return order.items
    
    @marshal_with(order_fields)
    def put(self, order_id):
        """Изменение заказа по order_id"""
        order_to_edit = Order.query.filter_by(id=order_id).first()
        if(order_to_edit is None):
            abort(404, message="order with this ID doesn't exist!")
        data = order_parser.parse_args()
        order_to_edit.customer = data["customer"]
        db.session.commit()
        return order_to_edit
    
    def delete(self, order_id):
        """Удаление заказа по order_id"""
        order_to_delete = Order.query.filter_by(id=order_id).first()
        if(order_to_delete is None):
            abort(404, message="order with this ID doesn't exist!")
        db.session.delete(order_to_delete)
        db.session.commit()
        return {"info": "order successfully deleted!"}
    

class ItemRes(Resource):
    """Класс товара"""
    @marshal_with(item_fields)
    def post(self, order_id):
        """Создание товара, привязанного к заказу"""
        if(Order.query.filter_by(id=order_id).first() is None):
            abort(404, message="order with this ID doesn't exist!")
        data = item_parser.parse_args()
        if(Item.query.filter_by(name=data["name"]).first() is not None):
            abort(400, message="item with this name already exists!")
        new_item = Item(name=data["name"], price=data["price"], order_id=order_id)
        db.session.add(new_item)
        db.session.commit()
        return new_item, 201
    
    @marshal_with(item_fields)
    def get(self, order_id, item_id):
        """Получение информации о товаре по item_id, входящим в заказ по order_id"""
        if(Order.query.filter_by(id=order_id).first() is None):
            abort(404, message="order with this ID doesn't exist!")
        item = Item.query.filter_by(id=item_id).first()
        if(item  is None):
            abort(400, message="item with this ID doesn't exist!")
        return item

    @marshal_with(item_fields)
    def put(self, order_id, item_id):
        """Изменение конкретного товара, привязанного к заказу"""
        if(Order.query.filter_by(id=order_id).first() is None):
            abort(404, message="order with this ID doesn't exist!")
        item_to_edit = Item.query.filter_by(id=item_id).first()
        if(item_to_edit is None):
            abort(404, message="item with this ID doesn't exist!")
        data = item_parser.parse_args()
        item_to_edit.name = data["name"]
        item_to_edit.price = data["price"]
        db.session.commit()
        return item_to_edit
    
    def delete(self, order_id, item_id):
        """Удаление конкретного товара, привязанного к заказу"""
        if(Order.query.filter_by(id=order_id).first() is None):
            abort(404, message="order with this ID doesn't exist!")
        item_to_del = Item.query.filter_by(id=item_id).first()
        if(item_to_del is None):
            abort(404, message="item with this ID doesn't exist!")
        db.session.delete(item_to_del)
        db.session.commit()
        return {"info": "item successfully deleted!"}


api.add_resource(
    OrderRes, 
    "/orders/add_order",        # url для POST-метода (добавление заказа)
    "/orders/<int:order_id>"    # url для GET-, PUT-, DELETE-методов
)
api.add_resource(
    ItemRes, 
    "/orders/<int:order_id>/add_item",      # url для POST-метода (добавление товара)
    "/orders/<int:order_id>/<int:item_id>"  # url для GET-, PUT-, DELETE-методов
)

if __name__ == "__main__":
    app.run(debug=True)