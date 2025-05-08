from pymongo import MongoClient
from bson.objectid import ObjectId
import os

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URI)
db = client['job_portal']

jobs_collection = db['jobs']
results_collection = db['results']
admit_cards_collection = db['admit_cards']
subscribers_collection = db['subscribers']
important_links_collection = db['important_links']
answer_keys_collection = db['answer_keys']
syllabus_collection = db['syllabus']
admin_collection = db['admin'] # Add admin collection

# Function to get admin user by username
def get_admin_by_username(username):
    return admin_collection.find_one({'username': username})

# Function to update admin password
def update_admin_password_in_db(username, new_hashed_password):
    return admin_collection.update_one({'username': username}, {'$set': {'password': new_hashed_password}})

# Function to create an admin user (useful for initial setup)
def create_admin(username, hashed_password):
    if not get_admin_by_username(username):
        admin_collection.insert_one({'username': username, 'password': hashed_password})
        print(f"Admin user '{username}' created.")
    else:
        print(f"Admin user '{username}' already exists.")

# Function to get all admin users
def get_all_admins():
    return list(admin_collection.find())

# Function to delete an admin user by ID
def delete_admin_by_id(user_id):
    return admin_collection.delete_one({'_id': ObjectId(user_id)})


def get_job_by_id(job_id):
    return jobs_collection.find_one({'_id': ObjectId(job_id)})

def get_jobs(filter_query=None, skip=0, limit=10):
    filter_query = filter_query or {}
    return list(jobs_collection.find(filter_query).skip(skip).limit(limit))

def count_jobs(filter_query=None):
    filter_query = filter_query or {}
    return jobs_collection.count_documents(filter_query)

def insert_job(job):
    """Insert a new job"""
    # Check if a job with the same title and category already exists
    existing_job = jobs_collection.find_one({
        'title': job.get('title'),
        'category': job.get('category')
    })
    
    if existing_job:
        return None  # Return None if duplicate found
    
    return jobs_collection.insert_one(job)

def update_job_in_db(job_id, job):
    return jobs_collection.update_one({'_id': ObjectId(job_id)}, {'$set': job})

def delete_job(job_id):
    return jobs_collection.delete_one({'_id': ObjectId(job_id)})

def get_results(skip=0, limit=10):
    return list(results_collection.find().skip(skip).limit(limit))

def count_results():
    return results_collection.count_documents({})

def insert_result(result):
    """Insert a new result"""
    # Check if a result with the same title and link already exists
    existing_result = results_collection.find_one({
        'title': result.get('title'),
        'link': result.get('link')
    })
    
    if existing_result:
        return None  # Return None if duplicate found
    
    return results_collection.insert_one(result)

def update_result_in_db(result_id, result):
    return results_collection.update_one({'_id': ObjectId(result_id)}, {'$set': result})

def delete_result(result_id):
    return results_collection.delete_one({'_id': ObjectId(result_id)})

def get_admit_cards(skip=0, limit=10):
    return list(admit_cards_collection.find().skip(skip).limit(limit))

def count_admit_cards():
    return admit_cards_collection.count_documents({})

def insert_admit_card(admit_card):
    """Insert a new admit card"""
    # Check if an admit card with the same title and link already exists
    existing_admit_card = admit_cards_collection.find_one({
        'title': admit_card.get('title'),
        'link': admit_card.get('link')
    })
    
    if existing_admit_card:
        return None  # Return None if duplicate found
    
    return admit_cards_collection.insert_one(admit_card)

def update_admit_card_in_db(admit_card_id, admit_card):
    return admit_cards_collection.update_one({'_id': ObjectId(admit_card_id)}, {'$set': admit_card})

def delete_admit_card(admit_card_id):
    return admit_cards_collection.delete_one({'_id': ObjectId(admit_card_id)})

def insert_subscriber(email):
    return subscribers_collection.insert_one({'email': email})

def get_important_links():
    """Get all important links"""
    return list(important_links_collection.find())

def insert_important_link(link_data):
    """Insert a new important link"""
    # Check if a link with the same title and URL already exists
    existing_link = important_links_collection.find_one({
        'title': link_data.get('title'),
        'url': link_data.get('url')
    })
    
    if existing_link:
        return None  # Return None if duplicate found
    
    return important_links_collection.insert_one(link_data)

def update_important_link(link_id, link_data):
    """Update an important link"""
    return important_links_collection.update_one(
        {'_id': ObjectId(link_id)},
        {'$set': link_data}
    )

def delete_important_link(link_id):
    """Delete an important link"""
    return important_links_collection.delete_one({'_id': ObjectId(link_id)})

def get_answer_keys(skip=0, limit=10):
    return list(answer_keys_collection.find().skip(skip).limit(limit))

def count_answer_keys():
    return answer_keys_collection.count_documents({})

def insert_answer_key(answer_key):
    """Insert a new answer key"""
    # Check if an answer key with the same title and link already exists
    existing_answer_key = answer_keys_collection.find_one({
        'title': answer_key.get('title'),
        'link': answer_key.get('link')
    })
    
    if existing_answer_key:
        return None  # Return None if duplicate found
    
    return answer_keys_collection.insert_one(answer_key)

def update_answer_key_in_db(answer_key_id, answer_key):
    return answer_keys_collection.update_one({'_id': ObjectId(answer_key_id)}, {'$set': answer_key})

def delete_answer_key(answer_key_id):
    return answer_keys_collection.delete_one({'_id': ObjectId(answer_key_id)})

def get_syllabus(skip=0, limit=10):
    return list(syllabus_collection.find().skip(skip).limit(limit))

def count_syllabus():
    return syllabus_collection.count_documents({})

def insert_syllabus(syllabus):
    """Insert a new syllabus"""
    # Check if a syllabus with the same title and link already exists
    existing_syllabus = syllabus_collection.find_one({
        'title': syllabus.get('title'),
        'link': syllabus.get('link')
    })
    
    if existing_syllabus:
        return None  # Return None if duplicate found
    
    return syllabus_collection.insert_one(syllabus)

def update_syllabus_in_db(syllabus_id, syllabus):
    return syllabus_collection.update_one({'_id': ObjectId(syllabus_id)}, {'$set': syllabus})

def delete_syllabus(syllabus_id):
    return syllabus_collection.delete_one({'_id': ObjectId(syllabus_id)})

def get_answer_key_by_id(answer_key_id):
    return answer_keys_collection.find_one({'_id': ObjectId(answer_key_id)})

def get_syllabus_by_id(syllabus_id):
    return syllabus_collection.find_one({'_id': ObjectId(syllabus_id)})

def get_admin_by_id(user_id):
    return admin_collection.find_one({'_id': ObjectId(user_id)})

class Result:
    def __init__(self, title, link, date_published, pdf_link=None):
        self.title = title
        self.link = link
        self.date_published = date_published
        self.pdf_link = pdf_link