import os
from aleph_alpha_client import Client, Document, QaRequest
# If you are using a Windows machine, you must install the python-dotenv package and run the two below lines as well.
# from dotenv import load_dotenv
# load_dotenv()

client = Client(token=os.getenv("AA_TOKEN"))
query_text = "When did wolves first appear?"
document_text = "The gray wolf (Canis lupus) is a species of placental mammal of the carnivore order. The earliest fossil record dates back eight hundred thousand years. Wolves are native to North America and Eurasia, where they were once widely distributed and abundant. Today, they inhabit only a very limited portion of their former territory."
params = {
    "query": query_text,
    "documents": [Document.from_text(document_text)]
}
request = QaRequest(**params)
response = client.qa(request=request)
answer = response.answers[0].answer

print(f"""Document: {document_text}
Q: {query_text}
A: {answer}""")
# prints:
# Document: [...]
# Q: When did wolves first appear?
# A: Wolves first appeared eight hundred thousand years ago.