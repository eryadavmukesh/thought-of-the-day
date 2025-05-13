from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain.memory import ConversationBufferMemory
from prompts.thought_prompt import ThoughtPromptTemplate
from dotenv import load_dotenv
import json
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
OPENAI_API_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
OPENAI_API_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_API_DEPLOYMENT_NAME")
OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_VERSION")


class ThoughtGenerator:
    def __init__(self):
        self.llm = ChatOpenAI(
            openai_api_key=OPENAI_API_KEY,
            azure_endpoint=OPENAI_API_ENDPOINT,
            deployment_name=OPENAI_API_DEPLOYMENT_NAME,
            openai_api_version=OPENAI_API_VERSION,
            temperature=0.7,
            max_tokens=200,
        )

        self.memory = ConversationBufferMemory(
            return_messages=True, memory_key="chat_history"
        )

        self.prompt = ThoughtPromptTemplate().get_thought_prompt()
        self.parser = JsonOutputParser()

        # Create a chain pipeline
        self.chain = self.prompt | self.llm | self.parser

    def get_thought(self, theme=""):
        try:
            memory_context = self.memory.load_memory_variables({})

            result = self.chain.invoke(
                {
                    "theme": theme or "random",
                    "chat_history": memory_context["chat_history"],
                }
            )
            self.memory.save_context(
                inputs={"human": f"Theme: {theme or 'random'}"},
                outputs={"assistant": json.dumps(result)},
            )
            return result
        except Exception as e:
            return {"error": f"Failed to generate thought: {str(e)}"}
