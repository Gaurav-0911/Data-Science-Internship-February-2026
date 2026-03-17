from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI()

# -----------------------------
# Product Data
# -----------------------------
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True}
]

orders = []
order_counter = 1


# -----------------------------
# Order Model
# -----------------------------
class Order(BaseModel):
    customer_name: str
    product_name: str
    quantity: int


# -----------------------------
# Get All Products
# -----------------------------
@app.get("/products")
def get_products():
    return {"products": products, "total": len(products)}


# -----------------------------
# Search Products
# -----------------------------
@app.get("/products/search")
def search_products(keyword: str = Query(...)):

    results = [
        p for p in products
        if keyword.lower() in p["name"].lower()
    ]

    if not results:
        return {"message": f"No products found for: {keyword}"}

    return {
        "keyword": keyword,
        "total_found": len(results),
        "products": results
    }


# -----------------------------
# Sort Products
# -----------------------------
@app.get("/products/sort")
def sort_products(
        sort_by: str = Query("price"),
        order: str = Query("asc")
):

    if sort_by not in ["price", "name"]:
        raise HTTPException(status_code=400, detail="sort_by must be 'price' or 'name'")

    reverse = order == "desc"

    sorted_products = sorted(
        products,
        key=lambda p: p[sort_by],
        reverse=reverse
    )

    return {
        "sort_by": sort_by,
        "order": order,
        "products": sorted_products
    }


# -----------------------------
# Pagination
# -----------------------------
@app.get("/products/page")
def paginate_products(
        page: int = Query(1, ge=1),
        limit: int = Query(2, ge=1)
):

    start = (page - 1) * limit
    result = products[start:start + limit]

    return {
        "page": page,
        "limit": limit,
        "total_products": len(products),
        "total_pages": -(-len(products) // limit),
        "products": result
    }


# -----------------------------
# Create Order
# -----------------------------
@app.post("/orders")
def create_order(order: Order):

    global order_counter

    new_order = {
        "order_id": order_counter,
        "customer_name": order.customer_name,
        "product_name": order.product_name,
        "quantity": order.quantity
    }

    orders.append(new_order)
    order_counter += 1

    return {"message": "Order placed", "order": new_order}


# -----------------------------
# Search Orders (Q4)
# -----------------------------
@app.get("/orders/search")
def search_orders(customer_name: str = Query(...)):

    results = [
        o for o in orders
        if customer_name.lower() in o["customer_name"].lower()
    ]

    if not results:
        return {"message": f"No orders found for: {customer_name}"}

    return {
        "customer_name": customer_name,
        "total_found": len(results),
        "orders": results
    }
    
 # -----------------------------
# Paginate Orders (BONUS)
# -----------------------------
@app.get("/orders/page")
def get_orders_paged(
    page: int = Query(1, ge=1),
    limit: int = Query(3, ge=1, le=20)
):
    start = (page - 1) * limit

    return {
        "page": page,
        "limit": limit,
        "total_orders": len(orders),
        "total_pages": (len(orders) + limit - 1) // limit,
        "orders": orders[start:start + limit]
    }   


# -----------------------------
# Sort By Category (Q5)
# -----------------------------
@app.get("/products/sort-by-category")
def sort_by_category():

    result = sorted(
        products,
        key=lambda p: (p["category"], p["price"])
    )

    return {"products": result, "total": len(result)}


# -----------------------------
# Browse Products (Search+Sort+Page) (Q6)
# -----------------------------
@app.get("/products/browse")
def browse_products(
        keyword: str | None = None,
        sort_by: str = "price",
        order: str = "asc",
        page: int = 1,
        limit: int = 4
):

    result = products

    # Search
    if keyword:
        result = [
            p for p in result
            if keyword.lower() in p["name"].lower()
        ]

    # Sort
    if sort_by in ["price", "name"]:
        result = sorted(
            result,
            key=lambda p: p[sort_by],
            reverse=(order == "desc")
        )

    # Pagination
    total = len(result)
    start = (page - 1) * limit
    paged = result[start:start + limit]

    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit,
        "total_found": total,
        "total_pages": -(-total // limit),
        "products": paged
    }


# -----------------------------
# Get Product by ID
# -----------------------------
@app.get("/products/{product_id}")
def get_product(product_id: int):

    for p in products:
        if p["id"] == product_id:
            return p

    raise HTTPException(status_code=404, detail="Product not found")
