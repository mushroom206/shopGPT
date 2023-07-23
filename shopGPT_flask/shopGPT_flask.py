from flask import Flask, request, jsonify
from flask_cors import CORS
from gpt_service import callChatGPT_async, callChatGPT_ask, callChatGPT_list, callChatGPT_properties
from paapi_service import search_items, search_items_with_price, get_variations
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
        data = request.get_json()
        # print("search()"+str(data))
        search_results = search_items(data['item_query']).search_result
        if search_results is None:
            result = {
                "target": data['item_query'],
                "choices":[],
                "empty": True
            }
            return jsonify(result), 200
        search_results_items = search_results.items
        if 'email' in data: # if user is logged in
            save_search_history(data['email'], data['item_query'])            
        result = callChatGPT_async(data['item_query'], data['language'], search_results_items)
        if len(result['choices']) == 0:
            result = {
                "target": data['item_query'],
                "choices":[],
                "empty": True
            }
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
        item_query = ' '.join([data['target']] + qualities)
        print("item_query"+ item_query)
        search_results = search_items_with_price(item_query, data['minPrice'], data['maxPrice']).search_result
        if search_results is None:
            result = {
                "target": data['target'],
                "choices":[],
                "empty": True
            }
            return jsonify(result), 200
        search_results_items = search_results.items
        result = callChatGPT_async(data['target'], data['language'], search_results_items)
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
    
@app.route('/api/get-variants/<asin>', methods=['GET'])
def getVariants(asin):
    response = {
        "asin": asin,
        "variants": [],
        "variation_dimensions": []
    }
    try:
        result = get_variations(asin, 1)
        if result.errors:
            response["error"] = result.errors[0].code
            return response
        if result.variations_result.variation_summary:
            if result.variations_result.variation_summary.page_count != 1:
                result2 = get_variations(asin, 2)
                result.variations_result.items += result2.variations_result.items
        result = result.variations_result
        variants = result.items
        if result.variation_summary:
            for variation_dimension in result.variation_summary.variation_dimensions:
                values = []
                for variant in variants:
                    item = next((obj for obj in variant.variation_attributes if obj.name == variation_dimension.name), None)
                    if item and (variant.offers and variant.offers.listings[0].price):
                        if item.value not in values:
                            values.append(item.value)
                temp_dime = {
                    "display_name": variation_dimension.display_name,
                    "name": variation_dimension.name,
                    "values": values
                }
                response['variation_dimensions'].append(temp_dime)
        for variant in variants:
            if variant.offers and variant.offers.listings[0].price:
                saving_amount = "check variant"
                saving_percentage = "check variant" 
                if(variant.offers.listings[0].price.savings):
                    saving_amount = variant.offers.listings[0].price.savings.amount
                    saving_percentage = variant.offers.listings[0].price.savings.percentage
                price = variant.offers.listings[0].price.display_amount
                amount = variant.offers.listings[0].price.amount
                amazon_fulfill = variant.offers.listings[0].delivery_info.is_amazon_fulfilled
                free_shipping = variant.offers.listings[0].delivery_info.is_free_shipping_eligible
                prime_eligible = variant.offers.listings[0].delivery_info.is_prime_eligible
                image_urls = []
                image_urls.append(variant.images.primary.large.url)
                if variant.images.variants:
                    for url in variant.images.variants:
                        image_urls.append(url.large.url)
                variation_attributes = []        
                for variation_attribute in variant.variation_attributes:
                    temp_attr = {
                        "name": variation_attribute.name,
                        "value": variation_attribute.value
                    }
                    variation_attributes.append(temp_attr)   
                temp = {
                    "url": variant.detail_page_url,
                    "asin": variant.asin,
                    "price": price,
                    "amount": amount,
                    "saving_amount": saving_amount,
                    "saving_percentage": saving_percentage,
                    "amazon_fulfill": amazon_fulfill,
                    "free_shipping": free_shipping,
                    "prime_eligible": prime_eligible,
                    "image_urls": image_urls,
                    "variation_attributes": variation_attributes
                }
                response['variants'].append(temp)
        return jsonify(response), 200
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