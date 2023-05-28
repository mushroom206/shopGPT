# firebase_service.py

import os
import json
import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, firestore

# Load environment variables
load_dotenv()

# Get the Firebase service account key from the environment variables
service_account_key_json = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY')

# Validate that the service account key is not None
if service_account_key_json is None:
    raise ValueError("Missing the Firebase service account key. Please set the environment variable 'FIREBASE_SERVICE_ACCOUNT_KEY'")

# Parse the JSON string into a Python dictionary
service_account_key = json.loads(service_account_key_json)

# Use the service account key to initialize the Firebase Admin SDK
cred = credentials.Certificate(service_account_key)
default_app = firebase_admin.initialize_app(cred)

db = firestore.client()

def save_user_email(email):
    # Validate that email is not None
    if email is None:
        raise ValueError("Invalid email. Email should not be None.")

    users_ref = db.collection('users')
    docs = users_ref.where('email', '==', email).get()
    if len(docs) == 0: # user email doesn't exist in the db
        users_ref.add({
            'email': email,
        })

def save_search_history(email, item_query):
    # Validate that email and item_query are not None
    if email is None or item_query is None:
        raise ValueError("Invalid input. Email and search query should not be None.")

    users_ref = db.collection('users')
    user_doc = users_ref.where('email', '==', email).get()
    
    # Error handling if user doesn't exist
    if len(user_doc) == 0:
        raise ValueError("Invalid input. User with provided email doesn't exist.")
    
    # Assuming user document is the first and only document in the query response
    user_ref = users_ref.document(user_doc[0].id)
    
    history_ref = user_ref.collection('search_history')
    history_ref.add({
        'search_query': item_query,
    })
