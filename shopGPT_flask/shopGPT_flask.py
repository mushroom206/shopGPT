from flask import Flask, request, jsonify
from flask_cors import CORS
from gpt_service import callChatGPT, callChatGPT_refine, callChatGPT_ask

app = Flask(__name__)
CORS(app)

@app.route('/')
def default():
    return 'default path'

@app.route('/api/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        result = callChatGPT(data)
        return jsonify(result), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "An error occurred while processing the request"}), 500

@app.route('/api/refineSearch', methods=['POST'])
def refineSearch():
    try:
        data = request.get_json()
        result = callChatGPT_refine(data)
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

if __name__ == '__main__':
    app.run(debug=True)