import openai
from dotenv import load_dotenv
import os
import threading
import json
import random
import time

from paapi_service import get_variations

# Load environment variables
load_dotenv()

# Get the API key from the environment variables and set it for the openai package
openai.api_key = os.getenv('OPENAI_API_KEY')

def callChatGPT_list(data):
    # print("callChatGPT_list")
    # print(data)
    MAX_RETRIES = 3
    retries = 0
    while retries < MAX_RETRIES:
        try:
            completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "user", "content": """Generate a list of items relevant to {context} as [item1,item2,item3...], so I can shop and prepare for {context}.
                    Try to generate items specific to {context} unless out of options.
                    If out of options, return items in higher level or broader categories. 
                    Eliminate ambiguity, for example, instead of toys you should return cat toys or dog toys.
                    Do not include {context} membership or member ship card.
                    For {context} IDs or access cards, return card holder instead.
                    Do not generate description of items. return 5 items.  
                    Generate your response in valid JSON format, watch out for symbols or contents that may break valid JSON format.
                    Do not write anything outside of the JSON structure. 
                    Write the Value of JSON in """+ data['language'] +""", Key of JSON in English. 
                    The structure is as follow: 
                    {
                    "context": "",
                    "itemList": []
                    }
                    context is type String, and itemList is type List.
                    now {context} =""" + data['list_query']
                    }
            ]
            )
            response = completion.choices[0].message.content
            # print(response)
            return response
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        retries += 1
        time.sleep(1)      

def callChatGPT_get_more_items(data):
    # print("callChatGPT_get_more_items")
    # print(data)
    MAX_RETRIES = 3
    retries = 0
    while retries < MAX_RETRIES:
        try:
            completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "user", "content": """Generate a list of items relevant to {context} as [item1,item2,item3...], so I can shop and prepare for {context}.
                    Do not include these items: """+ str.join(', ', data['itemList']) +""". 
                    Try to generate items specific to {context} unless out of options.
                    If out of options, return items in higher level or broader categories.
                    Eliminate ambiguity, for example, instead of toys you should return cat toys or dog toys.
                    Do not include {context} membership or member ship card.
                    For {context} IDs or access cards, return card holder instead.
                    Do not generate description of items. return 5 items.  
                    Generate your response in valid JSON format, watch out for symbols or contents that may break valid JSON format.
                    Do not write anything outside of the JSON structure. 
                    Write the Value of JSON in """+ data['language'] +""", Key of JSON in English. 
                    The structure is as follow: 
                    {
                    "context": "",
                    "itemList": []
                    }
                    context is type String, and itemList is type List.
                    now {context} =""" + data['context']
                    }
                    
                ]
            )
            response = completion.choices[0].message.content
            # print(response)
            return response
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        retries += 1
        time.sleep(1)

