from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI()

# Product Model
class Product(BaseModel):
    name: str
    price: int
    category: str
    in_stock: bool

# Initial Data
products = [
    {"id": 1, "name": "Keyboard", "price": 799, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 599, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 199, "category": "Stationery", "in_stock": True},
]

next_id = 5


# GET ALL PRODUCTS
@app.get("/products")
def get_products():
    return {
        "total": len(products),
        "items": products
    }


# ADD PRODUCT
@app.post("/products", status_code=201)
def add_product(product: Product):
    global next_id

    for p in products:
        if p["name"].lower() == product.name.lower():
            raise HTTPException(status_code=400, detail="Product already exists")

    new_product = {
        "id": next_id,
        **product.dict()
    }

    products.append(new_product)
    next_id += 1

    return new_product


# UPDATE PRODUCT
@app.put("/products/{product_id}")
def update_product(
    product_id: int,
    price: int = Query(None),
    in_stock: bool = Query(None)
):

    for product in products:
        if product["id"] == product_id:

            if price is not None:
                product["price"] = price

            if in_stock is not None:
                product["in_stock"] = in_stock

            return {"message": "Product updated", "product": product}

    raise HTTPException(status_code=404, detail="Product not found")


# DELETE PRODUCT
@app.delete("/products/{product_id}")
def delete_product(product_id: int):

    for product in products:
        if product["id"] == product_id:
            products.remove(product)
            return {"message": f'{product["name"]} deleted'}

    raise HTTPException(status_code=404, detail="Product not found")


# AUDIT REPORT
@app.get("/products/audit")
def audit_products():

    total_products = len(products)

    in_stock_count = sum(1 for p in products if p["in_stock"])

    total_stock_value = sum(p["price"] for p in products if p["in_stock"])

    most_expensive = max(products, key=lambda x: x["price"])

    return {
        "total_products": total_products,
        "in_stock_products": in_stock_count,
        "stock_value": total_stock_value,
        "most_expensive_product": most_expensive
    }
