from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from bson.objectid import ObjectId
import os
from flask_cors import CORS
# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo = PyMongo(app)
CORS(app)
@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.userentity.find()
    print(users)
    user_list = []
    for user in users:
        user_dict = {
            'user_id': str(user['_id']),
            'username': user['username'],
            'user_status': user['user_status'],
            'gender': user['gender'],
            'membership_type': user['membership_type'],
            'bio': user['bio'],
            'date_of_birth': user['date_of_birth']
        }
        user_list.append(user_dict)
    return jsonify(user_list)

@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.get_json()
    username = user_data['username']

    # Check if the username already exists in the database
    existing_user = mongo.db.userentity.find_one({'username': username})
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 409  # 409 Conflict

    new_user = {
        'username': username,
        'user_status': user_data['user_status'],
        'gender': user_data['gender'],
        'membership_type': user_data['membership_type'],
        'bio': user_data['bio'],
        'date_of_birth': user_data['date_of_birth']
    }
    result = mongo.db.userentity.insert_one(new_user)
    return jsonify({'message': 'User created successfully', 'user_id': str(result.inserted_id)})
# @app.route('/users', methods=['POST'])
# def create_user():
#     user_data = request.get_json()
#     new_user = {
#         'username': user_data['username'],
#         'user_status': user_data['user_status'],
#         'gender': user_data['gender'],
#         'membership_type': user_data['membership_type'],
#         'bio': user_data['bio'],
#         'date_of_birth': user_data['date_of_birth']
#     }
#     result = mongo.db.userentity.insert_one(new_user)
#     return jsonify({'message': 'User created successfully', 'user_id': str(result.inserted_id)})

# Add other routes and functions for updating, deleting, and retrieving users by ID
@app.route('/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.get_json()
    updated_user = {
        'username': user_data['username'],
        'user_status': user_data['user_status'],
        'gender': user_data['gender'],
        'membership_type': user_data['membership_type'],
        'bio': user_data['bio'],
        'date_of_birth': user_data['date_of_birth']
    }
    result = mongo.db.userentity.update_one({'_id': ObjectId(user_id)}, {'$set': updated_user})

    if result.modified_count == 1:
        return jsonify({'message': 'User updated successfully'})
    else:
        return jsonify({'message': 'User not found or not updated'})

@app.route('/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = mongo.db.userentity.delete_one({'_id': ObjectId(user_id)})

    if result.deleted_count == 1:
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'message': 'User not found or not deleted'})