def callChatGPT_async(target, language, search_results):
    # Create three threads to call ChatGPT simultaneously.
    threads = []
    result1 = [None]*1
    result2 = [None]*1
    result3 = [None]*1
    result4 = [None]*1
    result5 = [None]*1
    result6 = [None]*1
    results = [result1, result2, result3, result4, result5, result6]
    targets = []
    image_urls = []
    prices = []
    amounts = []
    saving_amounts = []
    saving_percentages = []
    amazon_fulfills = []
    free_shippings = []
    prime_eligibles = []
    scores = []
    # search_results = random.sample(search_results, min(3, len(search_results)))
    for i, search_result in enumerate(search_results):
        targets.append(search_result.item_info.title.display_value)
        data = {
            "language": language,
            "item_query": search_result.item_info.title.display_value,
            "details": search_result.detail_page_url
        }

        score = 0

        image_urls.append([])
        image_urls[i].append(search_result.images.primary.large.url)
        if search_result.images.variants:
            for url in search_result.images.variants:
                image_urls[i].append(url.large.url)
        try:
            prices.append(search_result.offers.listings[0].price.display_amount)
            score += 1
        except AttributeError:
            prices.append("check variants")

        try:
            amounts.append(search_result.offers.listings[0].price.amount)
        except AttributeError:
            amounts.append("check variants")    

        try:
            saving_amounts.append(search_result.offers.listings[0].price.savings.amount)
        except AttributeError:
            saving_amounts.append("check variants")

        try:
            saving_percentages.append(search_result.offers.listings[0].price.savings.percentage)
            if search_result.offers.listings[0].price.savings.percentage >= 20:
                score += 1
        except AttributeError:
            saving_percentages.append("check variants")  

        try:
            amazon_fulfills.append(search_result.offers.listings[0].delivery_info.is_amazon_fulfilled)
            if search_result.offers.listings[0].delivery_info.is_amazon_fulfilled:
                score += 1
        except AttributeError:
            amazon_fulfills.append("view on checkout")

        try:
            free_shippings.append(search_result.offers.listings[0].delivery_info.is_free_shipping_eligible)
            if search_result.offers.listings[0].delivery_info.is_free_shipping_eligible:
                score += 1
        except AttributeError:
            free_shippings.append("view on checkout")

        try:
            prime_eligibles.append(search_result.offers.listings[0].delivery_info.is_prime_eligible)
            if search_result.offers.listings[0].delivery_info.is_prime_eligible:
                score += 1
        except AttributeError:
            prime_eligibles.append("view on checkout")

        scores.append(score)                

    #     thread = threading.Thread(target=callChatGPT, args=(data, results[i]))
    #     thread.start()
    #     threads.append(thread)
    #     # thread = threading.Thread(target=callPaapi_variations, args=(search_result.asin, results[i+3]))
    #     # thread.start()
    #     # threads.append(thread)


    # # Wait for all threads to finish.
    # for thread in threads:
    #     thread.join()

    # Get the results for each thread.
    response = {
            "target" : target,
            "choices": []
            }
    minScore = 5
    x = 0
    while x < len(search_results):
        # if results[x][0] is not None:
        #   temp1 = json.loads(results[x][0])
        #   temp2 = json.loads(results[x+3][0])
          tempJSON = {
                #   "target": temp1['target'],
                #   "variations": temp2,
                #   "pros": temp1['pros'],
                  "target": targets[x],
                  "pros": [],
                  "cons": [],
                  "url": search_results[x].detail_page_url,
                  "asin": search_results[x].asin,
                  "parent_asin": search_results[x].parent_asin,
                  "price": prices[x],
                  "amount": amounts[x],
                  "saving_amount": saving_amounts[x],
                  "saving_percentage": saving_percentages[x],
                  "amazon_fulfill": amazon_fulfills[x],
                  "free_shipping": free_shippings[x],
                  "prime_eligible": prime_eligibles[x],
                  "image_urls": image_urls[x]
                  }
          if scores[x] == minScore:
            response['choices'].append(tempJSON)
            del search_results[x]
            if x == len(search_results):
              if len(response['choices']) < 3 and minScore >= 2:
                  minScore = minScore - 1
                  x = 0
              else:
                  x += 1    
            else:
                x += 1      
          else:
            if x == len(search_results)-1:
              if len(response['choices']) < 3 and minScore >= 2:
                  minScore = minScore - 1
                  x = 0
              else:
                  x += 1    
            else:
                x += 1               

    # print(response)
    if len(response['choices']) > 3:
        response['choices'] = random.sample(response['choices'], 3)
    return response 

def callChatGPT(data, result):
    # print("callChatGPT")
    # Generate a list of 3 specific items that fits the description of {target} as [choice1, choice2, choice3], 
    # breakdown each choice into [brand, item category, and model], 
    # detailed enough so I can use your response to query for the items on a shopping site like Amazon. 
    MAX_RETRIES = 3
    retries = 0
    while retries < MAX_RETRIES:
        try:
            completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "user", "content": """you are my shopping advisor. 
                    Define {target} as a product.
                    In """+ data['language'] +""", generate a list of at most 3 pros of {target}.
                    Generate your response in valid JSON format, watch out for symbols or contents that may break valid JSON format. 
                    Do not write anything outside of the JSON structure. 
                    Write the Value of JSON in """+ data['language'] +""", Key of JSON in English.
                    Make {target} concise, 5 words max , include brand.
                    The structure is as follow: 
                    {
                    "target": "",
                    "pros": []
                    }
                    now {target} =""" + data['item_query']
                    }
            ]
            )
            response = completion.choices[0].message.content
            result[0] = response
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        retries += 1
        time.sleep(1)      

# def callChatGPT_description(data, result):
#     # print("callChatGPT_description")
#     # print(data)
#     # Generate a list of 3 specific items that fits the description of {target} as [choice1, choice2, choice3], 
#     # breakdown each choice into [brand, item category, and model], 
#     # detailed enough so I can use your response to query for the items on a shopping site like Amazon. 
#     completion = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=[
#             {"role": "user", "content": """you are my shopping advisor. But do not mention you are my shopping advisor.
#             Define {target} as an item category or a concept of an item. 
#             Define {details} as your product reference link, do not include or mention the actual link in the description.
#             In """+ data['language'] +""", generate a brief one paragrapg description using first person angle, speak as if you have used the product and the description is from personal use experience.
#               Generate your response in valid JSON format, watch for symbols, new lines and contents that may break valid JSON format. 
#               Do not write anything outside of the JSON structure. 
#               Write the Value of JSON in """+ data['language'] +""", Key of JSON in English. 
#               The structure is as follow: 
#             {
#               "description": ""
#             }
#             now {target} =""" + data['item_query'] + """. {details} = """ + data['details']
#             }
#     ]
#     )
#     response = completion.choices[0].message.content
#     if not response.endswith('}'):
#       response += '}'
#     result[0] = response
    # print(result[0])

