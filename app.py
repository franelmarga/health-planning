from flask import Flask, request, jsonify
from db_connection import establish_connection
from bson import ObjectId
import openai
import os

openai.api_key = os.environ.get('OPENAI_API_KEY')

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
            "weight": user.get("weight"),
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
        "weight": user.get("weight"),
        "height": user.get("height"),
        "body-structure": user.get("body-structure"),
        "activity": user.get("activity"),
    }

    return user

@app.route('/generate_diet/<string:user_id>', methods=['GET'])
def generate_individual_diet(user_id):

    users_collection = establish_connection()
    user = users_collection.find_one({"_id": ObjectId(user_id)})

    if user is None:
        return jsonify({"error": "User not found"}), 404

    nutrition_plan = generate_diet(user)

    response_data = {
        "_id": user_id,
        "nutrition_plan": nutrition_plan
    }

    return jsonify(response_data)

def generate_diet(user):
    
    prompt = f"Hello, I'm {user['name']} and I am {user['age']} years old. "
    prompt += f"My height is {user['height']} cm and my weight is {user['weight']} kg. "
    prompt += f"I have a {user['body-structure']} body structure and my activity level is {user['activity']}. "
    prompt += "I need to create a weekly diet, day per day, with all the specific meals, with the previous conditions."

    # Call the OpenAI API to get the response
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150  
    )
    

    return response.choices[0].text


if __name__ == '__main__':
    app.run(debug=True)

