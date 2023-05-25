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
            I will provide an item category or a concept of an item defined as {target}, 
            you will give me a list of 3 specific items, represented as [choice1, choice2, choice3] and breakdown each choice into [brand, 
            item category, and model], that fits the description of {target}, 
            detailed enough so I can use your response to query for the items on a shopping site like Amazon, 
            give a brief description and a list of 3 pros and cons of each of your choices,
              represented as [choice1[description, pro1, pro2,pro3,con1,con2,con3]]. 
              You will also give me 3 common and important quality or properties specific to {target} that may affect your choices. for example, 
              if {target} = rice cooker, the quality or properties that may affect your choices can be price, size, design, etc. 
              For each quality or property, provide 3 options so you can fine tune your choices accordingly, 
              provide numerical range for each option if applicable. 
              Write your response in JSON and only JSON, so I can utilize your whole response directly in my app. 
              The format is as follow: 
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
            quality:””,
            options[]
            },
            {
            quality:””,
            options[]
            },
            {
            quality:””,
            options[]
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
            I will provide an item category or a concept of an item defined as {target}, 
            I will also provide some qualities or properties I value when choose {target}, defined as {qualities}, please respect these.
            you will give me a list of 3 specific items, represented as [choice1, choice2, choice3] and breakdown each choice into [brand, 
            item category, and model], that fits the description of {target}, 
            detailed enough so I can use your response to query for the items on a shopping site like Amazon, 
            give a brief description and a list of 3 pros and cons of each of your choices,
              represented as [choice1[description, pro1, pro2,pro3,con1,con2,con3]]. 
              Write your response in JSON and only JSON, so I can utilize your whole response directly in my app. 
              The format is as follow: 
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
            ["""+ data['choice']['brand'] +""", """+ data['choice']['item_category'] +""", """+ data['choice']['model'] +"""].
            The question is: """+ data['question'] +""". 
              Write your response in JSON and only JSON, so I can utilize your whole response directly in my app. 
              The format is as follow: 
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