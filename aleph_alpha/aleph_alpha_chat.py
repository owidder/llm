import os
from typing import List
from aleph_alpha_client import Client, CompletionRequest, Document, Prompt, QaRequest

client = Client(token=os.getenv("AA_TOKEN"))


def read_files(directory):
    files_content = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            with open(os.path.join(directory, filename), 'r') as file:
                files_content.append(file.read())
    return files_content


class ChatMemory:
    def __init__(self):
        self.user_messages = []
        self.agent_messages = []

    def memorize_user_message(self, msg: str):
        self.user_messages.append(msg)

    def memorize_agent_message(self, msg: str):
        self.agent_messages.append(msg)

    # this function takes the entire memory (itself) and returns it as a string
    def get_as_string(self, user_prefix: str, agent_prefix: str):
        user_strings = (f"{user_prefix}: {msg}" for msg in self.user_messages)
        agent_strings = (f"{agent_prefix}: {msg}" for msg in self.agent_messages)
        return "\n".join([f"{x}\n{y}" for x, y in zip(user_strings, agent_strings)])


class ChatAgent:
    def __init__(
        self,
        documents: List[str],
        name: str,
        enable_smalltalk: bool = True,
    ):
        self.document_base = documents
        self.name = name
        self.enable_smalltalk = enable_smalltalk
        self.memory = ChatMemory()

    def answer_smalltalk(self, query: str):
        if not self.enable_smalltalk:
            return "Sorry, I cannot answer your question based on the available documents."

        # building the prompt based on the prior conversation, a description of the chat agent and the most recent user query
        # this prompt will then be sent to our complete endpoint to generate a smalltalk response
        prompt = (
            f"""A chat agent called {self.name} is helping a user navigate the world of sports knowledge.
{self.name}: Hello, I'm {self.name}, your sports information agent."""
            + self.memory.get_as_string(agent_prefix="{self.name}", user_prefix="User")
            + f"""
User: {query}
{self.name}:"""
            )
        params = {
            "prompt": Prompt.from_text(prompt),
            "maximum_tokens": 64,
            "stop_sequences": ["\n"],
        }
        request = CompletionRequest(**params)
        response = client.complete(request=request, model="luminous-supreme")
        return response.completions[0].completion.strip()

    def memorize(self, query: str, reply: str):
        self.memory.memorize_user_message(msg=query)
        self.memory.memorize_agent_message(msg=reply)

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
            reply = self.answer_smalltalk(query=query)
        self.memorize(query=query, reply=reply)
        return reply


documents = read_files("./docs")
chat_agent = ChatAgent(documents=documents, name="Dave", enable_smalltalk=False)

agent_message = chat_agent.answer(query="What is a knotterbex policy?")
print(f"Agent message: {agent_message}")

agent_message = chat_agent.answer(query="Is it efficient?")
print(f"Agent message: {agent_message}")

agent_message = chat_agent.answer(query="How does it interact with other policy measures?")
print(f"Agent message: {agent_message}")
