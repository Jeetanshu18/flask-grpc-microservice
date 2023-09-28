import grpc
from concurrent import futures
import user_pb2
import user_pb2_grpc
from user_schema import db

class UserService(user_pb2_grpc.UserServiceServicer):
    def CreateUser(self, request, context):
        # Your code to create a user in the database
        # user_collection = get_user_collection()
        user_data = {
            'username': request.username,
            'email': request.email,
            'password': request.password
        }
        result = db['users'].insert_one(user_data)
        # result = user_collection.insert_one(user_data)
        user_id = str(result.inserted_id)

        return user_pb2.UserResponse(user_id=user_id, username=request.username)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print('User Service Started at PORT 50051')
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
