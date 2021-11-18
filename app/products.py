from fastapi import Response,status, HTTPException, APIRouter, Depends
from db.database import cursor, conn
from . import schema, oauth2

router = APIRouter(tags=["Posts"])

selectAllProductsSQL = "SELECT * FROM products_product"
createProductSQL = "INSERT INTO products_product (title,image_url,market_price,selling_price," \
                   "description,category_id, date) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING * "
getPostSQL = "SELECT * FROM products_product WHERE id = %s"
deletePostSQL = "DELETE FROM products_product WHERE id = %s RETURNING *"
updatePostSQL = "UPDATE products_product  SET title=%s,date=%s,image_url=%s,market_price=%s," \
                "selling_price=%s,description=%s, category_id=%s WHERE id=%s RETURNING *"


@router.get("/posts")
async def get_products(current_user = Depends(oauth2.get_current_user)):
    print(current_user)
    cursor.execute(selectAllProductsSQL)
    products = cursor.fetchall()
    return {"data": products}


@router.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_product(product: schema.Product):
    cursor.execute(createProductSQL, (product.title, product.image_url,
                                      product.market_price, product.selling_price, product.description,
                                      product.category_id, product.date))
    created_product = cursor.fetchone()
    conn.commit()
    return {"results": created_product, "message": "You created posts"}


@router.get('/posts/{id}')
def get_post(id: str):
    cursor.execute(getPostSQL, (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id : {id} does not exist.")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id : {id} does not exist."}
    return {"post_id": post}


@router.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(deletePostSQL, (str(id),))
    deleted_product = cursor.fetchone()
    conn.commit()
    if deleted_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post ID not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/posts/{id}')
def update_post(id: int, post: schema.Product):
    cursor.execute(updatePostSQL, (post.title, post.date, post.image_url,
                                   post.market_price, post.selling_price, post.description,
                                   post.category_id, str(id),))
    updated_product = cursor.fetchone()
    conn.commit()
    if updated_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post ID not found")
    return {"data": updated_product}


my_posts = [{"id": 1, "title": "george", "content": "Loves Coding"},
            {"id": 2, "title": "gabbs", "content": "Beautiful"}]


def find_posts(id):
    for post in my_posts:
        if post["id"] == id:
            return post


def find_index_post(id):
    for i, post in enumerate(my_posts):
        if post["id"] == id:
            return i


@router.get('/posts/latest')
def get_latest_posts():
    post = my_posts[len(my_posts) - 1]
    return {"post_id": post}
