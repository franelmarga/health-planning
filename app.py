from flask import Flask, request, jsonify
from db_connection import stablish_connection
from bson import ObjectId

app = Flask(__name__)

# Route to all users
@app.route('/users', methods=['GET'])
def get_all_users():
    users_collection = stablish_connection()
    
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

if __name__ == '__main__':
    app.run(debug=True)
