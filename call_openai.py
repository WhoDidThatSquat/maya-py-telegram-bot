import os
import openai
import api_key
def req_openai(text_to_send):
    openai.api_key = api_key.openai_api_key()
    completion = openai.Completion.create(
      model="text-davinci-003",
      prompt=text_to_send,
      max_tokens=200,
      temperature=1.2
    )
    return(completion.choices[0].text)
