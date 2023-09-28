import grpc
import os
from concurrent import futures
import post_pb2
import post_pb2_grpc
from bson import ObjectId
from datetime import datetime
from post_schema import db

class PostService(post_pb2_grpc.PostServiceServicer):
    def CreatePost(self, request, context):
        # Your code to create a post in the database
        post_id = "54321"  # Simulated post_id
        # post_data = {
        #     "title": "Sample Post",
        #     "content": "This is the content of the sample post.",
        #     "user_id": ObjectId("6515593c31e306773a93f006"),  # Replace with the actual User ObjectId
        #     "created_at": datetime.utcnow()
        # }
        #
        # db['posts'].insert_one(post_data)

        # # Query all Posts
        # all_posts = db['posts'].find()
        #
        # # Iterate through the Posts
        # for post in all_posts:
        #     print(f"Post Title: {post['title']}")
        #     print(f"Content: {post['content']}")
        #     print(f"User ID: {post['user_id']}")
        #     print(f"Created At: {post['created_at']}\n")

        post_id_to_fetch = ObjectId("651562ed703de79ef6bc1772")

        pipeline = [
            {
                "$match": {"_id": post_id_to_fetch}
            },
            {
                "$lookup": {
                    "from": 'users',
                    "localField": "user_id",
                    "foreignField": "_id",
                    "as": "user"
                }
            },
            {
                "$unwind": "$user"  # Unwind the "user" array created by the $lookup stage
            }
        ]

        result = list(db['posts'].aggregate(pipeline))

        if result:
            post = result[0]
            print(f"Post Title: {post['title']}")
            print(f"Content: {post['content']}")
            print(f"Created At: {post['created_at']}")
            print("User Details:")
            print(f"Username: {post['user']['username']}")
            print(f"Email: {post['user']['email']}")
        else:
            print("Post not found.")

        return post_pb2.PostResponse(
            post_id=post_id,
            user_id=request.user_id,
            content=request.content
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    post_pb2_grpc.add_PostServiceServicer_to_server(PostService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print('Post Service Started at PORT 50052')
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
