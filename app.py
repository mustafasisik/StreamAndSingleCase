import json
from flask import Flask, request, jsonify, Response
from flask_limiter import Limiter, HEADERS
from flask_limiter.util import get_remote_address
import hashlib
import time

app = Flask(__name__)
rate_limit_value = "4 per minute"
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=[rate_limit_value],
    storage_uri="memory://",
    header_name_mapping={
        HEADERS.LIMIT: "X-RateLimit-Limit",
        HEADERS.RESET: "X-RateLimit-Reset",
        HEADERS.REMAINING: "X-RateLimit-Remaining"
    }
)


# User data dictionary to store visit counts and stream sequence numbers
user_data = {}


@app.route('/api', methods=['GET'])
@limiter.limit(rate_limit_value)
def api():
    # Get the authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer USER'):
        return jsonify({"error": "Unauthorized"}), 401

    # Extract the user ID from the token
    user_id = auth_header.split('USER')[1]

    # Update visit count
    user_data.setdefault(user_id, {'visit_count': 0, 'stream_seq': 0})
    user_data[user_id]['visit_count'] += 1

    # Determine group based on hashed user ID
    group = int(hashlib.sha256(user_id.encode()).hexdigest(), 16) % 10 + 1

    # Get the query parameter "stream"
    stream = request.args.get('stream', default='false')

    if stream == 'true':
        return Response(generate_messages(user_id, user_data), mimetype='text/event-stream')
    else:
        # Respond immediately without streaming
        response = {
            "message": f"Welcome USER_{user_id}, this is your visit #{user_data[user_id]['visit_count']}",
            "group": group,
            "rate_limit_left": limiter.current_limit.remaining,
            "stream_seq": 0
        }
        return jsonify(response)


def generate_messages(user_id, user_data):
    max_messages = 5  # Limit the number of messages to 5
    for i in range(max_messages):
        user_data[user_id]['stream_seq'] += 1
        group = "example_group"  # Replace with the actual group name
        response = {
            "message": f"Welcome USER_{user_id}, this is your visit #{user_data[user_id]['visit_count']}",
            "group": group,
            "rate_limit_left": 0,  # Replace with the actual rate limit left
            "stream_seq": user_data[user_id]['stream_seq']
        }
        print(response)
        yield json.dumps(response).encode('utf-8') + b'\n\n'
        user_data[user_id]['visit_count'] += 1
        time.sleep(1)

# Example client code to test the API
if __name__ == '__main__':
    app.run(debug=True)
