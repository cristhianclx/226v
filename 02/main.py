from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "<p>Hello, World!</p>"

@app.route("/users")
def users():
    return "<p>USERS example</p>"

@app.route("/items")
def items():
    return [{
        "id": "ABCD",
        "content": "abcdef"
    }, {
        "id": "EFGH",
        "content": "efghij"
    }]

@app.route("/items/<id>")
def items_by_id(id):
    print(id)
    return {
        "id": "ABCD",
        "content": "abcdef"
    }

products_items = [{
    "id": 1,
    "name": "Apple"
}, {
    "id": 2,
    "name": "Orange"
}, {
    "id": 3,
    "name": "Pineapple"
}]

@app.route("/products/<int:id>", methods=["GET", "POST"])
def products(id):
    if request.method == "GET":
        return "GET data"
    if request.method == "POST":
        raw = request.get_json()
        id_to_modify = raw["id"]
        for product in products_items:
            if product["id"] == id_to_modify:
                return product
        return "POST data"