from db_setup import db

post_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["title", "content", "user_id"],
        "properties": {
            "title": {
                "bsonType": "string",
                "description": "Title of the post."
            },
            "content": {
                "bsonType": "string",
                "description": "Content of the post."
            },
            "user_id": {
                "bsonType": "objectId",
                "description": "User ID of the author."
            }
        }
    }
}

collection_name = "posts"

if collection_name not in db.list_collection_names():
    # The collection does not exist, so create it
    db.create_collection(collection_name, validator=post_schema)