def callChatGPT_properties(data):
    # print("callChatGPT_properties")
    # print(data)
    MAX_RETRIES = 3
    retries = 0
    while retries < MAX_RETRIES:
        try:
            completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "user", "content": """you are my shopping advisor. 
                    Define {target} as an item category or a concept of an item. 
                    In """+ data['language'] +""", generate 3 most common and important quality or properties specific to {target} that affect how consumers compare {target}, but do not include price. 
                    For example, 
                    if {target} = rice cooker, the quality or properties that may affect your choices can be material, size, design, etc. 
                    For each quality or property, generate 3 options. 
                    Options should be specific enough to help further filtering possible results on site like Amazon.
                    For search accuracy, use numerical value in options if applicable.
                    Generate your response in valid JSON format, watch out for symbols or contents that may break valid JSON format.
                    Do not write anything outside of the JSON structure. 
                    Write the Value of JSON in """+ data['language'] +""", Key of JSON in English. 
                    Keep the Value of {target} in english.
                    The structure is as follow: 
                    {
                    "target": "",
                    "qualities-properties": [
                    {
                    "quality":"",
                    "options": []
                    },
                    {
                    "quality":"",
                    "options": []
                    },
                    {
                    "quality":"",
                    "options": []
                    }
                    ]
                    }
                    now {target} =""" + data['item_query']
                    }
            ]
            )
            response = completion.choices[0].message.content
            # print(response)
            return response
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        retries += 1
        time.sleep(1)   

# def callChatGPT_refine(data):
#     print("callChatGPT_refine")
#     print(data)
#     completion = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=[
#             {"role": "user", "content": """you are my shopping advisor. 
#             Define {target} as an item category or a concept of an item. 
#             Some qualities and properties I value when I choose {target} are presented as {qualities}, please respect these.
#             Generate a list of 3 specific items that fits the description of {target} as [choice1, choice2, choice3], 
#             breakdown each choice into [brand, item category, and model], 
#             Generate a brief description use first person angle, speak as if you have used the product and the description is from personal use experience. 
#             Generate a list of 3 pros and cons of each of your choices 
#             as [choice1[description, pro1, pro2,pro3,con1,con2,con3]].
#               Generate your response in valid JSON format, watch out for symbols or contents that may break valid JSON format.
#               Do not write anything outside of the JSON structure. 
#               Write the Value of JSON in """+ data['language'] +""", Key of JSON in English. 
#               Keep the value of brand and model in english.
#               The structure is as follow: 
#             {
#             "target": "",
#             "choices": [
#                 {
#                 "brand": "",
#                 "item_category": "",
#                 "model": "",
#                 "description": "",
#                 "pros": [],
#                 "cons": []
#                 },
#                 {
#                 "brand": "",
#                 "item_category": "",
#                 "model": "",
#                 "description": "",
#                 "pros": [],
#                 "cons": []
#                 },
#                 {
#                 "brand": "",
#                 "item_category": "",
#                 "model": "",
#                 "description": "",
#                 "pros": [],
#                 "cons": []
#                 }
#             ]
#             }
#             now {target} =""" + data['target'] + """, and {qialities} =""" + str(data['qualities'])
#             }
#     ]
#     )
#     response = completion.choices[0].message.content
#     print(response)
#     return response

def callChatGPT_ask(data):
    # print("callChatGPT_ask")
    # print(data)
    MAX_RETRIES = 3
    retries = 0
    while retries < MAX_RETRIES:
        try:
            completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "user", "content": """you are my shopping advisor. 
                    Answer my {question} about {target}, try to be specific and informative.
                    Define {details} as your product reference link.
                    {target} = """ + data['queryObject']['choice']['target'] + """.
                    {question} = """+ data['queryObject']['question'] + """. 
                    {details} = """+ data['queryObject']['choice']['url'] + """. 
                    Generate your response in valid JSON format, watch out for symbols or contents that may break valid JSON format.
                    Do not write anything outside of the JSON structure. 
                    Write the Value of JSON in """+ data['queryObject']['language'] +""", Key of JSON in English. 
                    Keep the value of brand and model in english. 
                    The structure is as follow, the key must be the word "answer": 
                    {
                    "answer": ""
                    }
                    """
                    }
            ]
            )
            response = completion.choices[0].message.content
            # print(response)
            return response
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        retries += 1
        time.sleep(1)

def callPaapi_variations(asin, result):
    result[0] = get_variations(asin)
    