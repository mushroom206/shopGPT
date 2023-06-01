import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get the API key from the environment variables and set it for the openai package
openai.api_key = os.getenv('OPENAI_API_KEY')

def callChatGPT(data):
    print("callChatGPT")
    print(data)
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "user", "content": """you are my shopping advisor. 
            Define {target} as an item category or a concept of an item. 
            Generate a list of 3 specific items that fits the description of {target} as [choice1, choice2, choice3], 
            breakdown each choice into [brand, item category, and model], 
            detailed enough so I can use your response to query for the items on a shopping site like Amazon. 
            Generate a brief description and a list of 3 pros and cons of each of your choices 
            as [choice1[description, pro1, pro2,pro3,con1,con2,con3]]. 
              In addition, generate 3 most common and important quality or properties specific to {target} that may affect your choices. 
              for example, 
              if {target} = rice cooker, the quality or properties that may affect your choices can be price, size, design, etc. 
              For each quality or property, generate 3 options so fine tune choices is possible, 
              provide numerical range for each option if applicable. 
              Generate your response in valid JSON format, watch out for symbols or contents that may break valid JSON format.
              Do not write anything outside of the JSON structure. 
              Write the Value of JSON in """+ data['language'] +""", Key of JSON in English. 
              Keep the value of brand and model in english.
              The structure is as follow: 
            {
            "target": "",
            "choices": [
                {
                "brand": "",
                "item_category": "",
                "model": "",
                "description": "",
                "pros": [],
                "cons": []
                },
                {
                "brand": "",
                "item_category": "",
                "model": "",
                "description": "",
                "pros": [],
                "cons": []
                },
                {
                "brand": "",
                "item_category": "",
                "model": "",
                "description": "",
                "pros": [],
                "cons": []
                }
            ],
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
            },
            ],
            }
            now {target} =""" + data['item_query']
            }
    ]
    )
    response = completion.choices[0].message.content
    print(response)
    return response

def callChatGPT_refine(data):
    print("callChatGPT_refine")
    print(data)
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "user", "content": """you are my shopping advisor. 
            Define {target} as an item category or a concept of an item. 
            Some qualities and properties I value when I choose {target} are presented as {qualities}, please respect these.
            Generate a list of 3 specific items that fits the description of {target} as [choice1, choice2, choice3], 
            breakdown each choice into [brand, item category, and model], 
            Generate a brief description and a list of 3 pros and cons of each of your choices 
            as [choice1[description, pro1, pro2,pro3,con1,con2,con3]].
              Generate your response in valid JSON format, watch out for symbols or contents that may break valid JSON format.
              Do not write anything outside of the JSON structure. 
              Write the Value of JSON in """+ data['language'] +""", Key of JSON in English. 
              Keep the value of brand and model in english.
              The structure is as follow: 
            {
            "target": "",
            "choices": [
                {
                "brand": "",
                "item_category": "",
                "model": "",
                "description": "",
                "pros": [],
                "cons": []
                },
                {
                "brand": "",
                "item_category": "",
                "model": "",
                "description": "",
                "pros": [],
                "cons": []
                },
                {
                "brand": "",
                "item_category": "",
                "model": "",
                "description": "",
                "pros": [],
                "cons": []
                }
            ]
            }
            now {target} =""" + data['target'] + """, and {qialities} =""" + str(data['qualities'])
            }
    ]
    )
    response = completion.choices[0].message.content
    print(response)
    return response

def callChatGPT_ask(data):
    print("callChatGPT_ask")
    print(data)
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "user", "content": """you are my shopping advisor. 
            Answer my question about this item, represented as [brand, item_category, model]: 
            ["""+ data['queryObject']['choice']['brand'] +""", """+ data['queryObject']['choice']['item_category'] +""", """+ data['queryObject']['choice']['model'] +"""].
            The question is: """+ data['queryObject']['question'] +""". 
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