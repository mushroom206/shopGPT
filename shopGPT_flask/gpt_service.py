import openai
from dotenv import load_dotenv
import os
import threading
import json
import random

# Load environment variables
load_dotenv()

# Get the API key from the environment variables and set it for the openai package
openai.api_key = os.getenv('OPENAI_API_KEY')

def callChatGPT_list(data):
    print("callChatGPT_list")
    print(data)
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "user", "content": """Generate a list of items essential to {context} as [item1,item2,item3...], so I can shop and prepare for {context}.
              Generate items specific to {context}, eliminate ambiguity.
              Generate a brief tip specific to {context}.
              Do not generate items relates to subcriptions or memberships.
              Do not generate desciption of items. Max 15 most important items, Min 10 items. 
              Generate your response in valid JSON format, watch out for symbols or contents that may break valid JSON format.
              Do not write anything outside of the JSON structure. 
              Write the Value of JSON in """+ data['language'] +""", Key of JSON in English. 
              The structure is as follow: 
            {
            "context": "",
            "itemList": [],
            "tip": ""
            }
            now {context} =""" + data['list_query']
            }
    ]
    )
    response = completion.choices[0].message.content
    # print(response)
    return response

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
    image_urls = [[],[],[]]
    prices = []
    search_results = random.sample(search_results, min(3, len(search_results)))
    for i, search_result in enumerate(search_results):
        data = {
            "language": language,
            "item_query": search_result.item_info.title.display_value,
            "details": search_result.detail_page_url
        }

        image_urls[i].append(search_result.images.primary.large.url)
        for url in search_result.images.variants:
            image_urls[i].append(url.large.url)
        try:
            prices.append(search_result.offers.listings[0].price.display_amount)
        except AttributeError:
            prices.append("view on item details page")

        thread = threading.Thread(target=callChatGPT, args=(data, results[i]))
        thread.start()
        threads.append(thread)
        # thread = threading.Thread(target=callChatGPT_description, args=(data, results[i+3]))
        # thread.start()
        # threads.append(thread)


    # Wait for all threads to finish.
    for thread in threads:
        thread.join()

    # Get the results for each thread.
    response = {
            "target" : target,
            "choices": []
            }
    for x in range(3):
        if results[x][0] is not None:
          temp1 = json.loads(results[x][0])
          # temp2 = json.loads(results[x+3][0])
          tempJSON = {
                  "target": temp1['target'],
                  # "description": temp2['description'],
                  "pros": temp1['pros'],
                  "cons": temp1['cons'],
                  "url": search_results[x].detail_page_url,
                  "price": prices[x],
                  "image_urls": image_urls[x]
                  }
          response['choices'].append(tempJSON)

    # print(response)
    return response 

def callChatGPT(data, result):
    # print("callChatGPT")
    # print(data)
    # Generate a list of 3 specific items that fits the description of {target} as [choice1, choice2, choice3], 
    # breakdown each choice into [brand, item category, and model], 
    # detailed enough so I can use your response to query for the items on a shopping site like Amazon. 
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "user", "content": """you are my shopping advisor. 
            Define {target} as a product.
            Define {details} as product reference link to help you generate response.
            In """+ data['language'] +""", generate a list of 3 pros and cons of {target}.
              Generate your response in valid JSON format, watch out for symbols or contents that may break valid JSON format. 
              Do not write anything outside of the JSON structure. 
              Write the Value of JSON in """+ data['language'] +""", Key of JSON in English. 
              Keep the Value of {target} in english, make it concise max 5 words.
              The structure is as follow: 
            {
              "target": "",
              "pros": [],
              "cons": []
            }
            now {target} =""" + data['item_query'] + """. {details} = """ + data['details']
            }
    ]
    )
    response = completion.choices[0].message.content
    result[0] = response

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
    print("callChatGPT_properties")
    print(data)
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "user", "content": """you are my shopping advisor. 
            Define {target} as an item category or a concept of an item. 
              In """+ data['language'] +""", generate 3 most common and important quality or properties specific to {target} that affect how consumers compare {target}, but do not include price. 
              For example, 
              if {target} = rice cooker, the quality or properties that may affect your choices can be price, size, design, etc. 
              For each quality or property, generate 3 options,the options should by itself reflect the quality or property of {target}. 
              Options should be specific enough to help further filtering possible results on site like Amazon.
              For search accuracy, use only numerical value in options if applicable.
              Generate your response in valid JSON format, watch out for symbols or contents that may break valid JSON format.
              Do not write anything outside of the JSON structure. 
              Write the Value of JSON in """+ data['language'] +""", Key of JSON in English. 
              Keep the Value of {target} in english.
              The structure is as follow: 
            {
            "target": "",
            "qualities-properties": [
            {
            "quality":””,
            "options": []
            },
            {
            "quality":””,
            "options": []
            },
            {
            "quality":””,
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
    print("callChatGPT_ask")
    print(data)
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
    print(response)
    return response