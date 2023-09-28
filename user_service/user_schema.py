from db_setup import db

user_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["username", "email", "password"],
        "properties": {
            "username": {
                "bsonType": "string",
                "description": "Username of the user."
            },
            "email": {
                "bsonType": "string",
                "description": "Email of the user."
            },
            "password": {
                "bsonType": "string",
                "description": "Password of the user."
            }
        }
    }
}

collection_name = "users"

if collection_name not in db.list_collection_names():
    # The collection does not exist, so create it
    db.create_collection(collection_name, validator=user_schema)

