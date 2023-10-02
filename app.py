from flask import Flask, request, jsonify
from db_connection import establish_connection
from bson import ObjectId

app = Flask(__name__)


@app.route('/users', methods=['GET'])
def get_all_users():
    users_collection = establish_connection()
    
    users_cursor = users_collection.find({})
    
    users_list = []
    
    for user in users_cursor:
        user_dict = {
            "_id": str(user["_id"]),
            "name": user.get("name"),
            "age": user.get("age"),
            "height": user.get("height"),
            "body-structure": user.get("body-structure"),
            "activity": user.get("activity"),
        }
        users_list.append(user_dict)
    
    return jsonify(users_list)

@app.route('/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    users_collection = establish_connection()

    user = users_collection.find_one({"_id": ObjectId(user_id)})

    if user is None:
        return jsonify({"error": "User not found"}), 404

    user_dict = {
        "_id": str(user["_id"]),
        "name": user.get("name"),
        "age": user.get("age"),
        "height": user.get("height"),
        "body-structure": user.get("body-structure"),
        "activity": user.get("activity"),
    }

    return jsonify(user_dict)

if __name__ == '__main__':
    app.run(debug=True)

