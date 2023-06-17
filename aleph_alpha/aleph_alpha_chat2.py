import os
from typing import List
from aleph_alpha_client import Client, Document, QaRequest

client = Client(token=os.getenv("AA_TOKEN"))


def read_files(directory):
    files_content = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            with open(os.path.join(directory, filename), 'r') as file:
                files_content.append(file.read())
    return files_content


class ChatAgent:
    def __init__(self, documents: List[str]):
        self.document_base = documents

    def answer(self, query: str):
        params = {
            "query": query,
            "documents": [
                Document.from_text(document) for document in self.document_base
            ],
        }
        request = QaRequest(**params)
        response = client.qa(request=request)
        if response.answers:
            reply = response.answers[0].answer.strip()
        else:
            reply = "Sorry, I cannot answer your question based on the available documents."
        return reply


documents = read_files(os.getenv("DOCUMENTS_DIR"))
chat_agent = ChatAgent(documents=documents)

questions = os.getenv("QUESTIONS").split(";")

for question in questions:
    agent_message = chat_agent.answer(query=question)
    print(f"Q: {question}\nA: {agent_message}\n")
