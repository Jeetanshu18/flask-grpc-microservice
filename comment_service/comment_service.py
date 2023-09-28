import grpc
from concurrent import futures
import comment_pb2
import comment_pb2_grpc

class CommentService(comment_pb2_grpc.CommentServiceServicer):
    def CreateComment(self, request, context):
        # Your code to create a comment in the database
        comment_id = "98765"  # Simulated comment_id
        return comment_pb2.CommentResponse(
            comment_id=comment_id,
            user_id=request.user_id,
            post_id=request.post_id,
            content=request.content
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    comment_pb2_grpc.add_CommentServiceServicer_to_server(CommentService(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    print('Comment Service Started at PORT 50053')
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
