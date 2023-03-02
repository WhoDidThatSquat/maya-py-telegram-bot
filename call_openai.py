import os
import openai
def req_openai(text_to_send):
    openai.api_key = ""
    completion = openai.Completion.create(
      model="text-davinci-002",
      prompt=text_to_send,
      max_tokens=200,
      temperature=0.5
    )
    return(completion.choices[0].text)
