from fastapi import status, HTTPException, APIRouter
from db.database import cursor
from .schema import User
from . import utils, oauth2

router = APIRouter()

checkEmailSQL  = """SELECT * FROM users WHERE email = %s"""


@router.post('/login')
async def login_user(user: User):
    cursor.execute(checkEmailSQL, (str(user.email),))
    db_user = cursor.fetchone()
    compare_password = utils.verify(user.password, db_user['password'])
    if not db_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    if not compare_password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    # create token
    access_token = oauth2.create_access_token({"user_id": db_user['id']})
    return {"token": access_token}