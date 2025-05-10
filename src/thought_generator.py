from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain.memory import ConversationBufferMemory
from prompts.thought_prompt import get_thought_prompt
from src.prompts.thought_prompt import ThoughtPromptTemplate
from dotenv import load_dotenv
import json
import os

load_dotenv()

class ThoughtGenerator:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.7,
            max_tokens=200,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.memory = ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history"
        )

        self.prompt = ThoughtPromptTemplate().get_thought_prompt()
        self.parser = JsonOutputParser()

        # Create a chain pipeline
        self.chain = self.prompt | self.llm | self.parser

    def get_thought(self, theme=""):
        try:
            memory_context = self.memory.load_memory_variables({})
            
            result = self.chain.invoke({
                "theme": theme or "random",
                "chat_history": memory_context["chat_history"]
            })
            self.memory.save_context(
                inputs={"human": f"Theme: {theme or 'random'}"},
                outputs={"assistant": json.dumps(result)}
            )
            return result
        except Exception as e:
            return {"error": f"Failed to generate thought: {str(e)}"}