from flask_restful import reqparse

# парсер для заказа
order_parser = reqparse.RequestParser()
order_parser.add_argument("customer", type=str, required=True, help="customer is required")

# парсер для товара
item_parser = reqparse.RequestParser()
item_parser.add_argument("name", type=str, required=True, help="item's name is required")
item_parser.add_argument("price", type=float, required=True, help="item's price is required")
