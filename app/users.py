from fastapi import status, APIRouter, Depends
from db.database import cursor, conn
from . import utils, oauth2
from .schema import User

router = APIRouter(tags=["Users"])

createUserSQL = "INSERT INTO users (email,password) VALUES (%s,%s) RETURNING  id, email"


@router.post('/users', status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    # hash the user password
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    cursor.execute(createUserSQL, (user.email, user.password))
    created_user = cursor.fetchone()
    conn.commit()
    return {"results": created_user, "message": "You created user"}
