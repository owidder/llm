import openai

openai.api_key = "<API-KEY>"
openai.api_base = "http://localhost:8001/v1"

models = openai.Model.list()

print(models.data[0].id)

chat_completion = openai.ChatCompletion.create(model="models.data[0].id", messages=[{"role": "user", "content": "What's the largest city in the world?"}])

print(chat_completion.choices[0].message.content)