from flask import Flask, request, jsonify
from flask_cors import CORS
from gpt_service import callChatGPT_async, callChatGPT_ask, callChatGPT_list, callChatGPT_properties
from paapi_service import search_items, search_items_with_price 
from firebase_service import save_user_email, save_search_history, retrieve_search_history

app = Flask(__name__)
CORS(app)

@app.route('/')
def default():
    return 'default path'

@app.route('/api/generateList', methods=['POST'])
def generateList():
    try:
        print('generateList try')
        data = request.get_json()
        # print("search()"+str(data))
        # if 'email' in data: # if user is logged in
        #     save_search_history(data['email'], data['list_query'])
        result = callChatGPT_list(data)
        return jsonify(result), 200
    except Exception as e:
        print('search error')
        print(e)
        return jsonify({"error": "An error occurred while processing the request"}), 500

@app.route('/api/search', methods=['POST'])
def search():
    try:
        print('search try')
        data = request.get_json()
        # print("search()"+str(data))
        search_results = search_items(data['item_query']).search_result.items
        if 'email' in data: # if user is logged in
            save_search_history(data['email'], data['item_query'])            
        result = callChatGPT_async(data['item_query'], data['language'], search_results)
        return jsonify(result), 200
    except Exception as e:
        print('search error')
        print(e)
        return jsonify({"error": "An error occurred while processing the request"}), 500
    
@app.route('/api/searchProperties', methods=['POST'])
def searchProperties():
    try:
        print('searchProperties try')
        data = request.get_json()
        # print("search()"+str(data))
        result = callChatGPT_properties(data)
        return jsonify(result), 200
    except Exception as e:
        print('search error')
        print(e)
        return jsonify({"error": "An error occurred while processing the request"}), 500    

@app.route('/api/refineSearch', methods=['POST'])
def refineSearch():
    try:
        data = request.get_json()
        qualities = list(data['qualities'].values())      
        item_query = ', '.join([data['target']] + qualities)
        # print("item_query"+ item_query)
        search_results = search_items_with_price(item_query, data['minPrice'], data['maxPrice']).search_result.items
        result = callChatGPT_async(data['target'], data['language'], search_results)
        return jsonify(result), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "An error occurred while processing the request"}), 500
    
@app.route('/api/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        result = callChatGPT_ask(data)
        return jsonify(result), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "An error occurred while processing the request"}), 500

@app.route('/api/saveEmail', methods=['POST'])
def saveEmail():
    try:
        data = request.get_json()
        save_user_email(data['email'])
        return jsonify({"message": "Email saved successfully"}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "An error occurred while processing the request"}), 500

@app.route('/api/search-history/<email>', methods=['GET'])
def getUserSearchHistory(email):
    try:
        # Fetch user's search history from the database
        search_history = retrieve_search_history(email)
        return jsonify({"searchHistory": search_history}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "An error occurred while processing the request"}), 500

if __name__ == '__main__':
    app.run(debug=True)