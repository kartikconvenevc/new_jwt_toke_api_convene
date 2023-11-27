from flask import Flask, jsonify, request
import jwt
import time
import os
import base64
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv() 

app = Flask(__name__)
CORS(app)


@app.route('/generate-jwt')
def generate_jwt():

    user_name = request.args.get('user_name')
    user_email = request.args.get('user_email')
    room_name = request.args.get('room_name')

    payload = {
        "aud": os.getenv('JWT_APP_ID'),
        "iss": os.getenv('JWT_APP_ID'),
        "sub": os.getenv('JWT_SUB'),
        "room": room_name,
        "nbf": int(time.time()),
        "exp": int(time.time()) + 3600,
        "iat": int(time.time()),
        "context": {
            "user": {
                "avatar": os.getenv('AVATAR_URL'),
                "name": user_name,
                "email": user_email,
            },
        }
    }

    secret = os.getenv('JWT_APP_SECRET')
    #secret = str(secret)
   # print(secret)
   # print(type(secret))

    encoded_jwt = jwt.encode(payload, secret, algorithm="HS256")

    return jsonify(
        token=encoded_jwt,
        url=f'{os.getenv("DOMAIN")}{os.getenv("ROOM_NAME")}?jwt={encoded_jwt}',
    )



if __name__ == "__main__":
   # pass
    app.run(host='localhost',port=int("5000"), debug=True)
