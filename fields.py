from flask_restful import fields

# поля заказа для сериализации (marshal_with)
order_fields = {
    "id": fields.Integer,
    "customer": fields.String
}

# поля товара для сериализации (marshal_with)
item_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "price": fields.Float,
    "order_id": fields.Integer
}