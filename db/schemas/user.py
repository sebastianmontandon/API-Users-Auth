def user_schema(user) -> dict:
    return {"id": str(user["_id"]),
            "username": user["username"],
            "fullname": user["fullname"],
            "availability": user["availability"],
            "password": user["password"],
            "email": user["email"],
            "domain": user["domain"]
            }

def users_schema(users) -> list:
    return [user_schema(user) for user in users]