@app.route('/users/<string:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = mongo.db.userentity.find_one({'_id': ObjectId(user_id)})

    if user:
        user_dict = {
            'username': user['username'],
            'user_status': user['user_status'],
            'gender': user['gender'],
            'membership_type': user['membership_type'],
            'bio': user['bio'],
            'date_of_birth': user['date_of_birth']
        }
        return jsonify(user_dict)
    else:
        return jsonify({'message': 'User not found'})
@app.route('/movies/post', methods=['POST'])
def create_movie1():
    movie_data = request.get_json()
    new_movie = {
        'title': movie_data['title'],
        'description': movie_data['description'],
        'genre': movie_data['genre'],
        'duration': movie_data['duration'],
        'image':movie_data['image'],
        'category':movie_data['category'],
    }
    result = mongo.db.movies1.insert_one(new_movie)
    return jsonify({'message': 'Movie created successfully', 'movie_id': str(result.inserted_id)})
@app.route('/movies/get', methods=['GET'])
def get_movies1():
    movies = mongo.db.movies1.find()
    movie_list = []
    for movie in movies:
        movie_dict = {
            'title': movie['title'],
            'description': movie['description'],
            'genre': movie['genre'],
            'duration': movie['duration'],
            'image':movie['image'],
            'category':movie['category'],
        }
        movie_list.append(movie_dict)
    return jsonify(movie_list)
# ////////////////////
@app.route('/movies', methods=['GET'])
def get_movies():
    movies = mongo.db.movies.find()
    movie_list = []
    for movie in movies:
        movie_dict = {
            'title': movie['title'],
            'description': movie['description'],
            'genre': movie['genre'],
            'duration': movie['duration'],
            'userid': movie['userid']
        }
        movie_list.append(movie_dict)
    return jsonify(movie_list)

# Get Movie by ID
@app.route('/movies/<string:movie_id>', methods=['GET'])
def get_movie_by_id(movie_id):
    movie = mongo.db.movies.find_one({'_id': ObjectId(movie_id)})

    if movie:
        movie_dict = {
            'title': movie['title'],
            'description': movie['description'],
            'genre': movie['genre'],
            'duration': movie['duration'],
            'userid': movie['userid']
        }
        return jsonify(movie_dict)
    else:
        return jsonify({'message': 'Movie not found'})

# Create Movie
@app.route('/movies', methods=['POST'])
def create_movie():
    movie_data = request.get_json()
    new_movie = {
        'title': movie_data['title'],
        'description': movie_data['description'],
        'genre': movie_data['genre'],
        'duration': movie_data['duration'],
        'userid': movie_data['userid']  # This links the movie to the user entity
    }
    result = mongo.db.movies.insert_one(new_movie)
    return jsonify({'message': 'Movie created successfully', 'movie_id': str(result.inserted_id)})

# Update Movie
@app.route('/movies/<string:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    movie_data = request.get_json()
    updated_movie = {
        'title': movie_data['title'],
        'description': movie_data['description'],
        'genre': movie_data['genre'],
        'duration': movie_data['duration'],
        'userid': movie_data['userid']  # This links the movie to the user entity
    }
    result = mongo.db.movies.update_one({'_id': ObjectId(movie_id)}, {'$set': updated_movie})

    if result.modified_count == 1:
        return jsonify({'message': 'Movie updated successfully'})
    else:
        return jsonify({'message': 'Movie not found or not updated'})

# Delete Movie
@app.route('/movies/<string:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    result = mongo.db.movies.delete_one({'_id': ObjectId(movie_id)})

    if result.deleted_count == 1:
        return jsonify({'message': 'Movie deleted successfully'})
    else:
        return jsonify({'message': 'Movie not found or not deleted'})
@app.route('/events', methods=['GET'])
def get_events():
    events = mongo.db.events.find()
    event_list = []
    for event in events:
        event_dict = {
            'event_id': str(event['_id']),  # Convert ObjectId to string
            'title': event['title'],
            'date': event['date'],
            'location': event['location']
        }
        event_list.append(event_dict)
    return jsonify(event_list)

# Get Event by ID
@app.route('/events/<string:event_id>', methods=['GET'])
def get_event_by_id(event_id):
    event = mongo.db.events.find_one({'_id': ObjectId(event_id)})

    if event:
        event_dict = {
            'event_id': str(event['_id']),  # Convert ObjectId to string
            'title': event['title'],
            'date': event['date'],
            'location': event['location']
        }
        return jsonify(event_dict)
    else:
        return jsonify({'message': 'Event not found'})

# Create Event
@app.route('/events', methods=['POST'])
def create_event():
    event_data = request.get_json()
    new_event = {
        'title': event_data['title'],
        'date': event_data['date'],
        'location': event_data['location']
    }
    result = mongo.db.events.insert_one(new_event)
    return jsonify({'message': 'Event created successfully', 'event_id': str(result.inserted_id)})

# Update Event
@app.route('/events/<string:event_id>', methods=['PUT'])
def update_event(event_id):
    event_data = request.get_json()
    updated_event = {
        'title': event_data['title'],
        'date': event_data['date'],
        'location': event_data['location']
    }
    result = mongo.db.events.update_one({'_id': ObjectId(event_id)}, {'$set': updated_event})

    if result.modified_count == 1:
        return jsonify({'message': 'Event updated successfully'})
    else:
        return jsonify({'message': 'Event not found or not updated'})

# Delete Event
@app.route('/events/<string:event_id>', methods=['DELETE'])
def delete_event(event_id):
    result = mongo.db.events.delete_one({'_id': ObjectId(event_id)})

    if result.deleted_count == 1:
        return jsonify({'message': 'Event deleted successfully'})
    else:
        return jsonify({'message': 'Event not found or not deleted'})
    # Get All Show Events
@app.route('/show_events', methods=['GET'])
def get_show_events():
    show_events = mongo.db.show_events.find()
    show_event_list = []
    for show_event in show_events:
        show_event_dict = {
            'show_id': str(show_event['_id']),  # Convert ObjectId to string
            'movie_id': show_event['movie_id'],
            'timing': show_event['timing'],
            'category': show_event['category']
        }
        show_event_list.append(show_event_dict)
    return jsonify(show_event_list)

# Get Show Event by ID
@app.route('/show_events/<string:show_id>', methods=['GET'])
def get_show_event_by_id(show_id):
    show_event = mongo.db.show_events.find_one({'_id': ObjectId(show_id)})

    if show_event:
        show_event_dict = {
            'show_id': str(show_event['_id']),  # Convert ObjectId to string
            'movie_id': show_event['movie_id'],
            'timing': show_event['timing'],
            'category': show_event['category']
        }
        return jsonify(show_event_dict)
    else:
        return jsonify({'message': 'Show event not found'})

# Create Show Event
@app.route('/show_events', methods=['POST'])
def create_show_event():
    show_event_data = request.get_json()
    new_show_event = {
        'movie_id': show_event_data['movie_id'],
        'timing': show_event_data['timing'],
        'category': show_event_data['category']
    }
    result = mongo.db.show_events.insert_one(new_show_event)
    return jsonify({'message': 'Show event created successfully', 'show_id': str(result.inserted_id)})

# Update Show Event
@app.route('/show_events/<string:show_id>', methods=['PUT'])
def update_show_event(show_id):
    show_event_data = request.get_json()
    updated_show_event = {
        'movie_id': show_event_data['movie_id'],
        'timing': show_event_data['timing'],
        'category': show_event_data['category']
    }
    result = mongo.db.show_events.update_one({'_id': ObjectId(show_id)}, {'$set': updated_show_event})

    if result.modified_count == 1:
        return jsonify({'message': 'Show event updated successfully'})
    else:
        return jsonify({'message': 'Show event not found or not updated'})

# Delete Show Event
@app.route('/show_events/<string:show_id>', methods=['DELETE'])
def delete_show_event(show_id):
    result = mongo.db.show_events.delete_one({'_id': ObjectId(show_id)})

    if result.deleted_count == 1:
        return jsonify({'message': 'Show event deleted successfully'})
    else:
        return jsonify({'message': 'Show event not found or not deleted'})
@app.route('/participant_events', methods=['GET'])
def get_participant_events():
    participant_events = mongo.db.participant_events.find()
    participant_event_list = []
    for participant_event in participant_events:
        participant_event_dict = {
            'participant_event_id': str(participant_event['_id']),  # Convert ObjectId to string
            'event_id': participant_event['event_id'],
            'user_id': participant_event['user_id']
        }
        participant_event_list.append(participant_event_dict)
    return jsonify(participant_event_list)

# Get Participant Event by ID
@app.route('/participant_events/<string:participant_event_id>', methods=['GET'])
def get_participant_event_by_id(participant_event_id):
    participant_event = mongo.db.participant_events.find_one({'_id': ObjectId(participant_event_id)})

    if participant_event:
        participant_event_dict = {
            'participant_event_id': str(participant_event['_id']),  # Convert ObjectId to string
            'event_id': participant_event['event_id'],
            'user_id': participant_event['user_id']
        }
        return jsonify(participant_event_dict)
    else:
        return jsonify({'message': 'Participant event not found'})

# Create Participant Event
@app.route('/participant_events', methods=['POST'])
def create_participant_event():
    participant_event_data = request.get_json()
    new_participant_event = {
        'event_id': participant_event_data['event_id'],
        'user_id': participant_event_data['user_id']
    }
    result = mongo.db.participant_events.insert_one(new_participant_event)
    return jsonify({'message': 'Participant event created successfully', 'participant_event_id': str(result.inserted_id)})

# Update Participant Event
@app.route('/participant_events/<string:participant_event_id>', methods=['PUT'])
def update_participant_event(participant_event_id):
    participant_event_data = request.get_json()
    updated_participant_event = {
        'event_id': participant_event_data['event_id'],
        'user_id': participant_event_data['user_id']
    }
    result = mongo.db.participant_events.update_one({'_id': ObjectId(participant_event_id)}, {'$set': updated_participant_event})

    if result.modified_count == 1:
        return jsonify({'message': 'Participant event updated successfully'})
    else:
        return jsonify({'message': 'Participant event not found or not updated'})

# Delete Participant Event
@app.route('/participant_events/<string:participant_event_id>', methods=['DELETE'])
def delete_participant_event(participant_event_id):
    result = mongo.db.participant_events.delete_one({'_id': ObjectId(participant_event_id)})

    if result.deleted_count == 1:
        return jsonify({'message': 'Participant event deleted successfully'})
    else:
        return jsonify({'message': 'Participant event not found or not deleted'})
if __name__ == '__main__':
    app.run(debug=True)