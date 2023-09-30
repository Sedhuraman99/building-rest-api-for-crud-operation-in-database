from flask import Flask, request, jsonify
import pymysql
from pymysql.cursors import DictCursor


app = Flask(__name__)

# products_list = [
#     {
#         "name": "product 1",
#         "barcode": "34567890",
#         "brand": "Brand 1",
#         "description": "This is sample",
#         "price": 200,
#         "available": "TRUE",
#         "id": 1
#     },
#     {
#         "name": "product 2",
#         "barcode": "4567890",
#         "brand": "Brand 2",
#         "description": "This is sample",
#         "price": 100,
#         "available": "FALSE",
#         "id": 2
#     },
#     {
#         "name": "product 3",
#         "barcode": "987654",
#         "brand": "Brand 3",
#         "description": "This is sample",
#         "price": 150,
#         "available": "TRUE",
#         "id": 3
#     },
#     {
#         "name": "product 4",
#         "barcode": "12345678",
#         "brand": "Brand 4",
#         "description": "This is sample",
#         "price": 250,
#         "available": "FALSE",
#         "id": 4
#     },
#     {
#         "name": "product 5",
#         "barcode": "23456765",
#         "brand": "Brand 5",
#         "description": "This is sample",
#         "price": 300,
#         "available": "TRUE",
#         "id": 5
#     },
#     {
#         "name": "product 6",
#         "barcode": "23423452",
#         "brand": "Brand 6",
#         "description": "This is sample",
#         "price": 350,
#         "available": "TRUE",
#         "id": 6
#     },
#     {
#         "name": "product 7",
#         "barcode": "987123",
#         "brand": "Brand 7",
#         "description": "This is sample",
#         "price": 180,
#         "available": "TRUE",
#         "id": 7
#     },
#     {
#         "name": "product 8",
#         "barcode": "1256789",
#         "brand": "Brand 8",
#         "description": "This is sample",
#         "price": 120,
#         "available": "FALSE",
#         "id": 8
#     },
#     {
#         "name": "product 9",
#         "barcode": "34562718",
#         "brand": "Brand 9",
#         "description": "This is sample",
#         "price": 110,
#         "available": "TRUE",
#         "id": 9
#     },
#     {
#         "name": "product 10",
#         "barcode": "3.46E+08",
#         "brand": "Brand 10",
#         "description": "This is sample",
#         "price": 90,
#         "available": "FALSE",
#         "id": 10
#     },
#     {
#         "name": "product 11",
#         "barcode": "667788",
#         "brand": "Brand 10",
#         "description": "This is sample",
#         "price": 90,
#         "available": "FALSE",
#         "id": 11
#     },
#     {
#         "name": "product 12",
#         "barcode": "887799",
#         "brand": "Brand 10",
#         "description": "This is sample",
#         "price": 90,
#         "available": "FALSE",
#         "id": 12
#     },
#     {
#         "name": "product 13",
#         "barcode": "24342",
#         "brand": "Brand 10",
#         "description": "This is sample",
#         "price": 90,
#         "available": "FALSE",
#         "id": 13
#     },
#     {
#         "name": "product 14",
#         "barcode": "111",
#         "brand": "Brand 10",
#         "description": "This is sample",
#         "price": 90,
#         "available": "FALSE",
#         "id": 14
#     },
#     {
#         "name": "product 15",
#         "barcode": "1015",
#         "brand": "Brand 10",
#         "description": "This is sample",
#         "price": 90,
#         "available": "FALSE",
#         "id": 15
#     }
# ]


def db_connection():
    conn = None
    try:
        conn = pymysql.connect(host="sql12.freesqldatabase.com",
                                database="sql12649901",
                                user="sql12649901",
                                password="6Nxz6zhI4K",
                                port=3306,
                                charset="utf8mb4",
                                cursorclass=pymysql.cursors.DictCursor
                                )
    except pymysql.Error as e:
        print(e)
    return conn


@app.route("/products", methods=["GET", "POST"])
def products():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor.execute("SELECT * FROM Products")
        products = [
            dict(id=row["id"], name=row["name"], barcode=row["barcode"], brand=row["brand"],
                 description=row["description"], price=row["price"], available=row["available"])
            for row in cursor.fetchall()
        ]
        if products is not None:
            return jsonify(products)

    if request.method == "POST":
        new_name = request.form["name"]
        new_barcode = request.form["barcode"]
        new_brand = request.form["brand"]
        new_description = request.form["description"]
        new_price = request.form["price"]
        new_available = request.form["available"]
        sql = """INSERT INTO Products (name, barcode, brand, description, price, available)
                 VALUES (%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql, (new_name, new_barcode, new_brand, new_description, new_price, new_available))
        conn.commit()
        return f"Product created succesfully"


@app.route("/products/<int:id>", methods=["GET", "PUT", "DELETE"])
def single_product(id):
    conn = db_connection()
    cursor = conn.cursor()
    product = None
    if request.method == "GET":
        cursor.execute("SELECT * FROM Products WHERE id=?", (id,))
        rows = cursor.fetchall()
        for r in rows:
            product = r
        if product is not None:
            return jsonify(product), 200
        else:
            return "Something wrong", 404
    if request.method == "PUT":
        sql = """UPDATE Products
                SET name=?,
                    barcode=?,
                    brand=?,
                    description=?,
                    price=?,
                    available=?
                WHERE id=? """

        name = request.form["name"]
        barcode = request.form["barcode"]
        brand = request.form["brand"]
        description = request.form["description"]
        price = request.form["price"]
        available = request.form["available"]
        updated_product = {
            "id": id,
            "name": name,
            "barcode": barcode,
            "brand": brand,
            "description": description,
            "price": price,
            "available": available
        }
        cursor.execute(sql, (name, barcode, brand, description, price, available, id))
        conn.commit()
        return jsonify(updated_product)

    if request.method == "DELETE":
        sql = """ DELETE FROM Products WHERE id=? """
        cursor.execute(sql, (id,))
        conn.commit()
        return "The product has deleted.", 200


if __name__ == "__main__":
    app.run()
