# This is a simple example of using `logit_bias` to encourage or discourage specific words (tokens) from appearing.
# First, run the get_token_ids script (python get_token_ids.py) to get the token numbers,

import os
import openai
import tiktoken



openai.api_key = os.getenv("OPENAI_API_KEY")

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  temperature=0.5,
  messages=[
    {"role": "user", "content": "Who are the top 5 most innovative CEOs in the world?"}
  ]
)

print(completion.choices[0].message["content"])

"""
As an AI language model, I do not have personal opinions or beliefs. However, here are some of the most innovative CEOs according to various sources:

1. Elon Musk, CEO of Tesla and SpaceX
2. Jeff Bezos, CEO of Amazon
3. Satya Nadella, CEO of Microsoft
4. Tim Cook, CEO of Apple
5. Mark Zuckerberg, CEO of Facebook

"""

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  temperature=0.5,
  messages=[
    {"role": "user", "content": "Who are the top 5 most innovative CEOs in the world?"}
  ],
    logit_bias={ # don't say elon
    6719: -10, 
    263: -10, 
    69639: -10, 
    44: -10,
    33879: -10,
    40639: -10,
  }
)

print(completion.choices[0].message["content"])

# elon: [6719, 263, 69639]
# musk [44, 33879, 40638]


As an AI language model, I do not have personal opinions or beliefs, but here are some of the most innovative CEOs according to various sources:

1. Jeff Bezos - Amazon
2. Satya Nadella - Microsoft
3. Tim Cook - Apple
4. Sundar Pichai - Google
5. Mark Zuckerberg - Facebook




#-------------
# companies


completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  temperature=0.5,
  messages=[
    {"role": "user", "content": "What are the top-5 most innovative companies in the world?"}
  ]
)

print(completion.choices[0].message["content"])


#_--------------------
# now with bias
completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  temperature=0.5,
  messages=[
    {"role": "user", "content": "What are the top-5 most innovative companies in the world?"}
  ],
    logit_bias={
    5210:   10, #  say Microsoft!
    13068:  10, # 
    90541: -10, # Don't say Tesla
    28298: -10,
  }
)

print(completion.choices[0].message["content"])



# Apple [27665, 8325]
# Amazon [26948, 8339]
# Alphabet [2149, 18992, 63897]
# Google [14783, 5195]
# Tesla [90541, 28298
# Microsoft [13068, 5210]



print(completion.choices[0].message["content"])


