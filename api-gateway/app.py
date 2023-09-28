from flask import Flask, request, jsonify
import grpc
import user_pb2
import user_pb2_grpc
import post_pb2
import post_pb2_grpc
import comment_pb2
import comment_pb2_grpc

app = Flask(__name__)

# gRPC client setup
user_service_channel = grpc.insecure_channel('localhost:50051')
user_service_stub = user_pb2_grpc.UserServiceStub(user_service_channel)

post_service_channel = grpc.insecure_channel('localhost:50052')
post_service_stub = post_pb2_grpc.PostServiceStub(post_service_channel)

comment_service_channel = grpc.insecure_channel('localhost:50053')
comment_service_stub = comment_pb2_grpc.CommentServiceStub(comment_service_channel)

@app.route('/create_user', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        username = data['username']
        email = data['email']
        password = data['password']

        # Call the gRPC User Service to create a user
        user_request = user_pb2.UserRequest(
            username=username,
            email=email,
            password=password
        )
        user_response = user_service_stub.CreateUser(user_request)

        return jsonify({
            'user_id': user_response.user_id,
            'username': user_response.username
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/create_post', methods=['POST'])
def create_post():
    try:
        data = request.get_json()
        user_id = data['user_id']
        content = data['content']

        # Call the gRPC Post Service to create a post
        post_request = post_pb2.PostRequest(
            user_id=user_id,
            content=content
        )
        post_response = post_service_stub.CreatePost(post_request)

        return jsonify({
            'post_id': post_response.post_id,
            'user_id': post_response.user_id,
            'content': post_response.content
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/create_comment', methods=['POST'])
def create_comment():
    try:
        data = request.get_json()
        user_id = data['user_id']
        post_id = data['post_id']
        content = data['content']

        # Call the gRPC Comment Service to create a comment
        comment_request = comment_pb2.CommentRequest(
            user_id=user_id,
            post_id=post_id,
            content=content
        )
        comment_response = comment_service_stub.CreateComment(comment_request)

        return jsonify({
            'comment_id': comment_response.comment_id,
            'user_id': comment_response.user_id,
            'post_id': comment_response.post_id,
            'content': comment_response.content
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
