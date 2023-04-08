import re
import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_cliente

router = APIRouter(prefix="/user",
                   tags=["User"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})


@router.post("/",response_model=User, status_code=status.HTTP_201_CREATED)
async def add_user(user: User):

    if not email_format_check(user.email):
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED, detail="Email format not match")

    if (type(search_user("username", user.username)) == User or type(search_user("email", user.email)) == User):
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED, detail="User/Email already exist")

    hashed_password = pass_hasher(user.password)
    user.password = hashed_password

    user_dict = dict(user)
    del user_dict["id"]

    id = db_cliente.users.insert_one(user_dict).inserted_id
    new_user = user_schema(db_cliente.users.find_one({"_id": id}))
    return User(**new_user)


# Function
def search_user(field: str, key):
    try:
        user = user_schema(db_cliente.users.find_one({field: key}))
        return User(**user)
    except:
        return {"error_message": "User not found"}


def pass_hasher(password: str):
    salt = bcrypt.gensalt()
    ecode_pass = password.encode("utf-8")
    hashed_password = bcrypt.hashpw(ecode_pass, salt)
    return hashed_password


def email_format_check(email: str):
    format = r"^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if re.fullmatch(format, email):
        return True
    return False
